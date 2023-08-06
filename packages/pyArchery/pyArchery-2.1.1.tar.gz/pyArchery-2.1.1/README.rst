
ArcherySec REST API
*******************

Archery is an opensource vulnerability assessment and management tool which helps developers and pentesters to perform scans and manage vulnerabilities. Archery uses popular opensource tools to perform comprehensive scanning for web application and network. It also performs web application dynamic authenticated scanning and covers the whole applications by using selenium. The developers can also utilize the tool for implementation of their DevOps CI/CD environment.

- `For More details <http://docs.archerysec.com/>`__

Requirements
~~~~~~~~~~~~

- `Archery tool <https://github.com/archerysec/archerysec>`__
- Python 2.7

Quick Start
~~~~~~~~~~~~

Several quick start options are available:

- Install with pip: ``pip install PyArchery``
- Build locally: ``python setup.py build``
- `Download the latest release <https://github.com/target/webinspectapi/releases/latest/>`__


Example
~~~~~~~

::


    # Import the package
    from archery import api

    # Set Archery url
    host = 'http://127.0.0.1:8008'

    # Setup archery connection
    archery = api.ArcheryAPI(host)

    # Provide Archery Credentials for authentication.
    authenticate = archery.archery_auth('admin', 'admin@123A')

    # Collect Token after authentication
    token = authenticate.data
    for key, value in token.viewitems():
        token = value

    # List all Projects
    project = archery.list_project(auth=token)

    # Printing in Json Format
    print project.data_json()


Bugs and Feature Requests
~~~~~~~~~~~~~~~~~~~~~~~~~

- `If you Found bug or have a feature request? Please open a new issue <https://github.com/archerysec/archerysec/issues>`__
