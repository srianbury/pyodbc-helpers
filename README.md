## pyodbc-helpers

#### Additional features related to pyodbc
- assert successful run of stored procedure

### Getting started
1. install `pip install pyodbc-helpers`

### Examples
- run_sp
```
with pyodbc.connect('CNXN_STRING') as cnxn:
  with cnxn.cursor() as cursor:
    pyodbch.run_sp(cursor, 'USP_MY_SP') # no params
    pyodbch.run_sp(cursor, 'USP_MY_SP', [2, 'bob']) # with params
```
