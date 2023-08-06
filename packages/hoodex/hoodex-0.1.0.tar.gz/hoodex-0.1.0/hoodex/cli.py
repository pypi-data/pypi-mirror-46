# -*- coding: utf-8 -*-

"""Console script for hoodex."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for hoodex."""
    click.echo("Replace this message by putting your code into "
               "hoodex.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    sys.exit(0)


if __name__ == "__main__":
    main()
