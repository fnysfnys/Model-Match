from ..database import Base
from .datasets import Dataset
from .downloads import Download
from .feedback import Feedback
from .models import Model
from .users import User

"""
Definitions of our database schema with SQLAlchemy, here we define our tables,
fields, and relationships.

We point this definition to alembic in line 20 of src/alembic/env.py.

If we want to update our database schema, simply add your changes here
(for example a new field in users, or a new table)

Then run:

alembic revision --autogenerate -m "My useful message"

This will result in a new revision in src/alembic/versions.

To apply this to your database, run:

alembic upgrade head

(make sure you have set the DB_URL environment variable on your machine)
"""