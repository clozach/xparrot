# -*- coding: utf-8 -*-
"""
Facilities that operate on raw JSON from the API.
"""
import json
from typing import Generator, Iterator

def print_tasks(self, tasksResponse: Generator[Iterator, None, None]):
    tasks = next(tasksResponse)
    if (tasks is None) or (len(tasks) == 0):
        print("No tasks to auto-archive. 😎")
        return [], []
    else:
        for task in tasks:
            print('\n〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰')
            # print("\n", json.dumps(task['fields'], indent=4), "\n")
            for k, v in task['fields'].items():
                if k == 'Notes': continue
                print(k.upper(), ": ", v)
            print('〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰〰\n')