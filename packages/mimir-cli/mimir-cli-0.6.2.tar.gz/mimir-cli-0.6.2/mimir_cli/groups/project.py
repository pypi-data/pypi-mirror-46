"""
project related commands
"""
import click
from mimir_cli.utils.submit import submit_to_mimir
from mimir_cli.utils.projects import (
    get_projects_list,
    print_projects,
    prompt_for_project,
)


@click.group()
def project():
    """project related commands"""
    pass


@project.command()
@click.option(
    "--path",
    help="the file or directory to submit",
    prompt=True,
    type=click.Path(exists=True, file_okay=True, dir_okay=True, resolve_path=True),
    metavar="<file path>",
)
@click.option(
    "--project-id",
    help="the project id on Mimir Classroom",
    type=click.UUID,
    metavar="<uuid>",
)
@click.option(
    "--force",
    help="force the submission even if files are missing",
    is_flag=True,
    default=False,
)
@click.option(
    "--on-behalf-of",
    help="email to submit on behalf of (instructor only)",
    type=str,
    metavar="<email>",
)
@click.option(
    "--custom-penalty",
    help="custom penalty for the submission (instructor only)",
    type=float,
    default=0.0,
    show_default=True,
    metavar="<float>",
)
def submit(path, project_id, on_behalf_of, custom_penalty, force):
    """
    submit files to a project on Mimir Classroom.

    \b
    if you are logged in as an instructor,
    you can also submit on behalf of another user,
    denoted by email, optionally adding a custom penalty
    """
    if not project_id:
        projects = get_projects_list()
        selected_project = prompt_for_project(projects)
        project_id = selected_project["id"]
    submit_to_mimir(
        path,
        project_id,
        on_behalf_of=on_behalf_of,
        custom_penalty=custom_penalty,
        forced=force,
    )


@project.command()
@click.option(
    "-l",
    "--limit",
    default=20,
    help="maximum number of projects to show",
    show_default=True,
    metavar="<int>",
)
@click.option(
    "-v",
    "--verbose",
    help="show more information about the projects",
    is_flag=True,
    default=False,
)
def ls(limit, verbose):
    """list open projects for this account on Mimir Classroom"""
    projects = get_projects_list()[:limit]
    print_projects(projects, verbose=verbose)
