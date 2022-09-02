# Model-Match

Backend for Model Match, a web-service for hosting trained machine learning models as Docker images.

## Requirements

You must have docker installed and the docker daemon must be running.

## Deployment

### 1. Setting up the database

Open up the terminal and run the following commands.

pull the postgres image:

`docker pull postgres:14.1`

run the image, here I have set the name to joseph and the password to 1234:

`docker run --name joseph -e POSTGRES_PASSWORD=1234 -d -p 5432:5432 postgres:14.1`

open the database CLI:

`docker exec -it joseph bash`

create the database 'joseph':

`psql -U postgres`

`create database joseph;`

Exit out of postgres:

`exit`

exit out of the image:

`exit`

### 2. Environment variables

There are two environment variables to be set in variables.env.

DB_URL is the URL used for connecting to the database. In the 'Setting up the database' section, I set the following:

* image name: joseph
* postgres password: 1234
* database name: joseph

so in this case, I would set DB_URL to:

`DB_URL=postgresql://postgres:1234@joseph:5432/joseph`

SECRET_KEY is used for authentication. Generate a random secret key for signing tokens with:

`openssl rand -hex 32`

you should get a result that looks something like this:

`75a1d72b209d112f5c7de86445e04ccba55931c6aea94d67e5021e694d70b6a4`

Copy it into variables.env, in the case above I would set:

`SECRET_KEY=75a1d72b209d112f5c7de86445e04ccba55931c6aea94d67e5021e694d70b6a4`

The variables.env file should now look something like this:

```
DB_URL=postgresql://postgres:1234@joseph:5432/joseph
SECRET_KEY=75a1d72b209d112f5c7de86445e04ccba55931c6aea94d67e5021e694d70b6a4
```

### 4. Running the application

Run the frontend and backend images:

`docker-compose up`

The backend is now running at

http://localhost:8000/docs

however, it won't work yet as you won't be able to login! We must set up the database schema and connection.

### 5. Populate the database with the schema and admin user

Open up a new terminal window and run the following:

Add the database to the docker network:

`docker network connect network joseph`

open the backend's CLI:

`docker exec -it backend bash`

cd into app:

`cd app`

Apply the database revisions:

```
alembic upgrade 8dd628a1bb2b
alembic upgrade 5a1457d50acc
alembic upgrade a4f0943a8eec

```

Since its a closed system, and only admins can add new users, we need to add our initial admin user:

`python3 create_admin.py`


This adds a new user with the following credentials:

* username: admin
* password: 1234

exit out of the CLI:

`exit`

You're all done!

### 6. Check it.

http://localhost:8000/docs

You can now login with:

* username: admin
* password: 1234

## Testing

To test the backend open the backend's CLI:

`docker exec -it backend bash`

cd into app:

`cd app`

To run all tests:

`pytest`

To run the system tests:

`pytest tests/system_tests`

To run the unit tests:

`pytest tests/unit_tests`

NOTE: Some system tests may take a while as they are building docker images, please be patient.
