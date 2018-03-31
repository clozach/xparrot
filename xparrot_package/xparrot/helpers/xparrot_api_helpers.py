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
        for task in tasks:
            print_record_boundary()
            # print("\n", json.dumps(task['fields'], indent=4), "\n")
            for k, v in task['fields'].items():
                keyStyle = C.HEADER
                valStyle = ''
                if k == 'Notes':
                    continue

                elif k == 'Status':
                    status(k, v)
                        
                elif k == 'Name':
                    name(k, v)

                elif k == 'Link':
                    link(k, v)

                else:
                    generic_line(k, v)

            print_record_boundary()

def print_record_boundary():
    print(C.BASE + '\n〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰' + C.RESET) 

def name(k, v):
    print(C.HEADER + k.title() + C.BASE, ": ", C.NAME + v + C.BASE)

def status(k, v):
    value_style = C.OKGREEN #Default
    if v == 'Auto-archived':
        value_style = C.STRIKE + C.OKBLUE
    print(C.HEADER + k + C.BASE, ": ", value_style + v + C.BASE)

def link(k, v):
    print(C.HEADER + k + C.BASE, ": ", C.LINK + v + C.BASE)

def generic_line(k, v):
    print(C.HEADER + k.title() + C.BASE, ": ", v)

class C:
    BASE = fg(90, 90, 90) + bg(32, 32, 32) + rs.underline
    BOLD = ef.bold
    FAIL = fg.magenta
    HEADER = fg(232, 209, 209) + ef.bold
    LINK = fg.blue + ef.underline
    NAME = fg.white + ef.bold
    OKBLUE = bg.blue + fg.white
    OKGREEN = bg.da_green + fg.white
    RESET = fg.rs + bg.rs + rs.italic + rs.bold + rs.underline + rs.strike
    STRIKE = ef.strike
    UNDERLINE = ef.underline
    WARNING = fg.red