"""
state store for the click application
"""
import click
import json
import sys


class State:
    """state object for click"""

    def __init__(self):
        """constructor"""
        self.verbose = False
        self.api = "https://class.mimir.io"


def get_state():
    """gets the current state of the click app"""
    return click.get_current_context().ensure_object(State)


def debug(text):
    """only prints if verbose mode is on"""
    state = get_state()
    if state.verbose:
        if isinstance(text, dict):
            text = json.dumps(text, indent=2, sort_keys=True, default=str)
        click.echo(click.style(text, fg="green"), err=True)


def api_login_url():
    """forms the login url"""
    state = get_state()
    return "{api}/lms/user_sessions".format(api=state.api)


def api_submit_url(project_id):
    """forms the submit url"""
    state = get_state()
    return "{api}/lms/projects/{project_id}/project_submissions".format(
        api=state.api, project_id=project_id
    )


def api_view_submission_url(submission_id):
    """forms the view submission url"""
    state = get_state()
    return "{api}/project_submissions/{submission_id}".format(
        api=state.api, submission_id=submission_id
    )


def api_projects_url():
    """forms the list projects url"""
    state = get_state()
    return "{api}/lms/projects".format(api=state.api)


def error_out(text, exit_code=1):
    """error out of the cli, throwing exit_code"""
    debug("\n[X] error_out with exit code {}".format(exit_code))
    click.echo("\nERROR:\n{}\n".format(text))
    sys.exit(exit_code)
