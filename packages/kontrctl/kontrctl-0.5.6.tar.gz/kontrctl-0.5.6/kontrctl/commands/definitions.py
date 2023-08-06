from typing import Dict

import click
import yaml

from kontrctl import errors
from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers

cli_definitions = click.Group('definition', help='Work with resource definitions')


@cli_definitions.command('dump-course', help='Get a course definition')
@click.argument('codename')
@click.pass_obj
def cli_course_dump(obj: AppConfig, codename: str):
    remote: Remote = obj.remote
    dump = remote.kontr_client.definitions.dump_course(codename).decode('utf-8')
    print(dump)


@cli_definitions.command('dump-project', help='Get a project definition')
@click.argument('course')
@click.argument('codename')
@click.pass_obj
def cli_project_dump(obj: AppConfig, course: str, codename: str):
    remote: Remote = obj.remote
    dump = remote.kontr_client.definitions.dump_project(course, codename).decode('utf-8')
    print(dump)


@cli_definitions.command('dump-role', help='Get a role definition')
@click.argument('course')
@click.argument('codename')
@click.pass_obj
def cli_role_dump(obj: AppConfig, course: str, codename: str):
    remote: Remote = obj.remote
    dump = remote.kontr_client.definitions.dump_role(course, codename).decode('utf-8')
    print(dump)


@cli_definitions.command('dump-group', help='Get a group definition')
@click.argument('course')
@click.argument('codename')
@click.pass_obj
def cli_group_dump(obj: AppConfig, remote, course: str, codename: str):
    remote: Remote = obj.remote
    dump = remote.kontr_client.definitions.dump_role(course, codename).decode('utf-8')
    print(dump)


@cli_definitions.command('sync-course', help='Sync a course using the definition')
@click.option('-f', '--definition', required=False, help='Definition file - if not provided, '
                                                         'stdout is used')
@click.pass_obj
def cli_course_sync(obj: AppConfig, definition=None):
    remote: Remote = obj.remote
    schema = helpers.input_read(definition)
    if not schema:
        print(f"No schema content provided")
    course = remote.kontr_client.definitions.sync_course(schema).decode('utf-8')
    helpers.entity_printer(course)


@cli_definitions.command('sync-project', help='Sync a project using the definition')
@click.option('-f', '--definition', required=False, help='Definition file - if not provided, '
                                                         'stdout is used')
@click.argument('course')
@click.pass_obj
def cli_project_sync(obj: AppConfig, definition=None, course=None):
    remote: Remote = obj.remote
    schema = helpers.input_read(definition)
    if not schema:
        print(f"No schema content provided")
        return
    course = remote.kontr_client.definitions.sync_project(course, schema)
    helpers.entity_printer(course)


@cli_definitions.command('sync-role', help='Sync a role using the definition')
@click.option('-f', '--definition', required=False, help='Definition file - if not provided, '
                                                         'stdout is used')
@click.argument('course')
@click.pass_obj
def cli_role_sync(obj: AppConfig, definition=None, course=None):
    remote: Remote = obj.remote
    schema = helpers.input_read(definition)
    if not schema:
        print(f"No schema content provided")
        return
    course = remote.kontr_client.definitions.sync_role(course, schema)
    helpers.entity_printer(course)


@cli_definitions.command('sync-group', help='Sync a group using the definition')
@click.option('-f', '--definition', required=False, help='Definition file - if not provided, '
                                                         'stdout is used')
@click.argument('course')
@click.pass_obj
def cli_group_sync(obj: AppConfig, remote, definition=None, course=None):
    remote: Remote = obj.remote
    schema = helpers.input_read(definition)
    if not schema:
        print(f"No schema content provided")
        return
    course = remote.kontr_client.definitions.sync_group(course, schema)
    helpers.entity_printer(course)


@cli_definitions.command('edit-course', help='Edit a course\'s definition')
@click.argument('codename')
@click.pass_obj
def cli_course_edit(obj: AppConfig, remote, codename: str = None):
    remote: Remote = obj.remote
    schema = remote.kontr_client.definitions.dump_course(codename).decode('utf-8')
    serialized = _edit_schema(schema)
    course = remote.kontr_client.definitions.sync_course(serialized)
    helpers.entity_printer(course)


@cli_definitions.command('edit-project', help='Edit a project\'s definition')
@click.argument('course')
@click.argument('codename')
@click.pass_obj
def cli_course_edit_project(obj: AppConfig, remote, codename: str = None, course=None):
    remote: Remote = obj.remote
    schema = remote.kontr_client.definitions.dump_project(course, codename).decode('utf-8')
    serialized = _edit_schema(schema)
    course = remote.kontr_client.definitions.sync_project(course, serialized)
    helpers.entity_printer(course)


@cli_definitions.command('edit-role', help='Edit a role\'s definition')
@click.argument('course')
@click.argument('codename')
@click.pass_obj
def cli_course_edit_role(obj: AppConfig, remote, codename: str = None, course=None):
    remote: Remote = obj.remote
    schema = remote.kontr_client.definitions.dump_role(course, codename).decode('utf-8')
    serialized = _edit_schema(schema)
    course = remote.kontr_client.definitions.sync_role(course, serialized)
    helpers.entity_printer(course)


@cli_definitions.command('edit-group', help='Edit a group\'s definition')
@click.argument('course')
@click.argument('codename')
@click.pass_obj
def cli_course_edit_group(obj: AppConfig, remote, codename: str = None, course=None):
    remote: Remote = obj.remote
    schema = remote.kontr_client.definitions.dump_group(course, codename).decode('utf-8')
    serialized = _edit_schema(schema)
    course = remote.kontr_client.definitions.sync_group(course, serialized)
    helpers.entity_printer(course)


def _edit_schema(schema: str) -> Dict:
    if not schema:
        print(f"No schema content provided")
    edited = click.edit(schema)
    if edited is None:
        raise errors.ContentNotChangedError()
    serialized = yaml.safe_load(edited)
    return serialized
