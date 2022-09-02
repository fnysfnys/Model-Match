import unittest

from ....api import models, crud, schemas, auth
from ....api.database import SessionLocal, engine
from fastapi import Depends
from ....api.models import Base
import os

class TestDatasets(unittest.TestCase):
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

        self.dataset = schemas.datasets.DatasetCreate(
            name="mock_dataset",
            description="this is a test"
        )

        db = SessionLocal()
        crud.datasets.create_dataset(db, self.dataset, file_path="/", user_id=1)
        db.close()

    def tearDown(self):
        os.remove(f'{os.getcwd()}/tests/data/test.db')
        
    def test_create_dataset(self):
        new_dataset = schemas.datasets.DatasetCreate(
            name="mock_dataset_2",
            description="this is a second test"
        )

        db = SessionLocal()
        crud.datasets.create_dataset(db, new_dataset, file_path="/", user_id=1)
        db.close()

        db = SessionLocal()
        db_dataset = db.query(models.Dataset).filter(
            models.Dataset.id == 2
            ).first()
        db.close()

        self.assertEqual(type(db_dataset), models.Dataset)
        self.assertEqual(db_dataset.name, new_dataset.name)
        self.assertEqual(db_dataset.description, new_dataset.description)
        self.assertEqual(db_dataset.file_path, "/")
        self.assertEqual(db_dataset.user_id, 1)
    
    def test_get_dataset_by_name(self):
        db = SessionLocal()
        db_dataset = crud.datasets.get_dataset_by_name(db, self.dataset.name)
        db.close()

        self.assertEqual(type(db_dataset), models.Dataset)
        self.assertEqual(db_dataset.name, self.dataset.name)
        self.assertEqual(db_dataset.description, self.dataset.description)
        self.assertEqual(db_dataset.file_path, "/")
        self.assertEqual(db_dataset.user_id, 1)

    def test_get_dataset_by_id(self):
        db = SessionLocal()
        db_dataset = crud.datasets.get_dataset_by_id(db, 1)
        db.close()

        self.assertEqual(type(db_dataset), models.Dataset)
        self.assertEqual(db_dataset.name, self.dataset.name)
        self.assertEqual(db_dataset.description, self.dataset.description)
        self.assertEqual(db_dataset.file_path, "/")
        self.assertEqual(db_dataset.user_id, 1)
    
    def test_get_datasets(self):
        db=SessionLocal()
        db_datasets = crud.datasets.get_datasets(db, 0, 100)
        db.close()
        self.assertEqual(type(db_datasets), list)
        self.assertEqual(len(db_datasets), 1)
        self.assertEqual(type(db_datasets[0]), models.Dataset)
        self.assertEqual(db_datasets[0].name, self.dataset.name)
        self.assertEqual(db_datasets[0].description, self.dataset.description)
        self.assertEqual(db_datasets[0].file_path, "/")
        self.assertEqual(db_datasets[0].user_id, 1)

    def test_delete_dataset(self):
        db=SessionLocal()
        crud.datasets.delete_dataset(db, 1)
        db.close()

        db=SessionLocal()
        db_datasets = db.query(models.Dataset).offset(0).limit(100).all()
        db.close()

        self.assertListEqual(db_datasets, [])
