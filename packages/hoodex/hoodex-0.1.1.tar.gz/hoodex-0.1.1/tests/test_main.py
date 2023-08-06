#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `main` package."""

import pytest
import os
import hoodex.main as hoodex_main


def test_load_config1_file():
    """Test load config1"""
    config_file = os.path.join("tests", "data", "configs", "config1.ini")
    hoodex_main.run_hoodex_loading_config_file(config_file)
    assert hoodex_main.PLEX_USER_NAME == "user1"
    assert hoodex_main.PLEX_PASSWORD == "password1"
    assert hoodex_main.PLEX_SERVER == "server1"
    assert hoodex_main.PLEX_LIBRARIES == "movies,tv"
