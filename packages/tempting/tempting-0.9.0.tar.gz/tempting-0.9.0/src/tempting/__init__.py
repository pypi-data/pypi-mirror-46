# -*- coding: utf-8 -*-

"""Top-level package for tempting."""
import click
from pkg_resources import DistributionNotFound, get_distribution

__author__ = """Markus Binsteiner"""
__email__ = "markus@frkl.io"
__version__ = "0.1.0"

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()
