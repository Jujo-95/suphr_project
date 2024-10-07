# suphr_project
this project consists of an entire HR solution called suphr stands for "SUPER HUMAN RESOURCES"

### Steps (local run)

## prerequisites:
    - Python
    - postgresql 
    - git

## 1. create and activate a python venv:
    python -m venv env
    .\env\Scripts\activate

## 2. clone and enter the repo :
    git clone "<this repo url>"
    cd suphr_project

## 3. install requirements:
    python -m pip install -r requirements.txt

## 4. create an .env file with the credentials of the postgresql database:
    DATABASE_HOST="localhost"
    DATABASE_NAME="suphr_dev"
    DATABASE_USER="<user>"
    DATABASE_PASSWORD="<password>"

## 5. run the app (at the root of the repo):
    python -m uvicorn app.main:app


## 6. migrate csv files:
    python .\app\db\migrate_tables.py

## 7. run reports
    python .\app\scripts\generate_report.py        


### Steps (Docker run)

## prerequisites:
    - docker Desktop (Windows) or docker app installed on linux
    - git

## Step 1. clone and enter the repo :
    git clone "<this repo url>"
    cd suphr_project

## 2. create an .env file with the credentials of the postgresql database:
    DATABASE_NAME="suphr_dev"
    DATABASE_USER="<user>"
    DATABASE_PASSWORD="<password>"

## 5 build the app:
    docker compose up --build

## 6 when succcess:
    open explorer on url = localhost:8000

## 7 check migration
    docker exec -it postgres_db psql -U <user> -d <password> 
