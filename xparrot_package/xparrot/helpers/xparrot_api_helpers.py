# -*- coding: utf-8 -*-
"""
Facilities that operate on raw JSON from the API.
"""
import json
from typing import Generator, Iterator

def print_tasks(self, tasksResponse: Generator[Iterator, None, None]):
    tasks = next(tasksResponse)
    if (tasks is None) or (len(tasks) == 0):
        print(C.WARNING + "No tasks to auto-archive. 😎" + C.ENDC)
        return [], []
    else:
        for task in tasks:
            print('\n〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰')
            # print("\n", json.dumps(task['fields'], indent=4), "\n")
            for k, v in task['fields'].items():
                keyStyle = C.HEADER
                valStyle = ''
                if k == 'Notes':
                    continue
                elif k == 'Status':
                    valStyle = C.OKGREEN
                    if v == 'Auto-archived':
                        valStyle = C.UNDERLINE + C.OKBLUE
                elif k == 'Name':
                    valStyle = C.BOLD
                else:
                    print(C.HEADER + k.title() + C.ENDC, ": ", v)
                    continue

                print(C.HEADER + k.title() + C.ENDC, ": ", valStyle + v + C.ENDC)

            print('〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰\n')

class C:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
