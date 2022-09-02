import os
from . import schemas
from distutils.dir_util import copy_tree
from shutil import copy, make_archive, rmtree
import zipfile
import yaml

"""
Copies over the backend and frontend docker image files, a docker-compose file
for running both services together, and a readme for how to run it.

zips this as a temporary file and returns the path.
"""

def update_yaml_file(temp_dir, img_name):

    """
    Updates the backend image name in the docker-compose file
    """

    yml_path = f'{temp_dir}/docker-compose.yml'

    with open(yml_path) as f:
        docker_compose = yaml.safe_load(f)

    docker_compose['services']['model']['image'] = img_name

    with open(yml_path, 'w') as f:
        yaml.dump(docker_compose, f)
    
def update_readme(temp_dir, img_name):

    """
    Updates the name of the model in the readme 
    """

    with open(f'{temp_dir}/readme.md', 'r') as file :
        filedata = file.read()

    filedata = filedata.replace('[model_name]', img_name)

    with open(f'{temp_dir}/readme.md', 'w') as file:
        file.write(filedata)

def generate_download(model: schemas.models.Model):
    model_path = model.file_path
    img_name = model.name.replace(" ", "_").lower()

    # Creates and copies over model_download into a temporary directory
    temp_dir = f'{os.getcwd()}/data/temp/{img_name}-download'
    os.mkdir(temp_dir)
    copy_tree(f'{os.getcwd()}/data/model_download/', temp_dir)

    # Copies the backend model .tar file to the temp directory
    copy(model_path, temp_dir)

    # Updates the backend image name in the docker-compose file
    update_yaml_file(temp_dir, img_name)

    # Updates the docker image name in the readme
    update_readme(temp_dir, img_name)

    # Zips this temp directory
    make_archive(temp_dir, 'zip', temp_dir)

    # Deletes temp directory
    rmtree(temp_dir)

    return f'{os.getcwd()}/data/temp/{img_name}-download.zip'
