import click

from kontrctl import errors
from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers
from kontrctl.utils.helpers import entity_printer


@click.group('remotes', help='Manages remotes')
def cli_remotes():
    pass


@cli_remotes.command('add', help='Adds remote')
@click.argument('name', default='default')
@click.argument('url')
@click.pass_obj
def cli_remotes_add(obj: AppConfig, name, url):
    config = {}
    obj.remotes.add(name, url, **config)
    obj.remotes.save()


@cli_remotes.command('rm', help='Removes remote')
@click.argument('name')
@click.pass_obj
def cli_remotes_rm(obj: AppConfig, name: str):
    obj.remotes.delete(name)
    obj.remotes.save()


@cli_remotes.command('read', help='Reads remote')
@click.option('--output-format', default="text", help="Output format: (json|text|dict)")
@click.argument('name')
@click.pass_obj
def cli_remotes_read(obj: AppConfig, name: str, output_format):
    remote = obj.remotes[name]
    if remote is None:
        raise errors.ResourceNotFoundError(collection_name=remote.__class__.__name__, name=name)
    entity_printer(remote, output_format=output_format)


@cli_remotes.command('list', help='List remotes')
@click.pass_obj
def cli_remotes_list(obj: AppConfig):
    helpers.generic_list(obj.remotes.list(), params=['name', 'url'])


@cli_remotes.command('select', help='Selects remote')
@click.argument('name')
@click.pass_obj
def cli_select_remote(obj: AppConfig, name: str):
    obj.config.default_remote = name
    obj.save()


@cli_remotes.command('edit', help='Edit remotes info')
@click.argument('name')
@click.pass_obj
def cli_remote_edit(obj: AppConfig, name: str):
    remote: Remote = helpers.get_remote(obj, name)
    update_dict = helpers.edit_entity_using_editor(remote)
    if update_dict is not None:
        remote.config.update(update_dict)
        remote.update()
    print(update_dict)
