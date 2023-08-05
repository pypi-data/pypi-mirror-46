"""
the main mimir cli click module
"""
import click
import requests
import sys
from mimir_cli.globals import __version__
from mimir_cli.utils.state import State, debug
from mimir_cli.groups import GROUPS


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click.option("-v", "--verbose", is_flag=True, default=False, hidden=True)
@click.option("-a", "--api", default="https://class.mimir.io", hidden=True)
def cli(ctx, verbose, api):
    """Mimir Classroom CLI"""
    state = ctx.ensure_object(State)
    state.verbose = verbose
    state.api = api
    debug("[+] verbose mode enabled")


@cli.command()
def version():
    """print version info"""
    click.echo("mimir-cli {cli}".format(cli=__version__))
    debug(
        "click {click}\n"
        "requests {requests}\n"
        "python {python}".format(
            click=click.__version__, requests=requests.__version__, python=sys.version
        )
    )


for group in GROUPS:
    cli.add_command(group)


if __name__ == "__main__":
    cli()  # noqa
