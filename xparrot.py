import sys
import requests

if len(sys.argv) != 2:
  sys.exit("Usage: `python` " + sys.argv[0] + " <AIRTABLE_API_KEY>")
airtable_api_key = str(sys.argv[1])

tasks_table_root = 'https://api.airtable.com/v0/appiU1DE5MRcJwbMk/Table%201'

def fetch_stale_tasks(api_key):
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + api_key}
    theFilter = "AND({Status}='',DATETIME_DIFF(TODAY(),{CreationTime},'days')>7)"
    data = {'filterByFormula':theFilter}
    r1 = requests.get(tasks_table_root, params=data, headers=headers)
    print(r1)

def auto_archive_task(task_id, api_key):
    data = {'fields': {'Status': 'Auto-archived'}}
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + airtable_api_key}
    r = requests.patch(tasks_table_root + '/' + task_id, json=data, headers=headers)

    print(r)

fetch_stale_tasks(airtable_api_key)
auto_archive_task('recMPxChvmkXCWYJG', airtable_api_key)
