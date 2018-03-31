# -*- coding: utf-8 -*-
"""
Facilities that operate on raw JSON from the API.
"""
import json
from sty import fg, bg, ef, rs
from typing import Generator, Iterator

def print_tasks(self, tasksResponse: Generator[Iterator, None, None]):
    tasks = next(tasksResponse)
    if (tasks is None) or (len(tasks) == 0):
        print(C.WARNING + "No tasks to auto-archive. 😎" + C.RESET)
        return [], []
    else:
        newline()
        format_tasks(tasks)
        newline()

def format_tasks(tasks):
        for i, task in enumerate(tasks):
        # print("\n", json.dumps(task['fields'], indent=4), "\n") # 👈 For debugging
            if i > 0: # Don't pad first row
                newline()
            for k, v in task['fields'].items():
                format_attribute(k, v)

def format_attribute(k, v):
    keyStyle = C.HEADER
    valStyle = ''
    if k == 'Notes':
        return
    elif k == 'Status':
        status(k, v)
    elif k == 'Name':
        name(k, v)
    elif k == 'Link':
        link(k, v)
    else:
        generic_line(k, v)

def newline():
    print('')

def name(k, v):
    print(C.HEADER + k.title() + ": " + C.RESET, C.NAME + v + C.RESET)

def status(k, v):
    if v == 'Done':
        value_style = C.WHITE_ON_GREEN
    elif v == 'Auto-archived':
        value_style = C.STRIKE + C.WHITE_ON_BLUE
    else:
        value_style = C.NULL_STYLE
    print(C.HEADER + k + C.RESET, ": ", value_style + v + C.RESET)

def link(k, v):
    print(C.HEADER + k + C.RESET, ": ", C.LINK + v + C.RESET)

def generic_line(k, v):
    print(C.HEADER + k.title() + C.RESET, ": ", v)

class C:
    NULL_STYLE = ''
    BOLD = ef.bold
    FAIL = fg.magenta
    HEADER = fg(232, 209, 209) + ef.bold
    LINK = fg.blue + ef.underline
    NAME = fg.white + ef.bold
    WHITE_ON_BLUE = bg.blue + fg.white
    WHITE_ON_GREEN = bg.da_green + fg.white
    RESET = fg.green + bg.black + rs.italic + rs.bold + rs.underline + rs.strike
    STRIKE = ef.strike
    UNDERLINE = ef.underline
    WARNING = fg.red