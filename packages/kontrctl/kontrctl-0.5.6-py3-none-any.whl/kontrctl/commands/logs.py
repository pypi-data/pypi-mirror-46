import logging

import click

from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers

log = logging.getLogger(__name__)


@click.command('logs', help="Show logs")
@click.option('-f', '--file', required=False, help='Show log content by filename', default=None)
@click.pass_obj
def cli_logs(obj: AppConfig, file: str = None):
    remote: Remote = obj.remote
    if file:
        print(remote.kontr_client.management.logs_file(path=file))
    else:
        print("Available logs: ")
        logs_tree = remote.kontr_client.management.logs_tree()
        helpers.entity_printer(logs_tree)
