# dbcl - Database Command Line
[![Build Status](https://travis-ci.org/ksofa2/dbcl.svg?branch=master)](https://travis-ci.org/ksofa2/dbcl)
[![Maintainability](https://api.codeclimate.com/v1/badges/e4663675580964433469/maintainability)](https://codeclimate.com/github/ksofa2/dbcl/maintainability)


An engine-agnostic database command line interface.


## Installation

Use `pip` to install the dbcl tool:

```
pip install dbcl
```

Also install the necessary packages for your database, for example: `cx_Oracle`, `pg8000` or `PyMySQL`.


## Database connection

Database connections are specified using [SQLAlchemy database URLs](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls). The database URL can be given as an argument to the `dbcl` command:

```
dbcl sqlite:///database.db
```

If the URL isn't given as an argument, a prompt will ask for the URL to use for the connection:

```
$ dbcl
Connect to [sqlite:///database.db]:
```

If the DATABASE_URL environmental variable is set, that value will be the default for the database prompt:

```
$ export DATABASE_URL=sqlite:///database.db
$ dbcl
Connect to [sqlite:///database.db]:
```

Example of a connection to a PostgreSQL database using wht `pg8000` package:

```
dbcl postgresql+pg8000://username:password@127.0.0.1:5432/dbname
```
