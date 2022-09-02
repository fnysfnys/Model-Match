from fastapi.testclient import TestClient
from ...api.database import engine
from ...api.main import app, get_db
import os
from ...api.models import Base
from ...api.dependencies import get_current_user, get_db

from ...api import schemas

def override_get_current_user():
    return schemas.users.User(
            email="gabrielturner@gmail.com",
            username="fnysfnys",
            permissions=2,
            id=1,
            datasets = [],
            models = [],
            feedback = [],
            downloads = [],
        )

def override_get_current_user_read_only():
    return schemas.users.User(
            email="gabrielturner@gmail.com",
            username="fnysfnys",
            permissions=0,
            id=1,
            datasets = [],
            models = [],
            feedback = [],
            downloads = [],
        )

def override_get_current_user_second_user():
    return schemas.users.User(
            email="gabrielturner@gmail.com",
            username="fnysfnys",
            permissions=0,
            id=2,
            datasets = [],
            models = [],
            feedback = [],
            downloads = [],
        )

Base.metadata.create_all(bind=engine)

test_data_path = f'{os.getcwd()}/tests/data'
data_path = f'{os.getcwd()}/data'

app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

def test_create_user():
    response = client.post(
        "api/users/create",
        json={
            "email": "test@example.com",
            "username": "test",
            "permissions": 2,
            "password": "1234"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "test"
    assert data["permissions"] == 2
    assert "id" in data
    username = data["username"]

    response = client.get(f"/api/users/{username}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "test@example.com"

def test_create_user_with_duplicate_email():
    response = client.post(
        "/api/users/create",
        json={
            "email": "test@example.com",
            "username": "test2",
            "permissions": 2,
            "password": "1234"},
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Email already registered"

def test_create_user_with_duplicate_username():
    response = client.post(
        "/api/users/create",
        json={
            "email": "test2@example.com",
            "username": "test",
            "permissions": 2,
            "password": "1234"},
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Username already registered"

def test_user_me():
    response = client.get("/api/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "fnysfnys"
    assert data["email"] == "gabrielturner@gmail.com"
    assert data["permissions"] == 2

def test_dataset_upload_read_only():

    app.dependency_overrides[get_current_user] = override_get_current_user_read_only
    
    dataset = {"name": "test dataset", "description": "this is a test"}

    with open(f"{test_data_path}/mock_dataset.zip", "rb") as f:
        data = f.read()
    files = {"file": ("file", data, "zip")}

    response = client.post("/api/datasets/upload", data=dataset, files=files)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Unauthorised"

    app.dependency_overrides[get_current_user] = override_get_current_user

def test_dataset_upload():
    dataset = {"name": "test dataset", "description": "this is a test"}

    with open(f"{test_data_path}/mock_dataset.zip", "rb") as f:
        data = f.read()
    files = {"file": ("file", data, "zip")}

    response = client.post("/api/datasets/upload", data=dataset, files=files)
    assert response.status_code == 200
    assert os.path.exists(f"{data_path}/datasets/test-dataset.zip")
    data = response.json()
    assert data["name"] == "test dataset"
    assert data["description"] == "this is a test"
    assert os.path.exists(data["file_path"])

def test_dataset_upload_with_duplicate_name():
    dataset = {"name": "test dataset", "description": "this is a test"}

    with open(f"{test_data_path}/mock_dataset.zip", "rb") as f:
        data = f.read()
    files = {"file": ("file", data, "zip")}

    response = client.post("/api/datasets/upload", data=dataset, files=files)
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Name already registered"

def test_get_datasets():
    response = client.get(f"/api/datasets/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "test dataset"
    assert data[0]["description"] == "this is a test"
    assert os.path.exists(data[0]["file_path"])
    assert data[0]["user_id"] == override_get_current_user().id

def test_get_dataset_by_id():
    response = client.get(f"/api/datasets/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "test dataset"
    assert data["description"] == "this is a test"
    assert os.path.exists(data["file_path"])
    assert data["user_id"] == override_get_current_user().id

def test_get_dataset_by_non_existent_id():
    response = client.get(f"/api/datasets/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Dataset not found"

def test_download_dataset():
    response = client.get(f"/api/datasets/1/download")
    assert response.status_code == 200

def test_download_non_existent_dataset():
    response = client.get(f"/api/datasets/2/download")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Dataset not found"

def test_delete_non_existent_dataset():
    response = client.delete(f"/api/datasets/2/delete")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Dataset not found"

def test_delete_dataset_uploaded_by_other_user():

    app.dependency_overrides[get_current_user] = override_get_current_user_second_user

    response = client.delete(f"/api/datasets/1/delete")
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Unauthorised"

    app.dependency_overrides[get_current_user] = override_get_current_user

def test_delete_dataset():
    response = client.delete(f"/api/datasets/1/delete")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["ok"]
    assert response.status_code == 200
    assert not os.path.exists(f"{data_path}/datasets/test-dataset.zip")

def test_dataset_upload_read_only():

    app.dependency_overrides[get_current_user] = override_get_current_user_read_only
    
    model = {
        "name":"dummy-model",
        "description":"this is a dummy model",
        "version_control":"some vc",
        "release_terms":"some release terms",
        "outcome":"some outcome",
        "output":"some output",
        "output_to_trigger":"some ott",
        "target_population":"some target population",
        "time_of_prediction":"some time of prediction",
        "input_data_source":"some input data source",
        "input_data_type":"some input data type",
        "training_details":"some training details",
        "model_type":"some model type"
        }

    with open(f"{test_data_path}/dummy_model/requirements.txt", "rb") as f:
        requirements = f.read()
    with open(f"{test_data_path}/dummy_model/src.zip", "rb") as f:
        source_code = f.read()
    with open(f"{test_data_path}/dummy_model/model", "rb") as f:
        pickle = f.read()
    with open(f"{test_data_path}/dummy_model/config.json", "rb") as f:
        config = f.read()

    files = {
        "requirements": ("requirements", requirements, "txt"),
        "source_code": ("source_code", source_code, "zip"),
        "pickle": ("requirements", pickle, "pickle"),
        "config": ("config", config, "json"),
        }

    response = client.post("/api/models/upload", data=model, files=files)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Unauthorised"

    app.dependency_overrides[get_current_user] = override_get_current_user

def test_model_upload():
    model = {
        "name":"dummy-model",
        "description":"this is a dummy model",
        "version_control":"some vc",
        "release_terms":"some release terms",
        "outcome":"some outcome",
        "output":"some output",
        "output_to_trigger":"some ott",
        "target_population":"some target population",
        "time_of_prediction":"some time of prediction",
        "input_data_source":"some input data source",
        "input_data_type":"some input data type",
        "training_details":"some training details",
        "model_type":"some model type"
        }

    with open(f"{test_data_path}/dummy_model/requirements.txt", "rb") as f:
        requirements = f.read()
    with open(f"{test_data_path}/dummy_model/src.zip", "rb") as f:
        source_code = f.read()
    with open(f"{test_data_path}/dummy_model/model", "rb") as f:
        pickle = f.read()
    with open(f"{test_data_path}/dummy_model/config.json", "rb") as f:
        config = f.read()

    files = {
        "requirements": ("requirements", requirements, "txt"),
        "source_code": ("source_code", source_code, "zip"),
        "pickle": ("requirements", pickle, "pickle"),
        "config": ("config", config, "json"),
        }

    response = client.post("/api/models/upload", data=model, files=files)
    
    assert response.status_code == 200
    assert os.path.exists(f"{data_path}/models/dummy-model.tar")
    data = response.json()
    assert data["name"] == "dummy-model"
    assert data["description"] == "this is a dummy model"
    assert os.path.exists(data["file_path"])

def test_model_upload_with_duplicate_name():
    model = {
        "name":"dummy-model",
        "description":"this is a dummy model",
        "version_control":"some vc",
        "release_terms":"some release terms",
        "outcome":"some outcome",
        "output":"some output",
        "output_to_trigger":"some ott",
        "target_population":"some target population",
        "time_of_prediction":"some time of prediction",
        "input_data_source":"some input data source",
        "input_data_type":"some input data type",
        "training_details":"some training details",
        "model_type":"some model type"
        }

    with open(f"{test_data_path}/dummy_model/requirements.txt", "rb") as f:
        requirements = f.read()
    with open(f"{test_data_path}/dummy_model/src.zip", "rb") as f:
        source_code = f.read()
    with open(f"{test_data_path}/dummy_model/model", "rb") as f:
        pickle = f.read()
    with open(f"{test_data_path}/dummy_model/config.json", "rb") as f:
        config = f.read()

    files = {
        "requirements": ("requirements", requirements, "txt"),
        "source_code": ("source_code", source_code, "zip"),
        "pickle": ("requirements", pickle, "pickle"),
        "config": ("config", config, "json"),
        }

    response = client.post("/api/models/upload", data=model, files=files)
    
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Name already registered"

def test_get_models():
    response = client.get(f"/api/models/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "dummy-model"
    assert data[0]["description"] == "this is a dummy model"
    assert os.path.exists(data[0]["file_path"])
    assert data[0]["user_id"] == override_get_current_user().id

def test_get_model_by_id():
    response = client.get(f"/api/models/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "dummy-model"
    assert data["description"] == "this is a dummy model"
    assert os.path.exists(data["file_path"])
    assert data["user_id"] == override_get_current_user().id

def test_get_non_existent_model_by_id():
    response = client.get(f"/api/models/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Model not found"

def test_download_non_existent_model():
    response = client.get(f"/api/models/2/download")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Model not found"

def test_model_download():
    response = client.get(f"/api/models/1/download")
    assert response.status_code == 200

def test_my_downloads():
    response = client.post(f"/api/users/my-downloads")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["name"] == "dummy-model"

def test_submitting_feedback():
    response = client.post(
        "/api/feedback/1/submit-feedback",
        json={
            "feedback_type":"type",
            "feedback_catagory":"catagory",
            "feedback":"good"
        }
        )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["feedback_type"] == "type"
    assert data["feedback_catagory"] == "catagory"
    assert data["feedback"] == "good"
    assert data["model_id"] == 1
    assert data["user_id"] == override_get_current_user().id

def test_submitting_feedback_on_non_existent_model():
    response = client.post(
        "/api/feedback/2/submit-feedback",
        json={
            "feedback_type":"type",
            "feedback_catagory":"catagory",
            "feedback":"good"
        }
        )
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Model not found"

def test_get_model_feedback():
    response = client.get("/api/feedback/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 1
    assert data[0]["feedback_type"] == "type"
    assert data[0]["feedback_catagory"] == "catagory"
    assert data[0]["feedback"] == "good"
    assert data[0]["model_id"] == 1
    assert data[0]["user_id"] == override_get_current_user().id

def test_delete_non_existent_feedback():
    response = client.delete(f"/api/feedback/delete-feedback?feedback_id=2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Feedback not found"

def test_delete_feedback_uploaded_by_other_user():

    app.dependency_overrides[get_current_user] = override_get_current_user_second_user

    response = client.delete(f"/api/feedback/delete-feedback?feedback_id=1")
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Unauthorised"

    app.dependency_overrides[get_current_user] = override_get_current_user

def test_delete_feedback():
    response = client.delete(f"/api/feedback/delete-feedback?feedback_id=1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["ok"]
    assert response.status_code == 200

def test_get_model_feedback_for_non_existent_model():
    response = client.get("/api/feedback/2")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Model not found"

def test_delete_non_existent_model():
    response = client.delete(f"/api/models/2/delete")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Model not found"

def test_delete_model_uploaded_by_other_user():

    app.dependency_overrides[get_current_user] = override_get_current_user_second_user

    response = client.delete(f"/api/models/1/delete")
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Unauthorised"

    app.dependency_overrides[get_current_user] = override_get_current_user

def test_delete_model():
    response = client.delete(f"/api/models/1/delete")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["ok"]
    assert response.status_code == 200
    assert not os.path.exists(f"{data_path}/models/dummy-model.tar")
    os.remove(f'{test_data_path}/test.db')
