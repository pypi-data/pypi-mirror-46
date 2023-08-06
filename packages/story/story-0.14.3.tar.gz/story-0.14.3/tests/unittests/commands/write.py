# -*- coding: utf-8 -*-
from click.testing import CliRunner

from pytest import fixture

from story.main import cli


@fixture
def runner():
    return CliRunner()


def test_choose_template(runner):
    res = runner.invoke(cli, ['write'])
    assert res.exit_code == 0
    assert 'Please specify a template' in res.output
