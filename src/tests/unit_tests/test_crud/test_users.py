import unittest

from ....api import models, crud, schemas, auth
from ....api.database import SessionLocal, engine
from fastapi import Depends
from ....api.models import Base
import os

class TestUsers(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(bind=engine)
        self.user = schemas.users.UserCreate(
            email="test@gmail.com",
            username="test",
            permissions = 2,
            password = "1234"
        )
        db = SessionLocal()
        crud.users.create_user(db, self.user)
        db.close()

    def tearDown(self):
        os.remove(f'{os.getcwd()}/tests/data/test.db')
        
    def test_create_user(self):
        new_user = schemas.users.UserCreate(
            email="test2@gmail.com",
            username="test2",
            permissions = 2,
            password = "1234"
        )

        db = SessionLocal()
        crud.users.create_user(db, new_user)
        db.close()

        db = SessionLocal()
        db_user = db.query(models.User).filter(
            models.User.email == new_user.email
            ).first()
        db.close()

        self.assertEqual(type(db_user), models.User)
        self.assertEqual(db_user.email, new_user.email)
        self.assertEqual(db_user.username, new_user.username)
        self.assertEqual(db_user.permissions, new_user.permissions)
        self.assertTrue(auth.verify_password(self.user.password, db_user.hashed_password))
    
    def test_get_user_by_email(self):
        db = SessionLocal()
        db_user = crud.users.get_user_by_email(db, self.user.email)
        db.close()

        self.assertEqual(type(db_user), models.User)
        self.assertEqual(db_user.email, self.user.email)
        self.assertEqual(db_user.username, self.user.username)
        self.assertEqual(db_user.permissions, self.user.permissions)
        self.assertTrue(auth.verify_password(self.user.password, db_user.hashed_password))

    def test_get_user_by_username(self):
        db=SessionLocal()
        db_user = crud.users.get_user_by_username(db, self.user.username)
        db.close()

        self.assertEqual(type(db_user), models.User)
        self.assertEqual(db_user.email, self.user.email)
        self.assertEqual(db_user.username, self.user.username)
        self.assertEqual(db_user.permissions, self.user.permissions)
        self.assertTrue(auth.verify_password(self.user.password, db_user.hashed_password))
    
    def test_get_users(self):
        db=SessionLocal()
        db_users = crud.users.get_users(db, 0, 100)
        db.close()
        self.assertEqual(type(db_users), list)
        self.assertEqual(len(db_users), 1)
        self.assertEqual(db_users[0].email, self.user.email)
        self.assertEqual(db_users[0].username, self.user.username)
        self.assertEqual(db_users[0].permissions, self.user.permissions)
        self.assertTrue(auth.verify_password(self.user.password, db_users[0].hashed_password))

    def test_update_password(self):
        new_password = schemas.users.NewPassword(
            password="12345",
            confirmation="12345"
            )
        db = SessionLocal()
        db_user = crud.users.get_user_by_username(db, self.user.username)
        db.close()

        db = SessionLocal()
        crud.users.update_password(db,db_user, new_password)
        db.close()

        db = SessionLocal()
        db_user = db.query(models.User).filter(
            models.User.email == self.user.email
            ).first()
        db.close()

        self.assertEqual(type(db_user), models.User)
        self.assertEqual(db_user.email, self.user.email)
        self.assertEqual(db_user.username, self.user.username)
        self.assertEqual(db_user.permissions, self.user.permissions)
        self.assertTrue(auth.verify_password("12345", db_user.hashed_password))
