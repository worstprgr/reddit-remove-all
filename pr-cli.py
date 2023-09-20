#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import argparse
from postremover import PostRemover

help_user = 'Your username on Reddit'
help_mode = 'Choose between delete posts(p) or comments(c)'
help_browser = 'Choose between Firefox(F) or Chrome(C)'
description = 'Example command: pr-cli.py stevetest C'

parser = argparse.ArgumentParser(description=description)
parser.add_argument('username', help=help_user)
parser.add_argument('mode', help_mode)
parser.add_argument('browser', help=help_browser)
args = parser.parse_args()

postRemover = PostRemover(args.username, args.mode, args.browser)
postRemover.deletePost()
