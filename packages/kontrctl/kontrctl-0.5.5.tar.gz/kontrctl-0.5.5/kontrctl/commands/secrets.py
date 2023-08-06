from datetime import datetime

import click

from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers

cli_secrets = click.Group('secrets', help='Workers management')


@cli_secrets.command('list', help='List all secrets')
@click.option('-u', '--user', required=False, help='Selects user')
@click.option('-w', '--worker', required=False, help='Selects worker')
@click.pass_obj
def cli_secrets_list(obj: AppConfig, user=None, worker=None):
    remote: Remote = obj.remote    
    client = helpers.get_any_client(remote, user, worker)
    secrets = client.secrets.list()
    helpers.generic_list(secrets, params=['name', 'id'])


@cli_secrets.command('read', help='Get a secret info')
@click.option('-u', '--user', required=False, help='Selects user')
@click.option('-w', '--worker', required=False, help='Selects worker')
@click.argument('codename')
@click.pass_obj
def cli_secrets_read(obj: AppConfig, user=None, worker=None, codename: str = None):
    remote: Remote = obj.remote    
    client = helpers.get_any_client(remote, user, worker)
    helpers.generic_read(client.secrets, codename)


@cli_secrets.command('delete', help='Delete secret')
@click.option('-u', '--user', required=False, help='Selects user')
@click.option('-w', '--worker', required=False, help='Selects worker')
@click.argument('codename')
@click.pass_obj
def cli_secrets_delete(obj: AppConfig, codename: str, user=None, worker=None):
    remote: Remote = obj.remote    
    client = helpers.get_any_client(remote, user, worker)
    print(f"Removing secret: {codename}")
    client.secrets.delete(codename)


@cli_secrets.command('create', help='Create secret')
@click.option('-u', '--user', required=False, help='Selects user')
@click.option('-w', '--worker', required=False, help='Selects worker')
@click.option('-N', '--name', prompt=True, required=False, help='Name')
@click.option('-E', '--expiration', required=False,
              help='Expiration date and time (YEAR-MONTH-DAY)')
@click.pass_obj
def cli_secrets_create(obj: AppConfig, user=None, worker=None, name=None, expiration=None):
    remote: Remote = obj.remote    
    client = helpers.get_any_client(remote, user, worker)
    params = dict(name=name)
    if expiration:
        params['expiration'] = datetime.strptime(expiration, "%Y-%m-%d")
    secret = client.secrets.create(params)
    print(f"Secret ({secret['id']}): {secret['value']}")
