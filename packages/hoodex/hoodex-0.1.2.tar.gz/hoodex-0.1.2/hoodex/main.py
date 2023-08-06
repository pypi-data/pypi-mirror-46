# -*- coding: utf-8 -*-

"""Main module."""

import configparser
import os
import sys

from hoodex.plex import HoodexPlexServer

PLEX_USER_NAME = ""
PLEX_PASSWORD = ""
PLEX_SERVER = ""
PLEX_LIBRARIES = ""


def run_hoodex_loading_config_file(config_file):
    print("Loading config file: {config}".format(config=config_file))
    if not os.path.isfile(config_file):
        sys.exit("Missing File: Unable to find config file {config_file}".format(config_file=config_file))
    global PLEX_USER_NAME, PLEX_PASSWORD, PLEX_SERVER, PLEX_LIBRARIES
    config = configparser.ConfigParser()
    config.read(filenames=config_file)

    if config.items('hoodex') is None:
        sys.exit(
            "Bad Configuration: Config file {config_file} has missing hoodex section".format(config_file=config_file))
    elif all(keys in ('PlexUserName', 'PlexPassword', 'PlexServer', 'PlexLibraries') for keys in config['hoodex']):
        sys.exit("Bad Configuration: Config file {config_file} has some missing keys".format(config_file=config_file))

    PLEX_USER_NAME = config['hoodex']['PlexUserName']
    PLEX_PASSWORD = config['hoodex']['PlexPassword']
    PLEX_SERVER = config['hoodex']['PlexServer']
    PLEX_LIBRARIES = config['hoodex']['PlexLibraries']


def run_hoodex(plex_user=None, plex_password=None, plex_server=None, plex_libraries=None):
    if plex_user is None:
        plex_user = PLEX_USER_NAME
    if plex_password is None:
        plex_password = PLEX_PASSWORD
    if plex_server is None:
        plex_server = PLEX_SERVER
    if plex_libraries is None:
        plex_libraries = PLEX_LIBRARIES

    plex_server = HoodexPlexServer(user=plex_user, password=plex_password, server=plex_server)

    libraries_dict = {}

    for library in str.split(str(plex_libraries), ','):
        libraries_dict[library] = plex_server.get_last_added(library_name=library)

    print(libraries_dict)

    return libraries_dict
