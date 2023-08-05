# Storyscript CLI

<!-- [![Requires.io](https://img.shields.io/requires/github/storyscript/cli.svg?style=flat-square)](https://requires.io/github/storyscript/cli/requirements/?branch=master)  -->
[![CircleCI](https://img.shields.io/circleci/project/github/storyscript/cli.svg?style=flat-square)](https://circleci.com/gh/storyscript/cli)
[![Codecov](https://img.shields.io/codecov/c/github/storyscript/cli.svg?style=flat-square)](https://codecov.io/gh/storyscript/cli)
[![PyPI](https://img.shields.io/pypi/v/story.svg?style=flat-square)](https://pypi.org/project/story/)
<!-- [![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fstoryscript%2Fcli.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fstoryscript%2Fcli?ref=badge_shield) -->

The Storyscript CLI is used to manage Storyscript Cloud from the command line.

## Overview

The goals of this project is to provide a utility for developers to interact with all of Storyscript Cloud features/services.

## Installation

```shell
$ brew install storyscript/brew/story
```

✨🍰✨

## Usage

Call `story` to get a full list of commands or continue to [read the documentation](https://docs.storyscript.io/cli).

![usage](https://github.com/storyscript/cli/blob/e7c2dc8f4b1de08163e94db16219a90fdb1d7d6b/ext/story-cli.png?raw=true)

## Issues

For problems directly related to the CLI, [add an issue on GitHub](https://github.com/storyscript/cli/issues/new).

For other issues, [submit a support ticket](mailto:support@asyncy.com)

[Contributors](https://github.com/storyscript/cli/contributors)

## Developing

Run
```sh
virtualenv venv --python=python3.7 && source venv/bin/activate
pip install -r requirements.txt

TOXENV=true python -m story.main
```

Test
```sh
pip install tox
tox
```

Install
```sh
python setup.py install
story
```


<!-- ## License -->
<!-- [![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fstoryscript%2Fcli.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fstoryscript%2Fcli?ref=badge_large) -->
