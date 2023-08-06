import click
import json

from typing import Dict

from kontrctl.commands.submission_files import cli_submission_files
from kontrctl.config import AppConfig, Remote
from kontrctl.utils import helpers


cli_submissions = click.Group('submissions', help='Submissions management')

cli_submissions.add_command(cli_submission_files)


def remove_none(**params) -> Dict:
    return {key: val for (key, val) in params.items() if val is not None}


@cli_submissions.command('list', help='List all submissions')
@click.option('-c', '--course', required=False, help='Sets course')
@click.option('-p', '--project', required=False, help='Sets project')
@click.option('-u', '--user', required=False, help='Sets user')
@click.option('-i', '--ids', required=False, is_flag=True, help='Get just ids')
@click.option('-s', '--state', required=False, help='Get submissions by state')
@click.option('-R', '--result', required=False, help='Get submissions by result')
@click.option('-P', '--points', required=False, help='Get points by expression (example: p > 3.0)')
@click.option('-C', '--cols', required=False, help='Show just provided columns, separator is ;')
@click.option('--t-format', required=False, help='Table formats (default simple), look at the tabular projects for more')
@click.pass_obj
def cli_submissions_list(obj: AppConfig, **kwargs):
    params = remove_none(**kwargs)
    remote: Remote = obj.remote
    submissions = remote.kontr_client.submissions.list(params=kwargs)
    params = ['id', 'created_at', 'result', 'points', 'state', 'user.username',
              'course.codename', 'project.codename']
    submissions = helpers.filter_submissions(submissions, **kwargs)
    helpers.generic_list(submissions, options=kwargs, params=params)


@cli_submissions.command('read', help='Get a submission info')
@click.argument('sid', required=False)
@click.pass_obj
def cli_submissions_read(obj: AppConfig, sid: str):
    remote: Remote = obj.remote
    submission = helpers.get_submission(remote, sid)
    if submission:
        helpers.entity_printer(submission)
    else:
        print("There are no submissions for you.")


@cli_submissions.command('stats', help='Get a submission stats')
@click.argument('sid', required=False)
@click.pass_obj
def cli_submissions_stats(obj: AppConfig, sid: str):
    remote: Remote = obj.remote
    submission = helpers.get_submission(remote, sid)
    if submission:
        print(json.dumps(submission.stats().json(), indent=4))
    else:
        print("There are no submissions for you.")


@cli_submissions.command('rm', help='Delete submission')
@click.argument('sid', required=False)
@click.pass_obj
def cli_submissions_delete(obj: AppConfig, sid: str):
    remote: Remote = obj.remote
    print(f"Removing submission: {sid}")
    submission = helpers.get_submission(remote, sid)
    submission.delete()


@cli_submissions.command('cancel', help='Cancel submission')
@click.argument('sid', required=False)
@click.pass_obj
def cli_submissions_cancel(obj: AppConfig, sid: str):
    remote: Remote = obj.remote
    print(f"Canceling submission: {sid}")
    submission = helpers.get_submission(remote, sid)
    submission.cancel()


@cli_submissions.command('resubmit', help='Resubmit submission')
@click.argument('sid', required=False)
@click.pass_obj
def cli_submissions_resubmit(obj: AppConfig, sid: str):
    remote: Remote = obj.remote
    print(f"Resubmitting submission: {sid}")
    submission = helpers.get_submission(remote, sid)
    submission.resubmit()
