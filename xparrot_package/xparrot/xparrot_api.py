# -*- coding: utf-8 -*-
"""

xParrotAPI Class Instance
***********************

>>> api = xParrotAPI() // Make sure to set the AIRTABLE_API_KEY environment variable.
>>> api.fetch(ready_to_be_moved_to_archive())
[{'id': 'recMtGPR0nE6499eC', 'fields': {'Name': 'Mess with Flutter', 'Notes': 'How much effort is needed to make a list from a single xParrot query? Try it out…is it better than Slack? Maybe not best for MVP…but sounds cool!', 'Status': 'Done', 'Link': 'https://flutter.io/setup-macos/', 'Project': ['recZmAQo7QyUzSORd'], 'Subproject': ['recsAxA5QsrtDdAUE']}, 'createdTime': '2018-03-14T08:44:03.000Z'}]

------------------------------------------------------------------------

🌪 Filters:

- endangered_tasks(days_til_endangered) : Status is empty & the days_til_endangered has expired
- stale_tasks(days_til_stale) : Empty or 'Endangered' status with expired creation date
- expired_tasks(hte=hours_til_expiry) : Tagged 'Auto-archived' with 'Auto-archive date' expired.
- tasks_ready_to_be_moved_to_archive() : Status is 'Done' or 'Auto-archived'

🌾 Fields:

- status_endangered : Status is Endangered
- status_auto_archived : Status is Auto-archived, with the current date provided for reference.

🐶 Actual Fetching

- fetch(airtable, filterString) : non-specific fetch
- fetch_endangered_tasks(airtable) : tasks w/empty status & expired creation date 👈⚠️This needs tweaking. Instead of creation date, I want to use some other set of metrics: one that responds to user behavior.
- fetch_archivable_tasks(airtable) : tasks w/status 'Done' or 'Auto-archived'
- fetch_stale_tasks(airtable, days_til_stale) : empty or 'Endangered' status with creation date > 7. ⚠️ Again, not ideal, this.
- fetch_expired_tasks(airtable, hours_til_expiry) : 'Auto-archived' with 'Auto-archive date' older than 18 hours old. I.e., tasks that have been marked as somehow done for nearly a day.

Question: Why have I been insisting that the archive exist separate from the todo list? I think perhaps it's because, if we're going to be keeping the equivalent of old scraps of paper around, we must ensure that they don't clutter our "action" space. The todo list must be lean, with as little inertia as possible, no matter what client is used to view it, including the native AirTable tools.

"""  #
from airtable import Airtable
from datetime import datetime

# 📕 Configuration constants. Extract to top-level config
app_id = 'appiU1DE5MRcJwbMk'
default_table = 'xParrot'
days_til_endangered = 5
days_til_stale = 7
hours_til_expiry = 18


class xParrotAPI():
    def __init__(self):
        self.remote_service = Airtable(app_id, default_table)

    def fetch(self, filterString, remote=None):
        remote = remote if remote is not None else self.remote_service
        return remote.get_iter(formula=filterString)


# 🌪 Filters
def endangered_tasks(dte=days_til_endangered):
    return "AND({Status}='',DATETIME_DIFF(TODAY(),{CreationTime},'days')>" + str(
        dte) + ')'


def stale_tasks(dts=days_til_stale):
    return "AND(OR({Status}='',{Status}='Endangered'),DATETIME_DIFF(TODAY(),{CreationTime},'days')>" + str(
        dts) + ')'


def expired_tasks(hte=hours_til_expiry):
    return "AND({Status}='Auto-archived',DATETIME_DIFF(TODAY(),{Auto-archive Date},'hours')>" + str(
        hte) + ')'


def tasks_ready_to_be_moved_to_archive():
    return "OR({Status}='Done',{Status}='Auto-archived')"


# 🌾 Fields
def status_endangered():
    return {'Status': 'Endangered'}


def status_auto_archived():
    return {
        'Status': 'Auto-archived',
        'Auto-archive Date': datetime.now().isoformat()
    }


# 🐶 Fetch
def fetch(airtable, filterString):
    return airtable.get_iter(formula=filterString)


def fetch_endangered_tasks(airtable):
    return fetch(airtable, endangered_tasks())


def fetch_archivable_tasks(airtable):
    return fetch(airtable, tasks_ready_to_be_moved_to_archive())


def fetch_stale_tasks(airtable, dts=days_til_stale):
    return fetch(airtable, stale_tasks())


def fetch_expired_tasks(airtable, hte=hours_til_expiry):
    return fetch(airtable, expired_tasks())
