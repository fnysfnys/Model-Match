from fastapi import FastAPI, UploadFile, File
import pickle
import json
import importlib

"""
Loads the trained model into memory and supplies an endpoint for the frontend
so that the user can call the predict function on the trained model.
"""

app = FastAPI()

class ModelDataLoader():

    """
    Loads model data from the JSON file into memory on initialisation of the
    API.
    """

    def _model_data(self):
        with open("model_data.json") as f:
            model_data = json.load(f)
        return model_data
        
    def __init__(self):
        self.model_data = self._model_data()

class ConfigLoader():

    """
    Loads model config (location of predict function) into memory from the
    JSON file on initialisation of the API.
    """

    def _config(self):
        with open("config.json") as f:
            config = json.load(f)
        return config
        
    def __init__(self):
        self.config = self._config()

class ModelLoader():

    """
    Loads the trained model into memory from the pickle file on initialisation
    of the API.
    """

    def _model(self):
        with open('model', 'rb') as model_file:
            model = pickle.load(model_file)
        return model
        
    def __init__(self):
        self.model = self._model()

class PredictionLoader():

    """
    Dynamically imports the predict function from src based on it's
    location defined in the uploaded config file and loads it into memory.
    """

    def _predict_function(self):

        imported_module = importlib.import_module(
            f'src.{self.config["predict"]["module"]}', package="Model"
            ) 
        imported_class = getattr(
            imported_module, self.config["predict"]["class"]
            )
        return getattr(self.model, self.config["predict"]["function"])

    def __init__(self, model, config):
        self.model = model
        self.config = config
        self.predict_function = self._predict_function()

model_data = ModelDataLoader()
model = ModelLoader()
config = ConfigLoader()
prediction = PredictionLoader(model.model, config.config)

@app.get("/model/data")
def meta_data():

    """
    Returns the model data as JSON (name, description, VC, ...).
    """

    return model_data.model_data

@app.post("/model/predict")
def predict(file: UploadFile = File(...)):

    """
    Takes in a file as input, calls the predict function of the trained model,
    and returns it's output as JSON.
    """

    predict = prediction.predict_function
    return predict(file)

