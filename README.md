# Model-Match

Backend for model match, a web-service for hosting trained machine learning models as Docker images.

## Deployment

### Database

pull the postgres image:

`docker pull postgres:14.1`

run the image with your set password:

`docker run --name joseph -e POSTGRES_PASSWORD=1234 -d -p 5432:5432 postgres:14.1`

open CLI:

`docker exec -it joseph bash`

create the database 'joseph':

`psql -U postgres`

`create database joseph;`

### Backend

Set correct database URLs in src.alembic.ini and src.api.database.py by changing the public IP address to your public IP address

Build the docker image:

`docker build -t backend .`

Run the image:

`docker-compose up`

Add tables to the database:

`docker exec -it backend bash`

`cd app`

`alembic upgrade 8dd628a1bb2b`

`alembic upgrade 5a1457d50acc`

test at http://localhost:8000/docs
