import sys
import os
from datetime import datetime
import requests
import json
from pprint import pprint

if len(sys.argv) != 2:
  sys.exit("Usage: `python` " + sys.argv[0] + " <AIRTABLE_API_KEY>")
airtable_api_key = str(sys.argv[1])

tasks_table_root = 'https://api.airtable.com/v0/appiU1DE5MRcJwbMk/Table%201'

def fetch_stale_tasks(api_key):
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key}
    theFilter = "AND({Status}='',DATETIME_DIFF(TODAY(),{CreationTime},'days')>7)"
    data = {'filterByFormula':theFilter}

    response = requests.get(tasks_table_root, params=data, headers=headers)

    if response.status_code == requests.codes.ok:
        return json.loads(response.content)['records']
    else:
        print('No records found: [' + str(response.status_code) + ']:' + response.reason)

def auto_archive_task(task, api_key):
    data = {'fields': {'Status': 'Auto-archived', 'Auto-archive Date': datetime.now().isoformat()}}
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + airtable_api_key}

    response = requests.patch(tasks_table_root + '/' + task['id'], json=data, headers=headers)

    if response.status_code == requests.codes.ok:
        return json.loads(response.content)
    else:
        print('Auto-archive failed for task ' + task['id'] + '(' + task['Name'] + '): [' + str(response.status_code) + ']:' + response.reason)

def auto_archive_stale_tasks(): # -> (archived, failed)
    tasks = fetch_stale_tasks(airtable_api_key)
    if (tasks is None) or (len(tasks) == 0):
        print("No tasks to auto-archive. 😎")
        return [], []
    else:
        print("\n🐕 Fetched these stale tasks 🐕")
        pprint(tasks)
        print("🐕 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 🐕\n")

        archived = []
        failed = []
        print(task_id(tasks[0]) + ': ' + task_name(tasks[0]))
        auto = auto_archive_task(tasks[0], airtable_api_key)
        print(task_id(auto) + ': ' + task_name(tasks[0]))
        for task in tasks:
            auto_archive_response = auto_archive_task(task, airtable_api_key)
            if auto_archive_response is None:
                print("😭 Dang.")
                failed.append(task)
            else:
                print('Auto-archived 👉  ' + str(auto_archive_response))
                archived.append(auto_archive_response)
        return archived, failed

def task_id(task):
    return task['id']

def task_name(task):
    return task['fields']['Name']

def notify(title, text):
    # os.system("""
    #           osascript -e 'display notification "{}" with title "{}"'
    #           """.format(text, title))
    foo = """
          osascript -e 'display notification "{}" with title "{}"'
          """.format(text, title)
    print(foo)
    os.system(foo)

archived, failed = auto_archive_stale_tasks()

for a in archived:
    print(a)
    notify(task_name(a), '⚠️ Auto-Archived')

for f in failed:
    notify('🚨 Failed to auto-archive', task_name(f))
