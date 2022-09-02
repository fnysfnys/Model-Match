import unittest

from ....api import models, crud, schemas, auth
from ....api.database import SessionLocal, engine
from fastapi import Depends
from ....api.models import Base
import os

class TestDownloads(unittest.TestCase):
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

        self.feedback = schemas.feedback.FeedbackCreate(
            feedback_type="type",
            feedback_catagory="catagory",
            feedback="feedback",
        )

        db = SessionLocal()
        crud.feedback.create_feedback(db, self.feedback, model_id=1, user_id=1)
        db.close()

    def tearDown(self):
        os.remove(f'{os.getcwd()}/tests/data/test.db')

    def test_create_feedback(self):
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

        self.feedback = schemas.feedback.FeedbackCreate(
            feedback_type="type",
            feedback_catagory="catagory",
            feedback="feedback",
        )

        db = SessionLocal()
        crud.feedback.create_feedback(db, self.feedback, model_id=2, user_id=1)
        db.close()

        db = SessionLocal()
        db_feedback = db.query(models.Feedback).filter(
            models.Feedback.id == 2
            ).first()
        db.close()

        self.assertEqual(db_feedback.model_id, 2)
        self.assertEqual(db_feedback.user_id, 1)
        
    def test_get_model_feedback(self):
        db=SessionLocal()
        db_feedback = crud.feedback.get_model_feedback(model_id=1, db=db, skip=0, limit=100)
        db.close()
        self.assertEqual(type(db_feedback), list)
        self.assertEqual(len(db_feedback), 1)
        self.assertEqual(type(db_feedback[0]), models.Feedback)
        self.assertEqual(db_feedback[0].model_id, 1)
        self.assertEqual(db_feedback[0].user_id, 1)
    
    def test_get_feedback_by_id(self):
        db=SessionLocal()
        db_feedback = crud.feedback.get_feedback_by_id(db, id=1)
        db.close()
        self.assertEqual(type(db_feedback), models.Feedback)
        self.assertEqual(db_feedback.model_id, 1)
        self.assertEqual(db_feedback.user_id, 1)
    
    def test_delete_feedback(self):
        db=SessionLocal()
        crud.feedback.delete_feedback(db, 1)
        db.close()

        db=SessionLocal()
        db_feedback = db.query(models.Feedback).offset(0).limit(100).all()
        db.close()

        self.assertListEqual(db_feedback, [])
