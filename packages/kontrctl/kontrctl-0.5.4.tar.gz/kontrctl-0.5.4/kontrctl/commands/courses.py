import click
from kontr_api import resources

from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers

cli_courses = click.Group('courses', help='Courses management')


@cli_courses.command('list', help='List all courses')
@click.option('--ids', default=False, is_flag=True, required=False, help='Print just ids')
@click.option('--codes', default=False, is_flag=True, required=False,
              help='Print just course codes')
@click.pass_obj
def cli_courses_list(obj: AppConfig, ids, codes):
    remote: Remote = obj.remote
    courses = remote.kontr_client.courses.list()
    if not codes and not ids:
        helpers.generic_list(courses, params=['id', 'name', 'codename'])
        return
    for course in courses:
        if ids and codes:
            print(f"{course['codename']} {course['id']}")
        elif ids:
            print(course['id'])
        elif codes:
            print(course['codename'])


@cli_courses.command('read', help='Get a course info')
@click.argument('codename')
@click.pass_obj
def cli_courses_read(obj: AppConfig, codename: str):
    remote: Remote = obj.remote
    helpers.generic_read(remote.kontr_client.courses, codename)


@cli_courses.command('rm', help='Delete course')
@click.argument('codename')
@click.pass_obj
def cli_courses_rm(obj: AppConfig, codename: str):
    remote: Remote = obj.remote
    print(f"Removing course: {codename}")
    remote.kontr_client.courses.delete(codename)


@cli_courses.command('edit', help='Edit courses config')
@click.argument('codename')
@click.pass_obj
def cli_courses_edit(obj: AppConfig, remote, codename: str):
    remote: Remote = obj.remote
    helpers.generic_edit(remote.kontr_client.courses, codename)


@cli_courses.command('edit-create', help='Create course using editor')
def cli_courses_edit_create(obj, remote):
    remote: Remote = obj.remote
    params = dict(name='', codename='', description='')
    helpers.generic_edit_create(remote.kontr_client.courses.create, params)


@cli_courses.command('create', help='Create course')
@click.option('-N', '--name', prompt=True, required=False, help='Name')
@click.option('-n', '--codename', prompt=True, required=False, help='Codename')
@click.option('-d', '--description', prompt=True, required=False, help='Description')
def cli_courses_create(obj, remote, **kwargs):
    remote: Remote = obj.remote
    helpers.generic_create(remote.kontr_client.courses.create, **kwargs)


@cli_courses.command('select', help='Select course')
@click.argument('codename')
@click.pass_obj
def cli_courses_select(obj: AppConfig, remote, codename: str):
    remote: Remote = obj.remote
    print(f"\nSelecting course: {codename} for remote: {remote.name}\n")
    remote.selected_course = codename
    remote.update()
    obj.remotes.save()


@cli_courses.command('deselect', help='Select course')
@click.pass_obj
def cli_courses_deselect(obj: AppConfig, remote):
    remote: Remote = obj.remote
    print(f"\nDeselecting course for the remote: {remote.name}\n")
    del remote.selected_course
    remote.update()
    obj.remotes.save()


@cli_courses.command('is-token-read', help='Get IS MU token for a course')
@click.argument('codename')
@click.pass_obj
def cli_courses_is_token_read(obj: AppConfig, remote, codename: str):
    remote: Remote = obj.remote
    course: resources.Course = remote.kontr_client.courses[codename]
    token = course.read_is_api_token()
    print(f"Token: {token}")


@cli_courses.command('is-token-update', help='Set IS MU token for a course')
@click.argument('codename')
@click.argument('token')
@click.pass_obj
def cli_courses_is_token_update(obj: AppConfig, remote, codename: str, token):
    remote: Remote = obj.remote
    course: resources.Course = remote.kontr_client.courses[codename]
    course.update_is_api_token(token=token)
