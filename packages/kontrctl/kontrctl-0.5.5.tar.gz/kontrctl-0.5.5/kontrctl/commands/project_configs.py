import click

from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers

cli_project_configs = click.Group('config', help='Projects configs management')


@cli_project_configs.command('read', help='Get a project config info')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_project_configs_read(obj: AppConfig, course, codename: str):
    remote: Remote = obj.remote    
    course = helpers.get_course(remote, course)
    project = helpers.read_helper(course.projects, codename)
    helpers.generic_read(project.project_config, codename)


@cli_project_configs.command('edit', help='Edit project config info')
@click.option('-c', '--course', required=False, help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_project_configs_edit(obj: AppConfig, course, codename: str):
    remote: Remote = obj.remote    
    course = helpers.get_course(remote, course)
    project = course.projects.read(codename)
    project_config = project.project_config.read()
    update_dict = helpers.edit_entity_using_editor(project_config)
    if update_dict is not None:
        project.project_config.update(update_dict)
    print(update_dict)
