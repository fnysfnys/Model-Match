"""
Definitions of our permissions, we store permissions as integers in the
database.

When a user is given their JWT, it contains their permissions data.

We authenticate this in our endpoints, for example, we only allow upload of
models and datasets if your permissions are 1 or 2.
"""

READ = 0
READ_WRITE = 1
READ_WRITE_CREATE_USERS = 2
