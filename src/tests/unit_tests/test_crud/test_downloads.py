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

        self.model = schemas.models.ModelCreate(
            name="dummy-model",
            description="this is a test",
            version_control="vc",
            release_terms="rt",
            outcome="outcome",
            output="output",
            output_to_trigger="ott",
            target_population="tp",
            time_of_prediction="top",
            input_data_source="ids",
            input_data_type="idt",
            training_details="td",
            model_type="mt"
        )

        db = SessionLocal()
        crud.models.create_model(db, self.model, file_path="/", user_id=1)
        db.close()

        db = SessionLocal()
        crud.downloads.create_download(db, 1, 1)
        db.close()

    def tearDown(self):
        os.remove(f'{os.getcwd()}/tests/data/test.db')

    def test_create_download(self):
        self.model = schemas.models.ModelCreate(
            name="dummy-model-2",
            description="this is a test",
            version_control="vc",
            release_terms="rt",
            outcome="outcome",
            output="output",
            output_to_trigger="ott",
            target_population="tp",
            time_of_prediction="top",
            input_data_source="ids",
            input_data_type="idt",
            training_details="td",
            model_type="mt"
        )

        db = SessionLocal()
        crud.models.create_model(db, self.model, file_path="/", user_id=1)
        db.close()

        db = SessionLocal()
        crud.downloads.create_download(db, model_id=2, user_id=1)
        db.close()

        db = SessionLocal()
        db_dataset = db.query(models.Download).filter(
            models.Download.id == 2
            ).first()
        db.close()

        self.assertEqual(db_dataset.model_id, 2)
        self.assertEqual(db_dataset.user_id, 1)
        
    def test_get_downloads(self):
        db=SessionLocal()
        db_downloads = crud.downloads.get_downloads(user_id=1, db=db, skip=0, limit=100)
        db.close()
        self.assertEqual(type(db_downloads), list)
        self.assertEqual(len(db_downloads), 1)
        self.assertEqual(type(db_downloads[0]), models.Download)
        self.assertEqual(db_downloads[0].model_id, 1)
        self.assertEqual(db_downloads[0].user_id, 1)
    
    def test_get_download(self):
        db=SessionLocal()
        db_download = crud.downloads.get_download(db, model_id=1, user_id=1)
        db.close()
        self.assertEqual(type(db_download), models.Download)
        self.assertEqual(db_download.model_id, 1)
        self.assertEqual(db_download.user_id, 1)
