"""
auth related commands
"""
import click
from mimir_cli.utils.auth import login_to_mimir, logout_of_mimir
from mimir_cli.strings import (
    AUTH_SUCCESS,
    EMAIL_HELP,
    ERR_INVALID_CRED,
    LOGOUT_SUCCESS,
    PW_HELP,
)


@click.command()
@click.option("-e", "--email", help=EMAIL_HELP, metavar="<email>")
@click.option("-p", "--password", help=PW_HELP, metavar="<string>")
def login(email, password):
    """
    log in to Mimir Classroom.

    \b
    You need to specify:
    - email and password; via either options or prompts
    """
    while not email:
        email = click.prompt("Email", type=str)
    while not password:
        password = click.prompt("Password", type=str, hide_input=True)
    logged_in = login_to_mimir(email, password)
    if logged_in:
        click.echo(AUTH_SUCCESS)
        return True
    click.echo(ERR_INVALID_CRED)
    return False


@click.command()
def logout():
    """log out of Mimir Classroom."""
    logout_of_mimir()
    click.echo(LOGOUT_SUCCESS)
