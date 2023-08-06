# Database Communication Manager

Collection of wrappers for communication with database. Supports following databases: 

* SQLite
* PostgreSQL

## Installation

To install the package, simply use pip.

```
$ pip install db_commuter
```

## SQLite

To create a new commuter instance, you need to set path to SQLite database file via constructor. 

```python
from db_commuter.commuters import SQLiteCommuter
commuter = SQLiteCommuter(path2db)
```

Select data from table and return pandas dataframe. 

```python
age = 55
salary = 1000
data = commuter.select('select * from people where age > %s and salary > %s' % (age, salary))
```

Insert from pandas dataframe to database table.

```python
commuter.insert('people', data)
```

Execute an SQL statement.

```python
who = 'Yeltsin'
age = 72
commuter.execute('insert into people values (?, ?)', vars=(who, age)) 
```

To execute multiple SQL statements with one call, use `executescript()`.

```python
commuter.execute_script(path2script)
```

## PostgreSQL

### Setting the Commuter

To initialize a new commuter with PostgreSQL database, you need to set the basic connection parameters, which are
`host`, `port`, `user`, `password`, `db_name`. Any other connection parameter can be passed as a keyword.
The list of the supported parameters [can be seen here](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-PARAMKEYWORDS).

```python
from db_commuter.commuters import PgCommuter
commuter = PgCommuter(host, port, user, password, db_name, sslmode='require')
```

Alternatively, you can use `from_dict` method to initialize commuter from dictionary.  

```python
commuter = PgCommuter.from_dict({
    'host': 'localhost', 
    'port': '5432', 
    'user': 'postgres', 
    'password': 'password', 
    'db_name': 'test_db'}) 
```

### Basic Usage

Basic operations are provided with `select()`, `insert()` and `execute()` methods.

```python
data = commuter.select('select * from people where age > %s and salary > %s' % (55, 1000))
commuter.insert('people', data)
commuter.execute('insert into people values (%s, %s)', vars=('Yeltsin', 72)) 
```   

To execute multiple SQL statements with one call, use executescript().

```python
commuter.execute_script(path2script)
```

### Fast Insert

In contrast to `insert()` method which, in turn, uses pandas `to_sql()` machinery, the `insert_fast()` method 
efficiently copies data from pandas dataframe to database employing PostgreSQL `copy` command. 

```python
commuter.insert_fast('people', data)
```

As compared to conventional `insert()`, this method works much more effective on the large dataframes. 

### Setting Schema in Constructor 

If you operate only on tables within the specific schema, it could make sense to specify the name of database schema 
when you create the commuter instance.

```python
from db_commuter.commuters import PgCommuter
commuter = PgCommuter(host, port, user, password, db_name, schema='model')
```

## License

Package is released under [MIT License](https://github.com/viktorsapozhok/db-commuter/blob/master/LICENSE).
