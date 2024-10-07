import pandas as pd
import requests
import json
from datetime import datetime
import numpy as np


def process_employees_data(df_employees):

    #process raw data
    df_employees["id"] = df_employees["id"].fillna(0).astype(int)
    df_employees["name"] = df_employees["name"].astype(str).fillna('')
    df_employees["department_id"] = df_employees["department_id"].fillna(0).astype(int)
    df_employees["job_id"] = df_employees["job_id"].fillna(0).astype(int)
    df_employees['datetime'] = pd.to_datetime(df_employees['datetime'], errors='coerce')  
    df_employees['datetime'] = df_employees['datetime'].fillna(pd.NaT).apply(lambda x: x.isoformat() if pd.notna(x) else None)

    return df_employees.to_dict(orient='records')




def upload_employees():
    csv_location = f"app/data/hired_employees.csv"
    url = "http://127.0.0.1:8000/upload-employees"

    column_names = ["id", "name", "datetime", "department_id", "job_id"]
    employees = pd.read_csv(csv_location, names=column_names, header=None, index_col=None)

    preprocessed_employees = process_employees_data(employees)

    response = requests.post(url, json=preprocessed_employees)
    print(response.json())
    

def upload_department():
    csv_location = f"app/data/departments.csv"
    url = "http://127.0.0.1:8000/upload-departments"
    column_names = ["id", "department"]
    departments = pd.read_csv(csv_location, names=column_names, header=None, index_col=None)
    departments_head = departments.to_dict(orient='records')
    print(departments_head)
    response = requests.post(url, json=departments_head)
    print(response.json())

def upload_jobs():
    csv_location = f"app/data/jobs.csv"
    url = "http://127.0.0.1:8000/upload-jobs"
    column_names = ["id", "job"]
    employees = pd.read_csv(csv_location, names=column_names, header=None, index_col=None)
    employees_head = employees.to_dict(orient='records')
    print(employees_head)
    response = requests.post(url, json=employees_head)
    print(response.json())


if __name__ == "__main__":
    upload_jobs()
    upload_department()
    upload_employees()