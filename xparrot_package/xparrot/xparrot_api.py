from airtable import Airtable

# 📕 Configuration constants. Extract to top-level config
app_id = 'appiU1DE5MRcJwbMk'
default_table = 'xParrot'


class xParrotAPI():
    def __init__(self, api_key):
        self.api_key = api_key
        self.remote_service = Airtable(app_id, default_table, api_key)

    def fetch(self, filterString, remote=None):
        remote = remote if remote is not None else self.remote_service
        return remote.get_iter(formula=filterString)
