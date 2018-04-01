# -*- coding: utf-8 -*-
"""

xParrotAPI Class Instance
***********************

>>> api = xParrotAPI() // Make sure to set the AIRTABLE_API_KEY environment variable.
>>> api.fetch(started())
[{'id': 'recMtGPR0nE6499eC', 'fields': {'Name': 'Mess with Flutter', 'Notes': 'How much effort is needed to make a list from a single xParrot query? Try it out…is it better than Slack? Maybe not best for MVP…but sounds cool!', 'Status': 'Started', 'Link': 'https://flutter.io/setup-macos/', 'Project': ['recZmAQo7QyUzSORd'], 'Subproject': ['recsAxA5QsrtDdAUE']}, 'createdTime': '2018-03-14T08:44:03.000Z'}]

------------------------------------------------------------------------

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


class xPF():
    """xPF == xParrot Filters
    """

    @staticmethod
    def unstarted():
        return "{Status}=''"

    # @staticmethod
    # def endangered_task(dte=days_til_endangered):
    #     return "AND({Status}='',DATETIME_DIFF(TODAY(),{CreationTime},'days')>" + str(
    #         dte) + ')'

    @staticmethod
    def started():
        return "{Status}='Started'"

    # @staticmethod
    # def stale_tasks(dts=days_til_stale):
    #     return "AND(OR({Status}='',{Status}='Endangered'),DATETIME_DIFF(TODAY(),{CreationTime},'days')>" + str(
    #         dts) + ')'

    # @staticmethod
    # def expired_tasks(hte=hours_til_expiry):
    #     return "AND({Status}='Auto-archived',DATETIME_DIFF(TODAY(),{Auto-archive Date},'hours')>" + str(
    #         hte) + ')'

    @staticmethod
    def stale():
        return "OR({Status}='Done',{Status}='Auto-archived')"


class xPPropertyJSON():
    """xPProps == xParrot Property JSON
    Encapsulates structures used to make changes to records in Airtable
    """

    @staticmethod
    def status_endangered():
        return {'Status': 'Endangered'}

    @staticmethod
    def status_auto_archived():
        return {
            'Status': 'Auto-archived',
            'Auto-archive Date': datetime.now().isoformat()
        }
