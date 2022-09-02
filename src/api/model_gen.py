import os
import json
import subprocess
from fastapi.encoders import jsonable_encoder
from zipfile import ZipFile
from distutils.dir_util import copy_tree
from shutil import rmtree

"""
Copies the uploaded files required for building the image:

* requirements.txt - (requirements needed for model)
* src.zip - (zipped source code)
* pickle - (pickle of the trained model)
* Config.json - (location of predict function)

into a temporary directory aswell as a docker file and api which supports
calls to the trained model.

Builds the image and stores as a .tar in ./data/models.
"""

def write_file(file, file_path):
    with open(file_path,'wb+') as f:
        f.write(file.file.read())
        f.close()

def write_model_data(model_data, temp_dir): 

    """
    write model data (name, description, VC,...) as a JSON to a file which
    will be loaded into memory when the docker image is run.
    """

    json_model_data = jsonable_encoder(model_data)
    with open(f'{temp_dir}/model_data.json', 'w') as outfile:
        json.dump(json_model_data, outfile)

def write_requirements(requirements, temp_dir):

    """
    Writes the requirements needed for the API aswell as the user
    specified requirements.
    """

    requirements_path = f'{temp_dir}/requirements.txt'
    
    with open(requirements_path,'wb+') as f:
        # Add requirements for api
        f.write("FastAPI==0.70.0\n".encode('utf-8'))
        f.write("uvicorn==0.15.0\n".encode('utf-8'))
        f.write("python-multipart==0.0.5\n".encode('utf-8'))
        
        # Add user-specified requirements
        f.write(requirements.file.read())
        f.close()

def write_source_code(source_code, temp_dir):

    """
    Saves the zip file of the source code to the temporary build directory,
    unzips, and adds __init__.py if none given, allowing the function to
    be dynamically imported.
    """

    #Writes the zipped source code to the temp directory
    file_path = f'{temp_dir}/src.zip'
    write_file(source_code, file_path)

    #unzips source code
    with ZipFile(file_path,"r") as zip_ref:   
        zip_ref.extractall(f'{temp_dir}/')

    #adds __init__.py to ./src
    with open(f'{temp_dir}/src/__init__.py','w+') as f:
        f.close()

def generate_model(temp_dir, img_name):

    """
    Builds the docker image, saves it to ./data/models as a .tar file, removes
    the image binary from the machine.

    Returns the file path of the model .tar file to be written into the db.
    """

    # Where the model will be saved to
    file_path = f'{os.getcwd()}/data/models/{img_name}.tar'

    # Builds the docker image
    subprocess.run(
        ['docker',
        'build',
        '-t',
        img_name,
        temp_dir])

    # Save as a .tar file to ./data/models
    subprocess.run(['docker', 'save', '-o', file_path, img_name])
    
    # Remove docker image binary
    subprocess.run(['docker', 'rmi', img_name])

    return file_path

def create_model(model_data, requirements, source_code, pickle, config):
    
    img_name = model_data.name.replace(" ", "_").lower()

    """
    Copies model_gen into a new temp directory where the required files
    for building the image to host the trained model will be copied to
    """

    temp_dir = f'{os.getcwd()}/data/temp/{img_name}-model-gen'
    os.mkdir(temp_dir)
    os.mkdir(f'{temp_dir}/__pycache__')
    copy_tree(f'{os.getcwd()}/data/model_gen/', temp_dir)

    # Writes files necissary for serving model requests to the frontend.
    write_model_data(model_data, temp_dir)
    write_requirements(requirements, temp_dir)
    write_source_code(source_code, temp_dir)
    write_file(pickle, f'{temp_dir}/model')
    write_file(config, f'{temp_dir}/config.json')

    file_path = generate_model(temp_dir, img_name)
    
    # Removes temporary build directory
    rmtree(temp_dir)

    return file_path
