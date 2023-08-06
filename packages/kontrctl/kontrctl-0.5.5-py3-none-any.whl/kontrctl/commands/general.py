import click

import kontr_api

from kontrctl.config import AppConfig
from kontrctl.utils import helpers


@click.command('info', help="Get info")
@click.pass_obj
def cli_info(obj: AppConfig):
    print("Kontrctl - Tool control the Kontr 2.0\n")
    print(f"Version: {obj.version}")
    print(f"Kontr-Api Version: {kontr_api.__version__}\n")
    remote_name = obj.config.default_remote
    if remote_name:
        _remote_info(obj, remote_name)


def _remote_info(obj, remote_name: str):
    print(f"Selected remote: {remote_name}")
    remote = helpers.get_remote(obj, remote_name)

    def __get_info(message, selector):
        if selector:
            print(f"{message}: {selector}")

    __get_info('Selected course', remote.selected_course)
    __get_info('Selected project', remote.selected_project)
    __get_info('Logged in user', remote.config.get('username'))
    __get_info('Logged in using identifier', remote.config.get('identifier'))
