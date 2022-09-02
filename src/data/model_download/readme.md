# Running the trained model

Thank you for downloading this model!

## Requirements

Before you start, you need to have docker installed, and the docker daemon must be running.

## Explaining the files

This directory contains 3 other files:

* [model_name].tar is the trained machine learning model docker image.

* model-frontend.tar is the frontend docker image which is what you use to interact with the model.

* docker-compose.yml is the file needed to run these two images together.

## 1. Setting up

Open your terminal and cd into this directory

## 2. Load the two images into docker

run these two commands:

`docker load -i [model_name].tar`

`docker load -i model-frontend.tar`

(These two commands load both of the docker image files onto your machine)

## 2. Run the docker-compose file

Run this command:

`docker-compose up`

(This runs the docker-compose.yml file which runs the two docker images together so that they can communicate)

## 3. Check it

You're all done! You can now view the frontend and test this model at:

http://localhost

## 4. Finishing up

When you're are done testing the model, just press ctrl+c in the terminal to stop the service, or press the stop button in the docker desktop UI.
