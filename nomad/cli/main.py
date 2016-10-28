# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import sys

import click

from .. import __version__

from .project import get_project

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler(sys.stderr)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', count=True)
@click.version_option(version=__version__)
@click.pass_context
def nomad(ctx, verbose):
    """ Orchestrate and run multiple containers using LXD. """
    # Handles vertbosity
    if verbose:
        console_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.INFO)

    # Initializes the project and store it in the commands' shared context
    ctx.obj['project'] = get_project()


@nomad.command()
@click.pass_context
def up(ctx, **kwargs):
    """ Create, start and provisions containers. """
    ctx.obj['project'].up()


@nomad.command()
@click.pass_context
def halt(ctx, **kwargs):
    """ Stop containers. """
    ctx.obj['project'].halt()


@nomad.command()
@click.pass_context
def destroy(ctx, **kwargs):
    """ Stop and remove containers. """
    ctx.obj['project'].destroy()


@nomad.command()
@click.pass_context
def provision(ctx, **kwargs):
    """ Provision containers. """
    ctx.obj['project'].provision()


def main():
    # Setup logging
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG)
    # Disables requests logging
    logging.getLogger('requests').propagate = False
    # Executes LXD-Nomad!
    nomad(obj={})
