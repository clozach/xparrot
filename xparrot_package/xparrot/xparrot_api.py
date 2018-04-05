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
import requests
from requests.exceptions import HTTPError

# 📕 Configuration constants. Extract to top-level config
app_id = 'appiU1DE5MRcJwbMk'
default_table = 'xParrot'
projects_table = 'Projects'
subprojects_table = 'Subprojects'
days_til_endangered = 5
days_til_stale = 7
hours_til_expiry = 18


class xParrotAPI():
    def __init__(self):
        self.remote_service = Airtable(app_id, default_table)
        self.remote_projects_service = Airtable(app_id, projects_table)
        self.remote_subprojects_service = Airtable(app_id, subprojects_table)

    def fetch(self, filterString, remote=None):
        remote = remote if remote is not None else self.remote_service
        return remote.get_iter(formula=filterString)

    def fetch_projects(self, filterString='', remote=None):
        remote = remote if remote is not None else self.remote_projects_service
        return remote.get_iter(formula=filterString)

    def fetch_subprojects(self, filterString='', remote=None):
        remote = remote if remote is not None else self.remote_subprojects_service
        return remote.get_iter(formula=filterString)

    def task(self, id=None, name=None, remote=None):
        """Task by ID (or, eventually, by name)
        
        Keyword Arguments:
            id {str} -- AirTable ID (default: {None})
            name {str} -- Contents of Airtable `Name` field (default: {None})
            remote {Airtable} -- The Airtable table to query (default: {None})
        
        Returns:
            record (`dict`) or None -- Airtable record.
        """

        remote = remote if remote is not None else self.remote_service
        if id == None and name == None:
            print('No task identifier given.')
            return None
        elif id != None:
            return remote.get(id)


class xPF():
    """xPF == xParrot Filters
    """

    @staticmethod
    def unstarted():
        return "{Status}=''"

    @classmethod
    def endangered(cls, dte=days_til_endangered):
        """Tasks that will be auto-archived if no action is taken "soon".

        Here "soon" is defined as "within {days_til_stale} - {days_til_endangered}".
        For example, if dts==7 and dte==5, `endangered` tasks are those tasks that
        will be expired in 2 days or less.

        Note that only Unstarted tasks can be Endangered. (Probably should include
        Started tasks as well? Baby steps.)
        
        Keyword Arguments:
            dte {num} -- The age at which the task will be considered "Expired" (default: {days_til_endangered})
        
        Returns:
            str -- A query string for Airtable's `filterByFormula` query parameter 
        """
        return "AND({Status}=''," + cls.older_than('{CreationTime}', dte) + ')'

    @staticmethod
    def by_name(name):
        return "{Name}='Name'"

    @staticmethod
    def started():
        return "{Status}='Started'"

    @staticmethod
    def done():
        return "{Status}='Done'"

    @staticmethod
    def auto_archived():
        return "{Status}='Auto-archived'"

    @classmethod
    def stale(cls, dts=days_til_stale):
        """Tasks ready to have the `Auto-archived` tag and `Auto-archive Date` applied

        Note that only Unstarted and Endangered tasks can be Stale. (As with `endangered`,
        there may be cause to include Started here as well)
        
        Keyword Arguments:
            dts {num} -- The age at which the task will be considered "Stale" (default: {days_til_stale})
        
        Returns:
            str -- A query string for Airtable's `filterByFormula` query parameter
        """
        return "AND(OR({Status}='',{Status}='Endangered')," + cls.older_than(
            '{CreationTime}', dts) + ')'

    @staticmethod
    def expired():
        """Tasks needing to be archived

        Future possibility: remove "Done" and "Auto-archived" statuses from the xParrot table,
        as well as the "Auto-archived Date", limiting those concepts to the Archive table (which,
        in turn, would not include "Started" and "Endangered" tags)

        Again. Baby steps.
        
        Returns:
            str -- A query string for Airtable's `filterByFormula` query parameter
        """
        return "OR({Status}='Done',{Status}='Auto-archived')"

    @staticmethod
    def older_than(birth_date_string, number_of_days, units='days'):
        return "DATETIME_DIFF(TODAY()," + birth_date_string + ",'days')>" + str(
            number_of_days)


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
