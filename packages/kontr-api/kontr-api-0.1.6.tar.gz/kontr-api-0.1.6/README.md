# Kontr Portal REST API Client

Kontr Portal REST API Client is the Portal REST API wrapper over the resources in the portal.
It supports CRUD operations and simple management over entities.

Kontr 2 is the project created on FI MUNI to test and execute students solutions for programming assignments.

## Setup

Install and update using the pip:

```bash
$ pip install kontr-api
```

## Simple examples

Simple examples how to configure and user the API Client.

Example how to manage the users.

```python
from kontr_api import KontrClient

portal_url='https://localhost'
username='admin'
password='123456'

kontr_client = KontrClient(url=portal_url, username=username, password=password)

# List all users
kontr_client.users.list()

# Create new user
kontr_client.users.create(username='xlogin', name='Test user', uco='123456')

# Get user
user = kontr_client.users.get('xlogin')

# Update user's name
user['name'] = 'new name'
user.update() # or use the kontr_client.users.update({ 'name': 'new name' }, 'xlogin')

# Set user's password
user.set_password('Password.123')

# Delete the user
user.delete() # or use the kontr_client.users.delete('xlogin')
```

## Contributing

Take a look at the [contribution guide](https://gitlab.fi.muni.cz/grp-kontr2/kontr-documentation/blob/master/contributing/GeneralContributionGuide.adoc).