import click

from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers


@click.command('submit', help='Create new submission')
@click.option('-c', '--course', required=False, help='Sets course')
@click.option('-p', '--project', required=False, help='Sets project')
@click.option('-t', '--source-type', required=False, default='git',
              help='Sets type of submission files source (git)')
@click.option('-u', '--url', help='Source url - i.e. git repo url')
@click.option('-b', '--branch', required=False,
              help='Source branch - default: master')
@click.option('--checkout', help='Checkout param', required=False)
@click.option('-D', '--directory', help='Submission subdir', required=False)
@click.pass_obj
def cli_submit(obj: AppConfig, course, project, source_type, url, branch, checkout, directory):
    remote: Remote = obj.remote    
    course = helpers.get_course(remote, course)
    project = helpers.get_project(remote, course, project)
    file_params = _create_file_params(source_type, url, branch, checkout, directory)
    config = dict(file_params=file_params, project_params={})
    submission = project.submit(config)
    helpers.entity_printer(submission)


def _create_file_params(source_type, url: str, branch: str,
                        checkout: str, directory: str):
    source = dict(type=source_type, url=url)
    if branch:
        source['branch'] = branch
    if checkout:
        source['checkout'] = checkout
    file_params = dict(source=source, from_dir=directory)
    return file_params
