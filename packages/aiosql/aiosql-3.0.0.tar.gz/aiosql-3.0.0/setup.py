# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiosql', 'aiosql.adapters']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiosql',
    'version': '3.0.0',
    'description': 'Simple SQL in Python.',
    'long_description': '# aiosql\n\nSimple SQL in Python.\n\nSQL is code, you should be able to write it, version control it, comment on it, and use it in database tools\nlike `psql` as you would any other SQL. But, you also want to be able to use it from your python\napplications, and that\'s where `aiosql` can help. With `aiosql` you can organize your SQL statements in `.sql`\nfiles and load them into a python object as methods to call.\n\nThis project supports sync and asyncio based drivers for SQLite (`sqlite3`, `aiosqlite`) and PostgreSQL\n(`psycopg2`, `asyncpg`) out of the box, and can be extended to support other database drivers by you! The ``asyncio``\nsupport restricts this package to python versions >3.6. If you are using older versions of python please see the\nrelated [anosql](https://github.com/honza/anosql) package which this project is based on.\n\n## Install\n\n```\npip install aiosql\n```\n\nOr if you you use [poetry](https://poetry.eustace.io/):\n\n```\npoetry add aiosql\n```\n\n## Getting Started\n\n#### Basic Usage\n\nGiven you have a SQL file like the one below called `users.sql`\n\n```sql\n-- name: get-all-users\n-- Get all user records\nselect * from users;\n\n\n-- name: get-user-by-username\n-- Get user with the given username field.\nselect userid,\n       username,\n       firstname,\n       lastname\n  from users\n where username = :username;\n```\n\nYou can use `aiosql` to load the queries in this file for use in your Python application:\n\n```python\nimport aiosql\nimport sqlite3\n\nconn = sqlite3.connect("myapp.db")\nqueries = aiosql.from_path("users.sql", "sqlite3")\n\nusers = queries.get_all_users(conn)\n# >>> [(1, "nackjicholson", "William", "Vaughn"), (2, "johndoe", "John", "Doe"), ...]\n\nusers = queries.get_user_by_username(conn, username="nackjicholson")\n# >>> [(1, "nackjicholson", "William", "Vaughn")\n```\n\nThis is pretty nice, we\'re able to define our methods in SQL and use them as methods from python!\n\n#### Query Operators to define different types of SQL actions\n\n`aiosql` can help you do even more by allowing you to declare in the SQL how you would like a query to be executed\nand returned in python. For instance, the `get-user-by-username` query above should really only return a single result\ninstead of a list containing one user. With the raw `sqlite3` driver in python we would probably have used \n`cur.fetchone()` instead of `cur.fetchall()` to retrieve a single row. We can inform `aiosql` to select a single row\nby using the `^` (select one) operator on the end of our query name.\n\n```sql\n-- name: get-user-by-username^\n-- Get user with the given username field.\nselect userid,\n       username,\n       firstname,\n       lastname\n  from users\n where username = :username;\n```\n\n```python\nnack = queries.get_user_by_username(conn, username="nackjicholson")\n# >>> (1, "nackjicholson", "William", "Vaughn")\n```\n\n#### Using your own python types for SQL data.\n\nBy declaring a `record_class` directive in our SQL file we can inform `aiosql` to automatically marshal our data to a\ncustom class we\'ve defined in python. In python3.7 a good choice for this is the new `dataclass` package.\n\n```sql\n-- name: get-user-by-username^\n-- record_class: User\n-- Get user with the given username field.\nselect userid,\n       username,\n       firstname,\n       lastname\n  from users\n where username = :username;\n```\n\nAll we have to do is provide our custom type to `aiosql` when we load our queries via the `record_classes` argument.\n\n```python\nimport aiosql\nimport sqlite3\nfrom dataclasses import dataclass\n\n\n@dataclass\nclass User:\n    userid: int\n    username: str\n    firstname: str\n    lastname: str\n\n\nconn = sqlite3.connect("myapp.db")\nqueries = aiosql.from_path("users.sql", "sqlite3", record_classes={"User": User})\n\nnack = queries.get_user_by_username(conn, username="nackjicholson")\n# >>> User(userid=1, username="nackjicholson", firstname="William", lastname="Vaughn")\n```\n\nHopefully this is enough to intrigue you and entice you to give aiosql a try. Check the documentation site for more\ninformation, and more features. Happy SQLing!\n\n## Documentation\n\nProject and API docs https://nackjicholson.github.io/aiosql\n',
    'author': 'William Vaughn',
    'author_email': 'vaughnwilld@gmail.com',
    'url': 'https://github.com/nackjicholson/aiosql',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
