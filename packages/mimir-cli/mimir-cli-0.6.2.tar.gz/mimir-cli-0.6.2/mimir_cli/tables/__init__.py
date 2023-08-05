"""
tables vendor submodule
"""
import click
import os
from mimir_cli.tables.ascii_table import AsciiTable  # noqa


os.environ["LESS"] = "-S"


def echo_table(table_data, title="", column_limit=-1):
    """
    takes in a table and will click echo it
    :param table_data: a list of lists for the table
    """
    if column_limit > 0:
        table_data = [x[:column_limit] for x in table_data]

    table = AsciiTable(table_data, title=title)
    table_width = len(table.table.split("\n")[0])
    term_width = click.get_terminal_size()[0]
    if table_width > term_width:
        click.echo_via_pager(table.table)
    else:
        click.echo(table.table)
