# epflldap

## Installation
`pip install dist/epflldap-<version>-py3-none-any.whl`

## Build new version
* Makes changes
* Change the version in `_version.py`
* `python setup.py bdist_wheel`

## Basic usages

### 1. Get and save locally the data of EPFL Ldap
```python
import epflldap
data = epflldap.db()
data.to_pickle()
```
This will create locally a `ldap_epfl.pickle` file.

To load the local data:
```python
import epflldap
data = epflldap.db(read_from_pickle=True)
```

### 2. Get users data only
```python
import epflldap
users = epflldap.db(read_from_pickle=True).get_users()
```
You will get a `Users` object.

### 3. Filter users data

#### Filter by group
```python
import epflldap
users = epflldap.db(read_from_pickle=True).get_users()
users_filtered = users.filter_by_group('webmasters')
```
You will get an other `Users` object with only the filtered data. Available
groups are here: https://groups.epfl.ch/

#### Filter by status
```python
import epflldap
users = epflldap.db(read_from_pickle=True).get_users()
users_filtered = users.filter_by_status(['Personnel'])
```
Possible status are:
* `Personnel`
* `Etudiant`
* `Hôte`
* `Hors EPFL`

Several entries don't have a status.

#### Filter by unit
```python
import epflldap
users = epflldap.db(read_from_pickle=True).get_users()
users_filtered = users.filter_by_unit('SISB')
```
You will get all the users from the SISB team.

#### Filter by school
```python
import epflldap
users = epflldap.db(read_from_pickle=True).get_users()
users_filtered = users.filter_by_school('CDH')
```
You will get all the users from the CDH school.

#### Filter by sciper
```python
import epflldap
users = epflldap.db(read_from_pickle=True).get_users()
users_filtered = users.filter_by_sciper(['sciper1', 'sciper2'])
```
Filter the list of users with the given list of sciper id.

In order to get information about a specific user you can:
```python
import epflldap
epflldap.db(read_from_pickle=True)
    .get_users()
    .filter_by_sciper(['sciper1'])
    .data[0]
    .get_info()
```
You will get a Pandas Series with information about the person with the
given sciper.

#### Keep only first accred
```python
import epflldap
users = epflldap.db(read_from_pickle=True).get_users()
users_filtered = users.filter_by_first_accred()
```
You will get only the main accreditation of each user.


### 4. Get all the email addresses of a `Users` object
```python
import epflldap
users = epflldap.db(read_from_pickle=True).get_users()
users_filtered = users.filter_by_group('webmasters')
users_filtered.get_emails()
```
You will get all the email addresses of the group 'webmaster'. If you want a txt
file, you can add an argument:
```python
users.get_emails(output='addresses.txt')
```

### 5. Get Excel file with personal information data
```python
import epflldap
users = epflldap.db(read_from_pickle=True).get_users()
users_filtered = users.filter_by_group('webmasters')
users_filtered.to_excel(webmasters.xlsx)
```
This will create a xlsx file with personal information about the users.
