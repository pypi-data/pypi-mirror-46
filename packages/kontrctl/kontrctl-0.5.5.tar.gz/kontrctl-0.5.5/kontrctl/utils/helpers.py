import json
import sys
from typing import Dict

import click
import yaml
from kontr_api.resources import Course, Project
from tabulate import tabulate

from kontrctl import errors
from kontrctl.config import AppConfig, Remote


def get_remote(app_config: AppConfig, remote: str = None) -> Remote:
    """Gets remote instance
    Args:
        app_config(AppConfig): App config instance
        remote(str): Remote name
    Returns(Remote): Remote instance
    """
    remote = app_config.remotes[remote] if remote else app_config.remote
    if not remote:
        raise errors.RemoteNotSetError()
    return remote


def get_course(remote: Remote, course: str) -> Course:
    """Gets course based either by name or remote selected
    Args:
        remote(Remote): Remote instance
        course(str): Course name
    Returns(Course): Course instance
    """
    course_name = course or remote.selected_course
    return read_helper(remote.kontr_client.courses, course_name)


def get_project(remote: Remote, course: Course, project: str):
    """Gets project instance
    Args:
        remote(Remote): Remote instance
        course(Course): Course instance
        project(str): Project name

    Returns(Project): Project instance

    """
    project_name = project or remote.selected_project
    return read_helper(course.projects, project_name)


def get_user(remote: Remote, username: str = None):
    username = username or remote['username']
    if username is None:
        return remote.kontr_client.clients.me()
    return read_helper(remote.kontr_client.users, username)


def get_my_latest_submissions(remote: Remote) -> list:
    course = remote.selected_course
    project = remote.selected_project
    user = get_user(remote=remote)
    params = dict(user=user['username'])
    if course is not None:
        params['course'] = course
        if project is not None:
            params['project'] = project
    return remote.kontr_client.submissions.list(params=params)


def get_submission(remote: Remote, sid: str = None):
    if sid is not None:
        return read_helper(remote.kontr_client.submissions, sid)
    submissions = get_my_latest_submissions(remote)
    if not submissions:
        return None
    return submissions[-1]


def entity_printer(entity, output_format: str = 'text'):
    """Prints entity info
    Args:
        entity: Entity instance
        output_format(str): Format in which the entity will be printed (dict|json|text)
            (default: text)
    """
    if entity is None:
        return
    print(f"\n{entity.__class__.__name__} info:\n")
    config = entity.config
    if output_format == 'text' or output_format == 'yaml':
        dump = dump_yaml(config)
        print(dump)
    elif output_format == 'json':
        print(json.dumps(config))
    else:
        print(config)


def dump_yaml(config: Dict) -> str:
    try:
        return yaml.safe_dump(config, sort_keys=False)
    except TypeError:
        return yaml.safe_dump(config)


def edit_entity_using_editor(entity) -> dict:
    """Edits config using the editor
    Args:
        entity: Entity instance, should have config property
    Returns(dict): Updated dict
    """
    json_content = json.dumps(entity.config, indent=4)
    edited = click.edit(json_content)
    if edited is None:
        raise errors.ContentNotChangedError()
    update_dict = json.loads(edited)
    return update_dict


def read_helper(client, entity_name):
    entity = client.read(entity_name)
    if not entity:
        raise errors.ResourceNotFoundError(collection_name=client.__class__.__name__,
                                           name=entity_name)
    return entity


def generic_edit(client, entity_name):
    print(f"Editing {client.__class__.__name__}: {entity_name}")
    entity = read_helper(client=client, entity_name=entity_name)
    edit_and_update_entity(entity)


def edit_and_update_entity(entity):
    updated = edit_entity_using_editor(entity=entity)
    entity.update(updated)
    entity_printer(entity=entity)


def generic_read(client, name: str, output_format: str = 'text'):
    """Generic read function
    Args:
        client: Entity collection client instance
        name(str): Name of the entity
        output_format(str): Output format
    """
    entity = read_helper(client=client, entity_name=name)
    entity_printer(entity, output_format=output_format)


def generic_create(create, **params):
    print(f"Create user: {params}")
    result = create(params)
    print(f"Result: {result}")


def generic_edit_create(create, params):
    return None


def generic_add_client(client, codename, user, client_type=None):
    print(f"Adding client '{user}' from the {client.__class__.__name__} for {codename}")
    entity = read_helper(client, codename)
    entity.add_client(user, client_type=client_type)
    entity.read()
    entity_printer(entity)


def generic_add_users(client, codename, *users, client_type=None):
    print(f"Adding clients '{users}' from the {client.__class__.__name__} for {codename}")
    entity = read_helper(client, codename)
    entity.add_clients(*users, client_type=client_type)
    entity.read()
    entity_printer(entity)


def generic_remove_client(client, codename, user, client_type=None):
    print(f"Removing client '{user}' from the {client.__class__.__name__}: {codename}")
    entity = read_helper(client, codename)
    entity.remove_client(user, client_type=client_type)
    entity.read()
    entity_printer(entity)


def generic_remove_users(client, codename, users):
    print(f"Removing clients '{users}' from the {client.__class__.__name__}: {codename}")
    entity = read_helper(client, codename)
    entity.remove_clients(users)
    entity.read()
    entity_printer(entity)


def generic_add_project(client, codename, project):
    print(f"Adding project '{project}' from the {client.__class__.__name__} for {codename}")
    entity = read_helper(client, codename)
    entity.add_project(project)
    entity.read()
    entity_printer(entity)


def generic_add_projects(client, codename, *projects):
    print(f"Adding project '{projects}' from the {client.__class__.__name__} for {codename}")
    entity = read_helper(client, codename)
    entity.add_projects(*projects)
    entity.read()
    entity_printer(entity)


def generic_remove_project(client, codename, project):
    print(f"Remove project '{project}' from the {client.__class__.__name__}: {codename}")
    entity = read_helper(client, codename)
    entity.remove_project(project)
    entity.read()
    entity_printer(entity)


def generic_remove_projects(client, codename, *projects):
    print(f"Remove projects '{projects}' from the {client.__class__.__name__}: {codename}")
    entity = read_helper(client, codename)
    entity.remove_projects(*projects)
    entity.read()
    entity_printer(entity)


def generic_list_users(client, codename, name='users'):
    print(f"Listing users for {client.__class__.__name__}:  \"{codename}\"")
    entity = read_helper(client, codename)
    generic_list(entity[name], params=['id', 'codename', 'name'])


def generic_list_projects(client, codename):
    entity = read_helper(client, codename)

    def __trans(project: Project):
        return [project['id'], project['codename'], project['course']['codename']]

    headers = ['ID', 'CODENAME', 'COURSE']
    generic_list(entity['projects'], __trans, headers=headers)


def _print_ids(data):
    for item in data:
        print(item['id'])


def generic_list(data_list, params=None, options=None, t_func=None, headers=None):
    def __default_trans(item):
        res = []
        for param in params:
            key = param.split('.')
            elem = item
            if not isinstance(item, dict):
                elem = item.config
            res.append(nested_get(elem, key))
        return res

    if options and options['cols']:
        params = options['cols'].split(';')

    if not t_func:
        t_func = __default_trans
    if not headers:
        headers = [param.upper().replace('.', ' ') for param in params]

    data = data_transform(data_list, t_func)
    if options and (options['ids']):
        _print_ids(data_list)
        return
    format = 'simple' if not options or not options['t_format'] else options['t_format']

    print(tabulate(data, headers=headers, tablefmt=format))


def get_any_client(remote: Remote, user, worker):
    if user:
        return read_helper(remote.kontr_client.users, user)
    elif worker:
        return read_helper(remote.kontr_client.workers, worker)
    else:
        return remote.kontr_client.clients.me()


def data_transform(data_list, t_func):
    return [t_func(data) for data in data_list]


def nested_get(input_dict, nested_key):
    internal_dict_value = input_dict
    for k in nested_key:
        internal_dict_value = internal_dict_value.get(k, None)
        if internal_dict_value is None:
            return None
    return internal_dict_value


def filter_submissions(submissions, points=None, result=None, state=None, **kwargs):
    res = []
    for subm in submissions:
        if result and subm['result'] != result:
            continue
        if points and not eval(points, None, dict(p=subm['points'])):
            continue
        if state and subm['state'] != state:
            continue
        res.append(subm)
    return res


def input_read(def_file=None):
    if def_file is None:
        return sys.stdout.read()
    with open(def_file, 'r') as fd:
        return fd.read()
