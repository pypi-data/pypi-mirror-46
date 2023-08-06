# -*- coding: utf-8 -*-

"""Plex module."""

import os
from plexapi.myplex import MyPlexAccount


class HoodexPlexServer(object):
    account = None
    server = None
    token = ""

    def __init__(self, user, password, server):
        self._connect_server(user=user, password=password, server=server)

    def _connect_server(self, user, password, server):
        print("Connecting to plex server {server} with user: {user}...".format(server=server, user=user))

        self.account = MyPlexAccount(user, password)
        self.server = self.account.resource(server).connect()
        self.token = self.account.resource(server).accessToken

    def get_last_added(self, library_name):
        media_list = []
        for media in self.server.library.section(library_name).recentlyAdded():
            local_path = media.locations[0]
            file_name = os.path.basename(local_path)
            media_list.append({
                "file_name": local_path,
                "name": file_name,
                "url": media.media[0].parts[0].key
            })

        return media_list
