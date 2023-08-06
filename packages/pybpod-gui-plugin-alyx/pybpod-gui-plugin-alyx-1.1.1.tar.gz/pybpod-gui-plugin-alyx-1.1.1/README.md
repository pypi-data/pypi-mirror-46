# Pybpod Alyx Module

Alyx is a database designed for storage and retrieval of all data in an experimental neuroscience laboratory - from subject management through data acquisition, raw data file tracking and storage of metadata resulting from manual analysis.

The Pybpod Alyx Module allows communication with Alyx databases inside the Pybpod environment. The goal is to use pybpod to manage Alyx information such as subjects and users, and associate Pybpod experiments with those users and subjects.

Currently, only subject and data is implemented on the API side, but API expansion is easy. More information on the Alyx API can be found at http://alyx.readthedocs.io/en/latest/index.html

## Usage

Following the REST API structure, we can divide the requests into several categories.

- USERS
- SUBJECTS
- Actions
- WATER RESTRICTIONS
- DATA

Each category has it's GET and POST/PATCH methods, described at the Alyx API page shared above.

The python implementation of the API calls is designed to mimic the documentation structure, for instance:

``` python
api.<CATEGORY>.<METHOD>.<METHODCALL>
```
or more explicitly

``` python
api.subjects.get.allsubjects()
``` 

All the api calls shall return objects in the JSON format, so they can be easily managed according to the type of application the user wants to use it in.