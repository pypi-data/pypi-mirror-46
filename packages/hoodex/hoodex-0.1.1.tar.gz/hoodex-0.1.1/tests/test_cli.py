#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cli` package."""

import pytest
import os

from click.testing import CliRunner

from hoodex import cli


def test_command_line_interface_without_parameters():
    """Test the CLI without parameters"""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 1
    assert "Missing Argument:" in result.exception.args[0]


def test_command_line_interface_help():
    """Test the CLI with --help parameter"""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--config' in help_result.output
    assert '--user' in help_result.output
    assert '--password' in help_result.output
    assert '--server' in help_result.output
    assert '--server' in help_result.output
    assert '--help' in help_result.output


def test_command_line_interface_config_missing_file():
    """Test the CLI with --config parameter"""
    runner = CliRunner()
    config_result = runner.invoke(cli.main, ['--config=missing.ini'])
    assert config_result.exit_code == 1
    assert 'Missing File:' in config_result.output


def test_command_line_interface_config_error():
    """Test the CLI with --config parameter without file"""
    runner = CliRunner()
    config_result = runner.invoke(cli.main, ['--config'])
    assert config_result.exit_code == 2
    assert 'Error: --config option requires an argument' in config_result.output
