#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import argparse
import sys
try:
    from .version import __version__
except ImportError:
    from version import __version__

class params:
    pass

def parse():
    p = params()
    parser = argparse.ArgumentParser('auto_check', description='A script for checking in & out automatically, which is just for fun ^_^.',)

    # parser = argparse.ArgumentParser(
    #     prog='自动打卡签到',
    #     #usage='python3 __main__.py [OPTION]... URL...',
    #
    #     add_help=False,
    # )

    parser.add_argument(
        '-v', '--version', action='store_true',
        help='print version and exit'
    )

    run_grp = parser.add_argument_group(
        'Run options'
    )
    run_grp.add_argument(
        '-c', '--config_dir', action='store', default='',
        help='the config files\' directory path'
    )
    run_grp.add_argument(
        '-u', '--url', action='store', default='',
        help='the url which used to get conf'
    )
    run_grp.add_argument(
        '-s', '--suffix', action='store', default='',
        help='run the config ending with the specific suffix'
    )
    run_grp.add_argument(
        '-t', '--test', action='store_true',
        help='set to test mode, aka not perform checking in or out'
    )
    run_grp.add_argument(
        '-i', '--immediately', action='store_true',
        help='perform checking in or out with random delay'
    )
    run_grp.add_argument(
        '-f', '--force', action='store_true',
        help='force to check out, but only works after 6:00 pm'
    )
    args = parser.parse_args(sys.argv[1:], namespace=p)

    if args.version:
        print('Auto Checker v{0}'.format(__version__))
        sys.exit()

    return p
