import logging

import click

from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers

log = logging.getLogger(__name__)


@click.command('shell',
               help="Start the shell - IPython is currently supported - needs to be installed")
@click.pass_obj
def cli_shell(obj: AppConfig, remote: str):
    remote: Remote = obj.remote
    try:
        _load_shell(remote)
    except ImportError:
        print("You have not installed the IPython package,\n"
              "to solve this problem please run:\n\n"
              "$ pip install ipython\n\nIn order to be able to use this feature")


def _load_shell(remote: Remote):
    import IPython
    kontr_client = remote.kontr_client
    IPython.embed()
