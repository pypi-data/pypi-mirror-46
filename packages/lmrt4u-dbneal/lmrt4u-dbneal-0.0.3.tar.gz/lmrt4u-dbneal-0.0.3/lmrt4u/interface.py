# -*- coding unix -*-

from __future__ import print_function

from PyInquirer import style_from_dict, Token, prompt, Separator

import sys
import os
import clint.arguments
import six
from datetime import datetime

sys.path.insert(0, os.path.abspath('..'))

from clint.textui import puts, indent, colored
from pyfiglet import figlet_format

try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None

def log(string, color, font="slant", figlet=False):
    """Prints string to console"""
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(
                string, font=font), color))
    else:
        six.print_(string)

def process_args(args):
    """Process console arguments"""
    input = {}
    if "Burndown" in args.all:
        input["activity"] = "Burndown Exit"
    else:
        print("Say somethin then")
    return input

def query():
    """Display lmrt4u console interface and collect user input."""
    args = clint.Args()
    if args:
        return process_args(args)

    style = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',  # default
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })

    questions = [
        {
            'type': 'list',
            'message': 'Select activity',
            'name': 'activity',
            'choices': [
                Separator('= Generate Artifacts='),
                'Burndown Chart',
                Separator('= Options ='),
                'Exit'
            ]
        }
    ]

    answer = prompt(questions, style=style)

    if (answer['activity'] == "Exit") : answer = None

    return answer

def initialize():
    """Prints program salutation to console."""
    log("LMRT4U", color="red", figlet=True)
    log("Let me help!", "green")
    return query()
