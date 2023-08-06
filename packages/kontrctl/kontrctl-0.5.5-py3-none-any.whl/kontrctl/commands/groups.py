import click

from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers
from kontrctl.utils.helpers import entity_printer

cli_groups = click.Group('groups', help='Groups management')


@cli_groups.command('list', help='List all groups')
@click.option('-c', '--course', required=False, help='Select course')
@click.pass_obj
def cli_groups_list(obj: AppConfig, course):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    groups = course.groups.list()
    helpers.generic_list(groups, params=['id', 'name', 'course.codename'])


@cli_groups.command('read', help='Get a group info')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_groups_read(obj: AppConfig, remote, course, codename: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    helpers.generic_read(course.groups, codename)


@cli_groups.command('rm', help='Delete group')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_groups_delete(obj: AppConfig, remote, course, codename: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    print(f"Removing group: {codename}")
    course.groups.delete(codename)


@cli_groups.command('edit', help='Edit group')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_groups_edit(obj: AppConfig, remote, course, codename: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    helpers.generic_edit(course.groups, codename)


@cli_groups.command('create', help='Create group')
@click.option('-c', '--course', required=False, help='Select course')
@click.option('-N', '--name', prompt=True, required=False, help='Name')
@click.option('-n', '--codename', prompt=True, required=False, help='Codename')
@click.option('-d', '--description', prompt=True, required=False, help='Description')
def cli_groups_create(obj, remote, course, **kwargs):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    helpers.generic_create(course.groups.create, **kwargs)


#
# Group users
#

cli_group_users = click.Group('users', help='Users management for the group')
cli_groups.add_command(cli_group_users)


@cli_group_users.command('list', help='List users for the group')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_group_users_list(obj: AppConfig, remote, course, codename: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    helpers.generic_list_users(course.groups, codename)


@cli_group_users.command('add', help='Add user for the group')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.argument('user')
@click.pass_obj
def cli_group_users_add(obj: AppConfig, remote, course, codename: str, user: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    helpers.generic_add_client(course.groups, codename, user)


@cli_group_users.command('rm', help='Removes user from the group')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.argument('user')
@click.pass_obj
def cli_group_users_rm(obj: AppConfig, course, codename: str, user: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    helpers.generic_remove_client(course.groups, codename, user)


#
# Group projects
#

cli_group_projects = click.Group('projects',
                                 help='Project management for the group')
cli_groups.add_command(cli_group_projects)


@cli_group_projects.command('list', help='List projects for the group')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_group_projects_list(obj: AppConfig, course, codename: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    helpers.generic_list_projects(course.groups, codename)


@cli_group_projects.command('add', help='Add project for the group')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.argument('project')
@click.pass_obj
def cli_group_projects_add(obj: AppConfig, course, codename: str, project: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    helpers.generic_add_project(course.groups, codename, project)


@cli_group_projects.command('rm', help='Removes project from the group')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.argument('project')
@click.pass_obj
def cli_group_projects_(obj: AppConfig, course, codename: str, project: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    helpers.generic_remove_project(course.groups, codename, project)
