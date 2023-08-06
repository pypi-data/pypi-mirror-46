import logging
from distutils import util

import click
import kontr_api

import kontrctl
from kontrctl import log_config
from kontrctl.commands import add_all_commands
from kontrctl.config import AppConfig

log = logging.getLogger('kontrctl.cli')


def str2bool(val) -> bool:
    if isinstance(val, str):
        return util.strtobool(val)

    return bool(val)


@click.group(help='Kontr portal Cli tool')
@click.version_option(kontrctl.__version__)
@click.option('-r', '--remote', required=False, help='Sets remote for the command')
@click.pass_context
def cli_main(ctx=None, remote=None):
    import os
    kontr_log = os.getenv('KONTR_LOG', 'false')
    if str2bool(kontr_log):
        log_config.load_logger()
    log.info(f"KONTRCTL Version: {kontrctl.__version__} "
             f"KONTR-API Version: {kontr_api.__version__}")
    ctx.obj = AppConfig(remote=remote)


add_all_commands(cli_main)

if __name__ == '__main__':
    cli_main()
