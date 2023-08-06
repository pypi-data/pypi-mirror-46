import click

from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers

cli_components = click.Group('components', help='Users management')


@cli_components.command('list', help='List all components')
@click.option('-r', '--remote', required=False, help='Sets remote for the login')
@click.pass_obj
def cli_components_list(obj: AppConfig, remote):
    remote: Remote = helpers.get_remote(obj, remote)
    components = remote.kontr_client.components.list()
    for component in components:
        print(f"{component['name']} ({component['id']})")


@cli_components.command('read', help='Get a component info')
@click.option('-r', '--remote', required=False, help='Sets remote for the login')
@click.argument('codename')
@click.pass_obj
def cli_components_read(obj: AppConfig, remote, codename: str):
    remote: Remote = helpers.get_remote(obj, remote)
    helpers.generic_read(remote.kontr_client.components, codename)


@cli_components.command('delete', help='Delete component')
@click.option('-r', '--remote', required=False, help='Sets remote for the login')
@click.argument('codename')
@click.pass_obj
def cli_components_delete(obj: AppConfig, remote, codename: str):
    remote: Remote = helpers.get_remote(obj, remote)
    print(f"Removing component: {codename}")
    remote.kontr_client.components.delete(codename)


@cli_components.command('edit', help='Edit component')
@click.option('-r', '--remote', required=False, help='Sets remote')
@click.argument('codename')
@click.pass_obj
def cli_users_edit(obj: AppConfig, remote, codename: str):
    remote: Remote = helpers.get_remote(obj, remote)
    helpers.generic_edit(remote.kontr_client.components, codename)
