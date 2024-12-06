# Facultad de Ingeniería en Ciencias Aplicadas (FICA)

# Tesis

## Team members

- [x] _Ramirez Henry_
- [x] _Chancosi Mateo_

## How to run the project

1. Clone this repository

```bash
git clone https://github.com/on-brulera/utn-encuesta-services
```

2. Prepare enviroment

```bash
#Create a virtualenv with Python 3.11.7
py -3 -m venv .venv
#Activate virtualenv
.venv\Scripts\activate
```
3. Copy .env-template and to the copy rename to .env and configurated your variables

4. Install flask dependencies

```bash
pip install -r requirements.txt
```

5. Install container

```bash
docker-compose up -d
#To access to postgres comand line
docker exec -it postgresql bash
psql -h localhost -U postgres
```

6. Configurate flask variable to run

```bash
# on windows
set FLASK_APP=entrypoint:app
set FLASK_ENV=development
set APP_SETTINGS_MODULE=config.default

#or maybe

$env:FLASK_APP = "entrypoint:app"
$env:FLASK_ENV = "development"
$env:APP_SETTINGS_MODULE = "config.default"

7. Migrate Database

```bash
#if is the first migration
flask db init
#Run These commands to update any change in database
flask db migrate
flask db upgrade

```

8. Run backend

```bash
#TO RUN PROJECT the Variable migth to be: FLASK_APP=main.py
flask run
```

9. Test Service

```bash
http://localhost:5000/ #Is a simple example about your server
```
