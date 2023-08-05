"""
logical groups for commands
"""
from mimir_cli.groups.auth import login, logout
from mimir_cli.groups.project import project

GROUPS = [login, logout, project]
