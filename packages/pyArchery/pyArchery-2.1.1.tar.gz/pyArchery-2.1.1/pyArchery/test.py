from pyArchery import api

# Set Archery url
host = 'http://127.0.0.1:8000'

# Setup archery connection
archery = api.ArcheryAPI(host)

# Provide Archery Credentials for authentication.
authenticate = archery.archery_auth('admin', 'admin@123')

# Collect Token after authentication
token = authenticate.data
for key, value in token.viewitems():
    token = value
# Get the scan result
web_scan_result = archery.findbugs_scan_status(
    auth=token,
    scan_id='d6ffdf33-036a-41d5-94ac-339c9a4b3105',
)

print(web_scan_result.data_json())