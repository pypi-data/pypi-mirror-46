import click
from kontr_api.resources import Role

from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers

cli_permissions = click.Group('permissions', help='Permissions management')


@cli_permissions.command('read', help='Get a permission info for the role by it\'s codename')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_permissions_read(obj: AppConfig, course, codename: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    role: Role = helpers.read_helper(course.roles, codename)
    helpers.entity_printer(role.permissions.read())


@cli_permissions.command('edit', help='Edit permissions for the role')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_permissions_edit(obj: AppConfig, course, codename: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    role: Role = helpers.read_helper(course.roles, codename)
    permissions = role.permissions.read()
    helpers.edit_and_update_entity(permissions)
