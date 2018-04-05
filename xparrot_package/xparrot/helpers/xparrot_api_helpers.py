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
        print(C.WARNING + "No tasks match your request. 😎" + C.RESET)
        return [], []
    else:
        newline()
        format_tasks(tasks)
        newline()


def format_tasks(tasks):
    for i, task in enumerate(tasks):
        print_task(task, i)


def print_task(task, i=0):
    # print("\n", json.dumps(task['fields'], indent=4), "\n") # 👈 For debugging
    if i > 0:  # Don't pad first row
        newline()
    for k, v in task['fields'].items():
        format_task_attribute(k, v)
    generic_line('id', task['id'])


def format_task_attribute(k, v):
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


def print_projects(self, projectsResponse: Generator[Iterator, None, None]):
    projects = next(projectsResponse)
    if (projects is None) or (len(projects) == 0):
        print(C.WARNING + "No projects match your request. 😎" + C.RESET)
        return [], []
    else:
        newline()
        format_projects(projects)
        newline()


def format_projects(projects):
    for i, project in enumerate(projects):
        # print("\n", json.dumps(task['fields'], indent=4), "\n") # 👈 For debugging
        if i > 0:  # Don't pad first row
            newline()
        for k, v in project['fields'].items():
            format_project_attribute(k, v)


def format_project_attribute(k, v):
    if k == 'xParrot':
        count('Tasks', v)
    elif k == 'Subprojects' or k == 'Archive':
        count(k, v)
    elif k == 'Name':
        name(k, v)
    else:
        generic_line(k, v)


def format_subprojects(subprojects):
    for i, subproject in enumerate(subprojects):
        # print("\n", json.dumps(task['fields'], indent=4), "\n") # 👈 For debugging
        if i > 0:  # Don't pad first row
            newline()
        for k, v in subproject['fields'].items():
            format_subproject_attribute(k, v)


def print_subprojects(self,
                      subprojectsResponse: Generator[Iterator, None, None]):
    subprojects = next(subprojectsResponse)
    if (subprojects is None) or (len(subprojects) == 0):
        print(C.WARNING + "No projects match your request. 😎" + C.RESET)
        return [], []
    else:
        newline()
        format_subprojects(subprojects)
        newline()


def format_subproject_attribute(k, v):
    if k == 'xParrot':
        count('Tasks', v)
    elif k == 'Archive':
        count(k, v)
    elif k == 'Name':
        name(k, v)
    else:
        generic_line(k, v)


def newline():
    print('')


def name(k, v):
    print(format_label(k), C.NAME + v + C.RESET)


def status(k, v):
    if v == 'Done':
        value_style = C.WHITE_ON_GREEN
    elif v == 'Auto-archived':
        value_style = C.STRIKE + C.WHITE_ON_BLUE
    else:
        value_style = C.NULL_STYLE
    print(format_label(k), value_style + v + C.RESET)


def count(k, v):
    print(format_label(k), len(v))


def link(k, v):
    print(format_label(k), C.LINK + v + C.RESET)


def generic_line(k, v):
    print(format_label(k.title()), v, C.RESET)


def format_label(k):
    return C.HEADER + k + ": " + C.RESET


class C:
    NULL_STYLE = ''
    FAIL = fg.magenta
    HEADER = fg(232, 209, 209) + ef.faint
    LINK = fg.blue + ef.underline
    NAME = fg.white
    WHITE_ON_BLUE = bg.blue + fg.white
    WHITE_ON_GREEN = bg.da_green + fg.white
    RESET = fg.green + bg.black + rs.italic + rs.underline + rs.strike + rs.faint
    STRIKE = ef.strike
    UNDERLINE = ef.underline
    WARNING = fg.red