import click

from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers

cli_workers = click.Group('workers', help='Workers management')


@cli_workers.command('list', help='List all workers')
@click.pass_obj
def cli_workers_list(obj: AppConfig):
    remote: Remote = obj.remote
    workers = remote.kontr_client.workers.list()
    helpers.generic_list(workers, params=['id', 'codename', 'state', 'url'])


@cli_workers.command('read', help='Get a worker info')
@click.argument('codename')
@click.pass_obj
def cli_workers_read(obj: AppConfig, codename: str):
    remote: Remote = obj.remote
    helpers.generic_read(remote.kontr_client.workers, codename)


@cli_workers.command('status', help='Get a worker status')
@click.argument('codename')
@click.pass_obj
def cli_workers_status(obj: AppConfig, codename: str):
    remote: Remote = obj.remote
    worker = helpers.read_helper(remote.kontr_client.workers, codename)
    status = worker.status.read()
    helpers.entity_printer(status)


@cli_workers.command('delete', help='Delete worker')
@click.argument('codename')
@click.pass_obj
def cli_workers_delete(obj: AppConfig, codename: str):
    remote: Remote = obj.remote
    print(f"Removing worker: {codename}")
    remote.kontr_client.workers.delete(codename)


@cli_workers.command('edit', help='Edit worker')
@click.argument('codename')
@click.pass_obj
def cli_workers_edit(obj: AppConfig, codename: str):
    remote: Remote = obj.remote
    helpers.generic_edit(remote.kontr_client.workers, codename)


@cli_workers.command('create', help='Create worker')
@click.option('-n', '--name', prompt=True, required=False, help='Name of the worker')
@click.option('-U', '--url', required=False, help='Url')
@click.option('-P', '--portal_secret', required=False, help='Portal secret')
@click.option('-T', '--tags', required=False, help='Tags')
def cli_workers_create(obj, **kwargs):
    remote: Remote = obj.remote
    helpers.generic_create(remote.kontr_client.workers.create, **kwargs)
