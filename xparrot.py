import sys
import os
from airtable import Airtable
from pprint import pprint
from datetime import datetime

# 📕 Configuration constants
app_id = 'appiU1DE5MRcJwbMk'
table = 'xParrot'
days_til_endangered = 5
days_til_stale = 7
hours_til_expiry = 18

if len(sys.argv) != 2:
  sys.exit("Usage: `python` " + sys.argv[0] + " <AIRTABLE_API_KEY>")
airtable_api_key = str(sys.argv[1])

airtable = Airtable(app_id, table, airtable_api_key)

# 🌪 Filters
def endangered(dte=days_til_endangered):
    return "AND({Status}='',DATETIME_DIFF(TODAY(),{CreationTime},'days')>" + str(dte) + ')'

def stale(dts=days_til_stale):
    return "AND(OR({Status}='',{Status}='Endangered'),DATETIME_DIFF(TODAY(),{CreationTime},'days')>" + str(dts) + ')'

def expired(hte=hours_til_expiry):
    return "AND({Status}='Auto-archived',DATETIME_DIFF(TODAY(),{Auto-archive Date},'hours')>" + str(hte) + ')'

# 🌾 Fields
def status_endangered():
    return {'Status': 'Endangered'}

def status_auto_archived():
    return {'Status': 'Auto-archived', 'Auto-archive Date': datetime.now().isoformat()}

# 🐶 Fetch
def fetch(airtable, filterString):
    return airtable.get_iter(formula=filterString)

def fetch_endangered_tasks(airtable):
    return fetch(airtable, endangered())

def fetch_stale_tasks(airtable, dts=days_til_stale):
    return fetch(airtable, stale())

def fetch_expired_tasks(airtable, hte=hours_til_expiry):
    return fetch(airtable, expired())

# ✍️ Update

def update(airtable, task, fields):
    return airtable.update(task['id'], fields)

def flag_as_endangered(airtable, task):
    return update(airtable, task, status_endangered())

def auto_archive(airtable, task):
    return update(airtable, task, status_auto_archived())

def delete(airtable, task):
    return airtable.delete(task['id'])

# 📓 Compositions
def auto_flag_endangered_tasks(): # -> (archived, failed)
    tasks = next(fetch_endangered_tasks(airtable))
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
            flagged_response = flag_as_endangered(airtable, task)
            if flagged_response is None:
                print("🐣 Oh noes.")
                failed.append(task)
            else:
                print('Flagged 👉  ' + str(flagged_response))
                flagged.append(flagged_response)
        return flagged, failed

def auto_archive_stale_tasks(): # -> (archived, failed)
    tasks = next(fetch_stale_tasks(airtable))
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
            auto_archive_response = auto_archive(airtable, task)
            if auto_archive_response is None:
                print("😭 Dang.")
                failed.append(task)
            else:
                print('Auto-archived 👉  ' + str(auto_archive_response))
                archived.append(auto_archive_response)
        return archived, failed

def auto_delete_expired_tasks(): # ->(deleted, failed)
    tasks = next(fetch_expired_tasks(airtable))
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
            auto_deleted = delete(airtable, task)
            if auto_deleted is None:
                print("🙈 Uh oh!")
                failed.append(task)
            else:
                print('Auto-deleted 👉 ' + str(auto_deleted))
                deleted.append(auto_deleted)
        return deleted, failed

# 🍹 Misc.
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

# 🎴 POOR MAN'S TESTS
s, f = auto_flag_endangered_tasks()
for i in s:
    notify(task_name(i), '🚩 Flagged')

for i in f:
    notify('🚨 Failed to flag', task_name(i))

s, f = auto_archive_stale_tasks()
for i in s:
    notify(task_name(i), '⚠️ Auto-Archived')

for i in f:
    notify('🚨 Failed to auto-archive', task_name(i))

s, f = auto_delete_expired_tasks()
if len(s) > 0:
    notify('❌', 'Deleted ' + str(len(s)) + ' expired tasks.')

for i in f:
    notify('🚨 Failed to delete', task_name(i))
