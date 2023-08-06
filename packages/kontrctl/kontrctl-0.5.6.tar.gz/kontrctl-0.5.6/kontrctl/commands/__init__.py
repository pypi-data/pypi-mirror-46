from kontrctl.commands.logs import cli_logs
from .definitions import cli_definitions
from .auth import cli_login, cli_logout
from .courses import cli_courses
from .groups import cli_groups
from .general import cli_info
from .permissions import cli_permissions
from .project_configs import cli_project_configs
from .projects import cli_projects
from .remotes import cli_remotes
from .roles import cli_roles
from .secrets import cli_secrets
from .submit import cli_submit
from .submission_files import cli_submission_files
from .submissions import cli_submissions
from .users import cli_users
from .workers import cli_workers
from .execute import cli_shell


def add_all_commands(main_command):
    main_command.add_command(cli_remotes)
    main_command.add_command(cli_login)
    main_command.add_command(cli_logout)
    main_command.add_command(cli_users)
    main_command.add_command(cli_workers)
    main_command.add_command(cli_courses)
    main_command.add_command(cli_projects)
    main_command.add_command(cli_roles)
    main_command.add_command(cli_groups)
    main_command.add_command(cli_submit)
    main_command.add_command(cli_submissions)
    main_command.add_command(cli_permissions)
    main_command.add_command(cli_secrets)
    main_command.add_command(cli_info)
    main_command.add_command(cli_shell)
    main_command.add_command(cli_definitions)
    main_command.add_command(cli_logs)

