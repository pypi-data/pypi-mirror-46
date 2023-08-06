import click

from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers

cli_roles = click.Group('roles', help='Roles management')


@cli_roles.command('list', help='List all roles')
@click.option('-c', '--course', required=False, help='Select course')
@click.pass_obj
def cli_roles_list(obj: AppConfig, course):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    roles = course.roles.list()
    helpers.generic_list(roles, params=['id', 'name', 'course.codename'])


@cli_roles.command('read', help='Get a role info')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_roles_read(obj: AppConfig, course, codename: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    helpers.generic_read(course.roles, codename)


@cli_roles.command('rm', help='Delete role')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_roles_delete(obj: AppConfig, course, codename: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    print(f"Deleting the role: {codename}")
    course.roles.delete(codename)


@cli_roles.command('edit', help='Edit roles')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_roles_edit(obj: AppConfig, course, codename: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    helpers.generic_edit(course.roles, codename)


@cli_roles.command('create', help='Create role')
@click.option('-c', '--course', required=False, help='Select course')
@click.option('-N', '--name', prompt=True, required=False, help='Name')
@click.option('-n', '--codename', prompt=True, required=False, help='Codename')
@click.option('-d', '--description', prompt=True, required=False, help='Description')
def cli_roles_create(obj, course, **kwargs):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    helpers.generic_create(course.roles.create, **kwargs)


#
# Role users
#

cli_role_users = click.Group('clients', help='Clients management for the role')
cli_roles.add_command(cli_role_users)


@cli_role_users.command('list', help='List clients for the role')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_role_users_list(obj: AppConfig, course, codename: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    helpers.generic_list_users(course.roles, codename, name='clients')


@cli_role_users.command('add', help='Add client to the role')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.argument('client')
@click.pass_obj
def cli_role_users_add(obj: AppConfig, course, codename: str, client: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    helpers.generic_add_client(course.roles, codename, client)


@cli_role_users.command('rm', help='Remove client from the role')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.argument('client')
@click.pass_obj
def cli_role_users_rm(obj: AppConfig, course, codename: str, client: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    helpers.generic_remove_client(course.roles, codename, client)
