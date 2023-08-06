#!/usr/bin/env python
# coding: utf-8

from argparse import ArgumentParser

parsers = ArgumentParser(
    usage = 'pypydata [-l]',
    description = "Location list PypyData"
    )

parsers.add_argument(
    "-l",
    action="store_true",
    default=False,
    help="You can see lists of all PypyData location."
    )

# parsers.add_argument(
#     "-o",
#     action="store",
#     nargs=1,
#     help="You can see lists of PyData organizer."
#     )