# -*- coding: utf-8 -*-
import pkgutil

import click

import emoji

from story import cli

CHOICES = [
    'http',
    'every',
    'function',
    'if',
    'loop',
    'twitter',
    'slack-bot',
    'subscribe',
    'every',
    'websocket',
    '-',
]


@cli.cli.command()
@click.argument('story', default='-', type=click.Choice(CHOICES))
@click.argument(
    'output_file', default=None, type=click.Path(exists=False), required=False
)
def write(story, output_file=None):
    """Pre–defined Storyscripts for your app!"""

    # Support '$ story write http -` usecase.`
    if output_file == '-':
        output_file = None

    if story == '-':
        click.echo(click.style('Please specify a template:', bold=True))
        click.echo(
            click.style('  http', fg='cyan') + '      - serverless http')
        click.echo(
            click.style('  function', fg='cyan') + '  - generic function')
        click.echo(
            click.style('  if', fg='cyan') + '        - example if/then')
        click.echo(
            click.style('  loop', fg='cyan') + '      - example for loop')
        click.echo(click.style('  twitter', fg='cyan') + '   - stream Tweets')
        click.echo('')

        click.echo(
            click.style('Coming Soon',
                        bold=True) + ' (under active development):'
        )
        click.echo(click.style('  slack-bot', fg='cyan') + ' - Slack bot')
        click.echo(
            click.style('  subscribe', fg='cyan') + ' - event subscriptions')
        click.echo(
            click.style('  every', fg='cyan') + '     - periodically run this')
        click.echo(
            click.style('  websocket', fg='cyan') + ' - websocket support')
        click.echo('')

        click.echo(
            '  Run $ '
            + click.style('story write :template_name: ', fg='magenta')
            + emoji.emojize(':backhand_index_pointing_left:')
        )
        click.echo('')

        click.echo(click.style('Learn more:', bold=True))
        click.echo(
            '  - Examples: '
            + click.style('https://github.com/topics/storyscript-example',
                          fg='cyan')
        )
        click.echo(
            '  - Services: ' + click.style('https://hub.storyscript.io/',
                                           fg='cyan')
        )
        click.echo('')

    else:

        # Grab the story, from packaging...
        data = pkgutil.get_data('story', f'stories/{story}.story')

        # If output_file was passed, assume it was an interfactive session.
        if output_file:
            # Write to the file...
            with open(output_file, 'wb') as f:
                f.write(data)

            cmd = f'cat {output_file}'
            cmd = click.style(cmd, fg='magenta')
            click.echo(f'$ {cmd}', err=True)

        click.echo(data)

        app_name = cli.get_app_name_from_yml()
        if app_name is None:
            app_name = 'Not created yet'

        cli.track('App Bootstrapped',
                  {'App name': app_name, 'Template used': story})
