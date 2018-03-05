import sys
import os
from datetime import datetime
import requests
import json
from pprint import pprint

days_til_endangered = 5
days_til_stale = 7
hours_til_expiry = 18

if len(sys.argv) != 2:
  sys.exit("Usage: `python` " + sys.argv[0] + " <AIRTABLE_API_KEY>")
airtable_api_key = str(sys.argv[1])

tasks_table_root = 'https://api.airtable.com/v0/appiU1DE5MRcJwbMk/Table%201'

def fetch_endangered_tasks(api_key):
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key}
    theFilter = "AND({Status}='',DATETIME_DIFF(TODAY(),{CreationTime},'days')>" + str(days_til_endangered) + ')'
    data = {'filterByFormula':theFilter}

    response = requests.get(tasks_table_root, params=data, headers=headers)

    if response.status_code == requests.codes.ok:
        return json.loads(response.content)['records']
    else:
        print('No records found: [' + str(response.status_code) + ']:' + response.reason)

def fetch_stale_tasks(api_key):
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key}
    theFilter = "AND({Status}='',DATETIME_DIFF(TODAY(),{CreationTime},'days')>" + str(days_til_stale) + ')'
    data = {'filterByFormula':theFilter}

    response = requests.get(tasks_table_root, params=data, headers=headers)

    if response.status_code == requests.codes.ok:
        return json.loads(response.content)['records']
    else:
        print('No records found: [' + str(response.status_code) + ']:' + response.reason)

def fetch_expired_tasks(api_key):
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key}
    theFilter = "AND({Status}='Auto-archived',DATETIME_DIFF(TODAY(),{Auto-archive Date},'hours')>" + str(hours_til_expiry) + ')'
    data = {'filterByFormula':theFilter}

    response = requests.get(tasks_table_root, params=data, headers=headers)

    if response.status_code == requests.codes.ok:
        return json.loads(response.content)['records']
    else:
        print('No records found: [' + str(response.status_code) + ']:' + response.reason)

def flag_task_as_endangered(task, api_key):
    data = {'fields': {'Status': 'Endangered'}}
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + airtable_api_key}

    response = requests.patch(tasks_table_root + '/' + task_id(task), json=data, headers=headers)

    if response.status_code == requests.codes.ok:
        return json.loads(response.content)
    else:
        print('Flagging-as-endangered failed for task ' + task_id(task) + '(' + task_name(task) + '): [' + str(response.status_code) + ']:' + response.reason)

def auto_archive_task(task, api_key):
    data = {'fields': {'Status': 'Auto-archived', 'Auto-archive Date': datetime.now().isoformat()}}
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + airtable_api_key}

    response = requests.patch(tasks_table_root + '/' + task_id(task), json=data, headers=headers)

    if response.status_code == requests.codes.ok:
        return json.loads(response.content)
    else:
        print('Auto-archive failed for task ' + task_id(task) + '(' + task_name(task) + '): [' + str(response.status_code) + ']:' + response.reason)

def delete_task(task, api_key): # -> {"deleted": <bool>, "id": "<id>"}
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + airtable_api_key}
    response = requests.delete(tasks_table_root + '/' + task_id(task), headers=headers)

    if response.status_code == requests.codes.ok:
        return json.loads(response.content)
    else:
        print('Deletion failed for task ' + task_id(task) + '(' + task_name(task))

def auto_flag_endangered_tasks(): # -> (archived, failed)
    tasks = fetch_endangered_tasks(airtable_api_key)
    if (tasks is None) or (len(tasks) == 0):
        print("No tasks to auto-flag. 👻")
        return [], []
    else:
        print("\n🐕 Fetched these endangered tasks 🐕")
        pprint(tasks)
        print("🐕 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 🐕\n")

        flagged = []
        failed = []
        for task in tasks:
            flagged_response = flag_task_as_endangered(task, airtable_api_key)
            if flagged_response is None:
                print("🐣 Oh noes.")
                failed.append(task)
            else:
                print('Flagged 👉  ' + str(flagged_response))
                flagged.append(flagged_response)
        return flagged, failed

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
        for task in tasks:
            auto_archive_response = auto_archive_task(task, airtable_api_key)
            if auto_archive_response is None:
                print("😭 Dang.")
                failed.append(task)
            else:
                print('Auto-archived 👉  ' + str(auto_archive_response))
                archived.append(auto_archive_response)
        return archived, failed

def auto_delete_expired_tasks(): # ->(deleted, failed)
    tasks = fetch_expired_tasks(airtable_api_key)
    if (tasks is None) or (len(tasks) == 0):
        print("No tasks to auto-delete. ✔️")
        return [], []
    else:
        print('\n🐕 Fetched these expired tasks 🐕')
        pprint(tasks)
        print("🐕 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 🐕\n")

        deleted = []
        failed = []
        for task in tasks:
            auto_deleted = delete_task(task, airtable_api_key)
            if auto_deleted is None:
                print("🙈 Uh oh!")
                failed.append(task)
            else:
                print('Auto-deleted 👉 ' + str(auto_deleted))
                deleted.append(auto_deleted)
        return deleted, failed

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


deleted, not_deleted = auto_delete_expired_tasks()

for d in deleted:
    print(d)
    notify('❌', 'Deleted ' + str(len(deleted)) + ' expired tasks.')

for n in not_deleted:
    print(n)


flagged, flag_failed = auto_flag_endangered_tasks()
for f in flagged:
    print(f)
    notify(task_name(f), '🚩 Flagged')

for ff in flag_failed:
    print(ff)
