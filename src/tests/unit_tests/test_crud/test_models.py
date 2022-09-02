import unittest

from ....api import models, crud, schemas, auth
from ....api.database import SessionLocal, engine
from fastapi import Depends
from ....api.models import Base
import os

class TestModels(unittest.TestCase):
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

    def tearDown(self):
        os.remove(f'{os.getcwd()}/tests/data/test.db')
        
    def test_create_model(self):
        new_model = schemas.models.ModelCreate(
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
        crud.models.create_model(db, new_model, file_path="/", user_id=1)
        db.close()

        db = SessionLocal()
        db_model = db.query(models.Model).filter(
            models.Model.id == 2
            ).first()
        db.close()

        self.assertEqual(type(db_model), models.Model)
        self.assertEqual(db_model.name, new_model.name)
        self.assertEqual(db_model.description, new_model.description)
        self.assertEqual(db_model.version_control, new_model.version_control)
        self.assertEqual(db_model.release_terms, new_model.release_terms)
        self.assertEqual(db_model.outcome, new_model.outcome)
        self.assertEqual(db_model.output, new_model.output)
        self.assertEqual(db_model.output_to_trigger, new_model.output_to_trigger)
        self.assertEqual(db_model.target_population, new_model.target_population)
        self.assertEqual(db_model.time_of_prediction, new_model.time_of_prediction)
        self.assertEqual(db_model.input_data_source, new_model.input_data_source)
        self.assertEqual(db_model.input_data_type, new_model.input_data_type)
        self.assertEqual(db_model.training_details, new_model.training_details)
        self.assertEqual(db_model.model_type, new_model.model_type)
        self.assertEqual(db_model.file_path, "/")
        self.assertEqual(db_model.user_id, 1)
    
    def test_get_model_by_name(self):
        db = SessionLocal()
        db_model = crud.models.get_model_by_name(db, self.model.name)
        db.close()

        self.assertEqual(type(db_model), models.Model)
        self.assertEqual(db_model.name, self.model.name)
        self.assertEqual(db_model.description, self.model.description)
        self.assertEqual(db_model.version_control, self.model.version_control)
        self.assertEqual(db_model.release_terms, self.model.release_terms)
        self.assertEqual(db_model.outcome, self.model.outcome)
        self.assertEqual(db_model.output, self.model.output)
        self.assertEqual(db_model.output_to_trigger, self.model.output_to_trigger)
        self.assertEqual(db_model.target_population, self.model.target_population)
        self.assertEqual(db_model.time_of_prediction, self.model.time_of_prediction)
        self.assertEqual(db_model.input_data_source, self.model.input_data_source)
        self.assertEqual(db_model.input_data_type, self.model.input_data_type)
        self.assertEqual(db_model.training_details, self.model.training_details)
        self.assertEqual(db_model.model_type, self.model.model_type)
        self.assertEqual(db_model.file_path, "/")
        self.assertEqual(db_model.user_id, 1)

    def test_get_model_by_id(self):
        db = SessionLocal()
        db_model = crud.models.get_model_by_id(db, 1)
        db.close()

        self.assertEqual(type(db_model), models.Model)
        self.assertEqual(db_model.name, self.model.name)
        self.assertEqual(db_model.description, self.model.description)
        self.assertEqual(db_model.version_control, self.model.version_control)
        self.assertEqual(db_model.release_terms, self.model.release_terms)
        self.assertEqual(db_model.outcome, self.model.outcome)
        self.assertEqual(db_model.output, self.model.output)
        self.assertEqual(db_model.output_to_trigger, self.model.output_to_trigger)
        self.assertEqual(db_model.target_population, self.model.target_population)
        self.assertEqual(db_model.time_of_prediction, self.model.time_of_prediction)
        self.assertEqual(db_model.input_data_source, self.model.input_data_source)
        self.assertEqual(db_model.input_data_type, self.model.input_data_type)
        self.assertEqual(db_model.training_details, self.model.training_details)
        self.assertEqual(db_model.model_type, self.model.model_type)
        self.assertEqual(db_model.file_path, "/")
        self.assertEqual(db_model.user_id, 1)
    
    def test_get_datasets(self):
        db=SessionLocal()
        db_models = crud.models.get_models(db, 0, 100)
        db.close()
        self.assertEqual(type(db_models), list)
        self.assertEqual(len(db_models), 1)
        self.assertEqual(type(db_models[0]), models.Model)
        self.assertEqual(db_models[0].name, self.model.name)
        self.assertEqual(db_models[0].description, self.model.description)
        self.assertEqual(db_models[0].version_control, self.model.version_control)
        self.assertEqual(db_models[0].release_terms, self.model.release_terms)
        self.assertEqual(db_models[0].outcome, self.model.outcome)
        self.assertEqual(db_models[0].output, self.model.output)
        self.assertEqual(db_models[0].output_to_trigger, self.model.output_to_trigger)
        self.assertEqual(db_models[0].target_population, self.model.target_population)
        self.assertEqual(db_models[0].time_of_prediction, self.model.time_of_prediction)
        self.assertEqual(db_models[0].input_data_source, self.model.input_data_source)
        self.assertEqual(db_models[0].input_data_type, self.model.input_data_type)
        self.assertEqual(db_models[0].training_details, self.model.training_details)
        self.assertEqual(db_models[0].model_type, self.model.model_type)
        self.assertEqual(db_models[0].file_path, "/")
        self.assertEqual(db_models[0].user_id, 1)

    def test_delete_dataset(self):
        db=SessionLocal()
        crud.models.delete_model(db, 1)
        db.close()

        db=SessionLocal()
        db_model = db.query(models.Model).offset(0).limit(100).all()
        db.close()

        self.assertListEqual(db_model, [])
