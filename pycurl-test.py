import pycurl
import re

try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

try:
    import simplejson as json
except ImportError:
    import json

headers = {}
def header_function(header_line):
    # HTTP standard specifies that headers are encoded in iso-8859-1.
    # On Python 2, decoding step can be skipped.
    # On Python 3, decoding step is required.
    header_line = header_line.decode('iso-8859-1')

    # Header lines include the first status line (HTTP/1.x ...).
    # We are going to ignore all lines that don't have a colon in them.
    # This will botch headers that are split on multiple lines...
    if ':' not in header_line:
        return

    # Break the header line into header name and value.
    name, value = header_line.split(':', 1)

    # Remove whitespace that may be present.
    # Header lines include the trailing newline, and there may be whitespace
    # around the colon.
    name = name.strip()
    value = value.strip()

    # Header names are case insensitive.
    # Lowercase name here.
    name = name.lower()

    # Now we can actually record the header name and value.
    # Note: this only works when headers are not duplicated, see below.
    headers[name] = value

buffer = BytesIO()
c = pycurl.Curl()

params = {'filterByFormula': "AND({Status}='',DATETIME_DIFF(TODAY(),{CreationTime},'days')>7)"}
# Form data must be provided already urlencoded.
c.setopt(c.URL, 'https://api.airtable.com/v0/appiU1DE5MRcJwbMk/Table%201' + '?' + urlencode(params))

c.setopt(pycurl.HTTPHEADER, ['Authorization: Bearer keyiAQYWEULeinv72',])
c.setopt(c.VERBOSE, True)
c.setopt(c.WRITEFUNCTION, buffer.write)
# Set our header function.
c.setopt(c.HEADERFUNCTION, header_function)
c.perform()
c.close()

# Figure out what encoding was sent with the response, if any.
# Check against lowercased header name.
encoding = None
if 'content-type' in headers:
    content_type = headers['content-type'].lower()
    match = re.search('charset=(\S+)', content_type)
    if match:
        encoding = match.group(1)
        print('Decoding using %s' % encoding)
if encoding is None:
    # Default encoding for HTML is iso-8859-1.
    # Other content types may have different default encoding,
    # or in case of binary data, may have no encoding at all.
    encoding = 'iso-8859-1'
    print('Assuming encoding is %s' % encoding)

body = buffer.getvalue()
# Decode using the encoding we figured out.
recs = json.loads(body.decode(encoding))['records']

# for r in recs: print(r)

ids2 = [r['id'] for r in recs]

print(ids2)


# curl -v -XPATCH https://api.airtable.com/v0/appiU1DE5MRcJwbMk/Table%201/recMPxChvmkXCWYJG \
# -H "Authorization: Bearer keyiAQYWEULeinv72" \
# -H "Content-type: application/json" \
#  -d '{
#   "fields": {
#     "Status": "Auto-archived"
#   }
# }'


c = pycurl.Curl()
c.setopt(c.CUSTOMREQUEST, 'PATCH')

# Form data must be provided already urlencoded.
c.setopt(c.URL, 'https://api.airtable.com/v0/appiU1DE5MRcJwbMk/Table%201/recMPxChvmkXCWYJG')

c.setopt(pycurl.HTTPHEADER, ['Authorization: Bearer keyiAQYWEULeinv72', 'Content-type: application/json'])
post_data = {'fields': {'Status': 'Auto-archived'}}
# Form data must be provided already urlencoded.
postfields = urlencode(post_data)
c.setopt(c.POSTFIELDS, postfields)

c.setopt(c.VERBOSE, True)
c.setopt(c.WRITEFUNCTION, buffer.write)
# Set our header function.
c.setopt(c.HEADERFUNCTION, header_function)
c.perform()
c.close()
