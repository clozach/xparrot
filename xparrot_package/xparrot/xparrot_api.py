from airtable import Airtable
from datetime import datetime

# 📕 Configuration constants. Extract to top-level config
app_id = 'appiU1DE5MRcJwbMk'
default_table = 'xParrot'
days_til_endangered = 5
days_til_stale = 7
hours_til_expiry = 18


class xParrotAPI():
    def __init__(self, api_key):
        self.api_key = api_key
        self.remote_service = Airtable(app_id, default_table, api_key)

    def fetch(self, filterString, remote=None):
        remote = remote if remote is not None else self.remote_service
        return remote.get_iter(formula=filterString)


# 🌪 Filters
def endangered(dte=days_til_endangered):
    return "AND({Status}='',DATETIME_DIFF(TODAY(),{CreationTime},'days')>" + str(
        dte) + ')'


def stale(dts=days_til_stale):
    return "AND(OR({Status}='',{Status}='Endangered'),DATETIME_DIFF(TODAY(),{CreationTime},'days')>" + str(
        dts) + ')'


def expired(hte=hours_til_expiry):
    return "AND({Status}='Auto-archived',DATETIME_DIFF(TODAY(),{Auto-archive Date},'hours')>" + str(
        hte) + ')'


def ready_for_archive():
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
    return fetch(airtable, endangered())


def fetch_archivable_tasks(airtable):
    return fetch(airtable, ready_for_archive())


def fetch_stale_tasks(airtable, dts=days_til_stale):
    return fetch(airtable, stale())


def fetch_expired_tasks(airtable, hte=hours_til_expiry):
    return fetch(airtable, expired())
