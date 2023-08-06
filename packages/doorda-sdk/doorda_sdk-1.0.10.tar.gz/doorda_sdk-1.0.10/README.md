# Doorda Python SDK


## Requirements

- Python 2.7 / Python 3
- [DoordaHost Account](https://doorda.com)

## Installation

### PyPi
```bash
$ pip install doorda-sdk
```

### Source
#### Download from:
1) https://github.com/Doorda/doorda-python-sdk/releases

```bash
$ wget https://github.com/Doorda/doorda-python-sdk/archive/1.0.10.zip

$ unzip 1.0.10.zip
```
#### Install
```bash
$ python setup.py install
```

## Usage

### DoordaHost

1) Connect to database
    ```python
    from doorda_sdk.host import client

    conn = client.connect(username="username",
                          password="password",
                          catalog="catalog_name",
                          schema="schema_name")
    cursor = conn.cursor()
    ```

2) Execute Queries
    ```python
    cursor.execute("SELECT * FROM table_name")

    # Returns generator of results
    # Does not put result into memory. Iterates through rows in a streaming fashion.
    for row in cursor.iter_result():
        # Do something with row
    
    # Fetch all results
    rows = cursor.fetchall()
    
    # Fetch one results
    rows = cursor.fetchone()
    
    # Fetch multiple results
    rows = cursor.fetchmany(size=10)
    
    # Get list of column names
    cursor.col_names
    
    # Get column names mapped to data types
    cursor.col_types
    ```

3) Simplified Functions

    ```python
    # Check database connection
    results = cursor.is_connected()
    
    # List all catalogs
    rows = cursor.show_catalogs()

    # List all tables
    rows = cursor.show_tables("catalog_name", "schema_name")
    
    # Get number of rows
    rows = cursor.table_stats(catalog="catalog_name", 
                              schema="schema_name",
                              table="table_name")
    ```

## Find out more

To find out more about DoordaHost, head over to [https://github.com/Doorda/Getting-Started](https://github.com/Doorda/Getting-Started/blob/master/README.md)
