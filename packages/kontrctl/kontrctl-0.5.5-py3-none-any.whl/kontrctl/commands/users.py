import click

from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers

cli_users = click.Group('users', help='Users management')


@cli_users.command('list', help='List all users')
@click.option('--ids', required=False, is_flag=True, help='Print just ids')
@click.option('--usernames', required=False, is_flag=True, help='Print just usernames')
@click.pass_obj
def cli_users_list(obj: AppConfig, ids, usernames):
    remote: Remote = obj.remote    
    users = remote.kontr_client.users.list()
    if ids or usernames:
        for user in users:
            if ids and usernames:
                print(f"{user['username']} {user['id']}")
            elif ids:
                print(user['id'])
            elif usernames:
                print(user['username'])
    else:
        params = ['id', 'username', 'email', 'uco']
        helpers.generic_list(users, params=params)


@cli_users.command('read', help='Get a user info')
@click.argument('username', required=False)
@click.pass_obj
def cli_users_read(obj: AppConfig, username: str):
    remote: Remote = obj.remote    
    user = helpers.get_user(remote, username=username)
    helpers.entity_printer(user)


@cli_users.command('rm', help='Delete user')
@click.argument('username')
@click.pass_obj
def cli_users_delete(obj: AppConfig, username: str):
    remote: Remote = obj.remote    
    print(f"Removing user: {username}")
    remote.kontr_client.users.delete(username)


@cli_users.command('create', help='Create user')
@click.option('-u', '--username', prompt=True, required=False, help='Username')
@click.option('-n', '--name', prompt=True, required=False, help='Name')
@click.option('-e', '--email', prompt=True, required=False, help='Email')
@click.option('-U', '--uco', prompt=True, required=False, help='Uco')
@click.option('-A', '--admin', is_flag=True, required=False, help='Is Admin?')
@click.pass_obj
def cli_users_create(obj, **kwargs):
    remote: Remote = obj.remote    
    helpers.generic_create(remote.kontr_client.users.create, **kwargs)


@cli_users.command('edit-create', help='Create users using editor')
@click.pass_obj
def cli_users_create_edit(obj):
    remote: Remote = obj.remote    
    params = {
        'username': '',
        'name': '',
        'email': '',
        'uco': '',
        'admin': False
    }
    helpers.generic_edit_create(remote.kontr_client.users.create, params)


@cli_users.command('edit', help='Edit user')
@click.argument('username')
@click.pass_obj
def cli_users_edit(obj: AppConfig, username: str):
    remote: Remote = obj.remote    
    helpers.generic_edit(remote.kontr_client.users, username)


@cli_users.command('set-password', help='Set password for the user')
@click.argument('username', required=False)
@click.pass_obj
def cli_users_update_password(obj: AppConfig, username: str):
    remote: Remote = obj.remote    
    user = helpers.get_user(remote, username)
    print(f"Updating password for {user['username']}")
    current = click.prompt('Current password', hide_input=True)
    new_password = click.prompt('New password', hide_input=True, confirmation_prompt=True)
    user.set_password(new=new_password, current=current)
