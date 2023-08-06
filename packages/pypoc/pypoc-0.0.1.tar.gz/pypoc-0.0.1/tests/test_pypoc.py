#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pypoc` package."""

import sys
import pytest
import pypoc

#from click.testing import CliRunner
#from pypoc import click


def test_pypoc_imported():
	"""Sample test, will always pass so long as import statement worked"""
	assert "pypoc" in sys.modules


if __name__ == "__main__":
        test_pypoc_imported()


#@pytest.fixture
#def response():
    #"""Sample pytest fixture.
    #
    #See more at: http://doc.pytest.org/en/latest/fixture.html
    #"""
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


#def test_content(response):
	#"""Sample pytest test function with the pytest fixture as an argument."""
	# from bs4 import BeautifulSoup
	# assert 'GitHub' in BeautifulSoup(response.content).title.string


#def test_command_line_interface():
	#"""Test the CLI."""
	#runner = CliRunner()
	#result = runner.invoke(click.main)
	#assert result.exit_code == 0
	#assert 'pypoc.click.main' in result.output
	#help_result = runner.invoke(click.main, ['--help'])
	#assert help_result.exit_code == 0
	#assert '--help  Show this message and exit.' in help_result.output
