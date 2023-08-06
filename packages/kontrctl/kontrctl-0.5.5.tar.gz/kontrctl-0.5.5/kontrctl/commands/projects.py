import click

from kontrctl.commands.project_configs import cli_project_configs
from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers

cli_projects = click.Group('projects', help='Projects management')

cli_projects.add_command(cli_project_configs)


@cli_projects.command('list', help='List all projects')
@click.option('-c', '--course', required=False, help='Select course')
@click.pass_obj
def cli_projects_list(obj: AppConfig, course):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    projects = course.projects.list()
    helpers.generic_list(
        projects, params=['id', 'name', 'codename', 'course.codename'])


@cli_projects.command('read', help='Get a project info')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_projects_read(obj: AppConfig, course, codename: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    helpers.generic_read(course.projects, codename)


@cli_projects.command('rm', help='Delete project')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_projects_delete(obj: AppConfig, course, codename: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    print(f"Removing project: {codename}")
    course.projects.delete(codename)


@cli_projects.command('select', help='Select project')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_projects_select(obj: AppConfig, course, codename: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    print(
        f"\nSelecting project: {codename} for remote course {course.name} using {remote.name}\n")
    remote.selected_project = codename
    remote.update()


@cli_projects.command('create', help='Create project')
@click.option('-c', '--course', required=False, help='Select course')
@click.option('-N', '--name', prompt=True, required=False, help='Name')
@click.option('-n', '--codename', prompt=True, required=False, help='Codename')
@click.option('-d', '--description', prompt=True, required=False, help='Description')
@click.option('-A', '--assignment-url', prompt=True, required=False, help='Assignment url')
def cli_projects_create(obj, course, **kwargs):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    helpers.generic_create(course.projects.create, **kwargs)


@cli_projects.command('deselect', help='Deselect project')
@click.option('-c', '--course', required=False, help='Select course')
@click.pass_obj
def cli_projects_deselect(obj: AppConfig):
    remote: Remote = obj.remote
    print(f"\nDeselecting project for remote {remote.name}\n")
    del remote.selected_project
    remote.update()


@cli_projects.command('edit', help='Edit project')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_projects_edit(obj: AppConfig, course, codename: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    helpers.generic_edit(course.projects, codename)


@cli_projects.command('refresh-files', help='Refresh project files')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_projects_refresh_files(obj: AppConfig, course, codename: str):
    remote: Remote = obj.remote
    course = helpers.get_course(remote, course)
    print(f"Refreshing project config: {course['codename']}/{codename}")
    course.projects.refresh_tests(codename)
