from pyArchery import api

# Set archery url
host = 'http://127.0.0.1:8008'

archery = api.ArcheryAPI(host)

authenticate = archery.archery_auth('admin', 'admin@123A')

token = authenticate.data
for key, value in token.viewitems():
    token = value

# # List all Projects
# project = archery.list_project(auth=token)
#
# # Printing in Json Format
# print project.data_json()

# Create Project
project_create = archery.create_project(
    auth=token,
    project_name="test_project",
    project_disc="Project Descriptions",
    project_start="2018-09-08",  # Project Start Date (YYYY-MM-DD)
    project_end="2018-09-08",  # Project End Date (YYYY-MM-DD)
    project_owner='Anand',  # Project Owner Name
)

print(project_create.data_json())

# # List all web scans
# web_scan = archery.web_scans(auth=token)
#
# # Print as Json Format
# print web_scan.data_json()

# web_scan_create = archery.create_webscan(
#     auth=token,
#     scan_url='http://demo.testfire.net',
#     project_id='1de4b51c-db0f-47c4-8979-55190f01055e',
#     scanner='zap_scan'
# )
#
# print web_scan_create.data_json()

# Get the scan result
# web_scan_result = archery.webscan_result(
#     auth=token,
#     scan_id='47631d4b-b715-4e7f-a67d-94b8ecfa8ae8',
# )
#
# print web_scan_result.data_json()

# network_scans = archery.network_scan(
#     auth=token,
# )
#
# print network_scans.data_json()

# Create network scans
# create_network_scan = archery.create_newtworkscan(
#     auth=token,
#     scan_ip='192.168.1.1',
#     project_id='1de4b51c-db0f-47c4-8979-55190f01055e'
# )
#
# print create_network_scan.data_json()

# Get the network scan results
# network_result = archery.networkscan_result(
#     auth=token,
#     scan_id='54fbaa87-e22f-4817-b4a2-15b86aa58e9c'
# )
#
# print network_result