# Development Server

## Prerequisite
###Postgres
- `brew install postgresql`
- `brew services start postgresql`
- `psql postgres`
- `CREATE DATABASE app;`

###Redis
- `brew install redis`
- `brew services start redis`

## Setup Virtual Environment and Installing Requirements
- Make sure the python version is 3.6
- `sh setup.sh`

## Start the server
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver`