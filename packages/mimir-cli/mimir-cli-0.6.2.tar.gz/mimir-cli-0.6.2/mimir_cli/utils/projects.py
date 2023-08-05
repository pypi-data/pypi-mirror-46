"""
project related utility functions
"""
import click
import json
from mimir_cli.strings import PROJECT_PROMPT
from mimir_cli.tables import echo_table
from mimir_cli.utils.auth import get
from mimir_cli.utils.io import date_fmt, parse_iso_date
from mimir_cli.utils.state import debug, api_projects_url, error_out


def print_projects(projects, verbose=False):
    """print a list of projects in a nice way"""
    table_data = [
        [
            "#",
            "project name",
            "limit",
            "due date",
            "course name",
            "cooldown",
            "project id",
        ]
    ]
    table_data += [
        [
            index,
            p["name"],
            "∞"
            if p["unlimitedSubmissions"]
            else "{} left".format(p["submissionsLeft"]),
            date_fmt(parse_iso_date(p["realDueDate"])),
            p["courseName"],
            "{} {}".format(p["cooldownDuration"], p["cooldownDurationUnit"])
            if p["enableCooldown"]
            else "",
            p["id"],
        ]
        for index, p in enumerate(projects)
    ]
    echo_table(table_data, column_limit=-1 if verbose else 4)


def get_projects_list():
    """gets the projects list for a user, sorted by due date"""
    projects_request = get(api_projects_url())
    if projects_request.status_code == 401:
        error_out("project ls failed: unauthorized - please try logging back in!")
    result = json.loads(projects_request.text)
    debug(result)
    sorted_projects = sorted(
        result["projects"], key=lambda x: parse_iso_date(x["realDueDate"])
    )
    return sorted_projects


def prompt_for_project(projects):
    """prompts for which project"""
    print_projects(projects)
    choice = click.prompt(PROJECT_PROMPT, type=int, default=0)
    return projects[choice]
