import sys
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
    data = {'fields': {'Status': 'Auto-archived'}}
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + airtable_api_key}

    response = requests.patch(tasks_table_root + '/' + task['id'], json=data, headers=headers)

    if response.status_code == requests.codes.ok:
        return json.loads(response.content)
    else:
        print('Auto-archive failed for task ' + task['id'] + '(' + task['Name'] + '): [' + str(response.status_code) + ']:' + response.reason)

def auto_archive_stale_tasks():
    tasks = fetch_stale_tasks(airtable_api_key)
    if tasks is not None:
        print("\n🐕 Fetched these stale tasks 🐕")
        pprint(tasks)
        print("🐕 ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 🐕\n")

        for task in tasks:
            auto_archive_response = auto_archive_task(task, airtable_api_key)
            if auto_archive_response is None:
                print("😭 Dang.")
            else:
                print('Auto-archived 👉  ' + auto_archive_response['fields']['Name'])

auto_archive_stale_tasks()
