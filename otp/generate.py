#!/usr/bin/env python
# -*- mode: python; coding: utf-8;  -*-

"""
Generate files for OTP assignment.
"""

__author__ = "Breanndán Ó Nualláin"
__author_email__ = "<o@uva.nl>"

from otp import generate_team_files
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("book_file", type=str, help="file containing book")
parser.add_argument("teams", type=int, help="number of teams")
parser.add_argument(
    "blocks", type=int, nargs="?", default=2, help="number of blocks per team"
)

args = parser.parse_args()

for team in range(args.teams):
    generate_team_files(team, args.book_file, args.blocks)
