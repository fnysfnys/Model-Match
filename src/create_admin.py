from api.database import SessionLocal
from api import crud
from api import schemas

"""
We have a closed system, so only administrators can create users.
This script is used to create the initial admin user when deploying.
"""

db = SessionLocal()
crud.users.create_user(db=db, user=schemas.users.UserCreate(
    email="admin@admin.com",
    username="admin",
    permissions=2,
    password="1234"
))
db.close()
