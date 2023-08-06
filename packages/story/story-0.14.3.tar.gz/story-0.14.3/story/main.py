# -*- coding: utf-8 -*-
import sys

try:
    from .cli import cli
    from .commands import *
except KeyboardInterrupt:
    print('Aborted!')
    sys.exit(1)

if __name__ == '__main__':
    try:
        cli()
    except KeyboardInterrupt:
        print('Aborted!')
        sys.exit(1)
