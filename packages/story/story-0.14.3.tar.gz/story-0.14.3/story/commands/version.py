# -*- coding: utf-8 -*-

import click

from .. import cli


@cli.cli.command()
def version():
    """Displays the Storyscript CLI & Compiler versions."""
    from storyscript import version

    click.echo(
        click.style('Storyscript CLI', fg='magenta')
        + ': v'
        + cli.version
        + click.style(', ', dim=True)
        + click.style('Storyscript Compiler', fg='cyan')
        + ': v'
        + version
        + '.'
    )
