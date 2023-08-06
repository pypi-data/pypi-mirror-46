import logging

import click
from kontr_api import KontrClient

from kontrctl import errors
from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers

log = logging.getLogger(__name__)


@click.command('logout', help="Logout")
@click.option('-a', '--all', required=False, help='Remove all login info',
              is_flag=True, default=False)
@click.pass_obj
def cli_logout(obj: AppConfig, all: bool):
    remote: Remote = obj.remote
    print(f"Logout from: {remote.name} ({remote.url})")
    _logout(remote, all=all)
    helpers.entity_printer(remote)


def _logout(remote: Remote, all: bool):
    def __safe_del(remote: Remote, name: str):
        if name in remote.config:
            del remote.config[name]

    def __del_params(*params):
        for name in params:
            __safe_del(remote, name)

    __del_params('access_token', 'refresh_token')

    if all:
        __del_params('username', 'identifier', 'password', 'secret')
    remote.update()


@click.command('login', help="Login to portal")
@click.option('-u', '--user', required=False, help='Sets user login')
@click.option('-s', '--secret', required=False, help='Sets user secret')
@click.option('--keep-credentials', required=False, default=False, is_flag=True,
              help='Sets user login to remotes file')
@click.pass_obj
def cli_login(obj: AppConfig, user, secret, keep_credentials):
    remote = obj.remote
    print(f"Login to: {remote.name} ({remote.url})")
    credentials = ask_for_credentials(remote, user, secret)
    if keep_credentials:
        _save_credentials_to_remote(remote, **credentials)
    login_and_set_tokens(remote, **credentials)
    log.debug("Updated remote(%s): {%s}", remote.name, remote.config)
    helpers.entity_printer(remote)
    obj.save()


def ask_for_credentials(remote: Remote, user, secret) -> (str, str):
    user = user or remote['username']
    secret = secret or remote['secret']
    password = remote['password']
    if user is None:
        user = click.prompt('User')
    if password is None and secret is None:
        password = click.prompt('Password', hide_input=True)
    return dict(password=password, username=user, secret=secret, identifier=user)


def login_and_set_tokens(remote: Remote, **credentials) -> Remote:
    kontr: KontrClient = KontrClient(remote.url, **credentials)
    tokens = kontr.login()
    log.debug("[LOGIN] Tokens: %s", tokens)
    if 'access_token' not in tokens:
        raise errors.LoginNotSuccessfulError()
    remote['access_token'] = tokens['access_token']
    remote['refresh_token'] = tokens['refresh_token']
    remote.update()
    return remote


def _save_credentials_to_remote(remote: Remote, **credentials):
    for key, value in credentials.items():
        if value is not None:
            remote[key] = value
    remote.update()
    return remote
