# -*- coding: utf-8 -*-

"""Console script for hoodex."""
import sys
import click
from hoodex.main import run_hoodex_loading_config_file, run_hoodex


@click.command()
@click.option('--config', required=False, type=click.STRING, help='Config File.')
@click.option('--user', required=False, type=click.STRING, help='Plex User name.')
@click.option('--password', required=False, type=click.STRING, help='Plex password.')
@click.option('--server', required=False, type=click.STRING, help='Plex server.')
@click.option('--libraries', required=False, type=click.STRING, help='Plex libraries to scan.')
def main(config, user, password, server, libraries):
    """Console script for hoodex."""
    if config:
        run_hoodex_loading_config_file(config)
        run_hoodex()
    else:
        if None in (user, password, server, libraries):
            sys.exit("Missing Argument: you have to set user, password, server and libraries or a config file")
        else:
            run_hoodex(plex_user=user, plex_password=password, plex_server=server, plex_libraries=libraries)

    sys.exit(0)


if __name__ == "__main__":
    main()
