import os
from typing import List
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
import pandas as pd
import psycopg2
from app.models.csv_schemas import DepartmentsCreate, EmployeeCreate, JobsCreate
from app.db.connection import get_db

router = APIRouter()

@router.post("/upload-employees/")
def upload_employee(data: List[EmployeeCreate]):
    insert_employee_query = """
    INSERT INTO employees (id, name, datetime, department_id, job_id) 
    VALUES (%s, %s, %s, %s, %s)
    """
    with get_db() as conn:
        with conn.cursor() as cursor:
            try :
                cursor.executemany(
                    insert_employee_query, [
                        (
                        employee.id,
                        employee.name,
                        employee.datetime,
                        employee.department_id,
                        employee.job_id,
                    )
                        for employee in data
                    ]
                ) 
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise HTTPException(status_code=500, detail=str(e))
    
    return {"message" : "Employees uploadesd successfully"}


@router.post("/upload-departments/")
def upload_department(data: List[DepartmentsCreate]):
    insert_department_query = """
    INSERT INTO departments (id, department) 
    VALUES (%s, %s)
    """

    with get_db() as conn:
        with conn.cursor() as cursor:
            try :
                for department in data:
                    query_values = (
                        department.id,
                        department.department
                    )
                    print(cursor.mogrify(insert_department_query, query_values).decode('utf-8'))
                    cursor.execute(insert_department_query,query_values)
                    conn.commit()
            except Exception as e:
                conn.rollback()
                raise HTTPException(status_code=500, detail=str(e))
    
    return {"message" : "Departments uploadesd successfully"}


@router.post('/upload-jobs/')
def upload_jobs(data: List[JobsCreate]):
    insert_jobs_query = """ 
    INSERT INTO jobs (id, job) 
    VALUES (%s, %s)
    """

    with get_db() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.executemany(
                    insert_jobs_query, [
                        (job.id,
                        job.job)
                        for job in data
                    ]
                ) 
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise HTTPException(status_code=500, detail="{e}")
            
@router.get('/employees-report/')
def get_employees_report():

    employees_report_query = ("""
    SELECT d.department, j.job,
        SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 1 THEN 1 ELSE 0 END) AS Q1,
        SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 2 THEN 1 ELSE 0 END) AS Q2,
        SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 3 THEN 1 ELSE 0 END) AS Q3,
        SUM(CASE WHEN EXTRACT(QUARTER FROM e.datetime) = 4 THEN 1 ELSE 0 END) AS Q4
    FROM employees e
    JOIN departments d ON e.department_id = d.id
    JOIN jobs j ON e.job_id = j.id
    WHERE EXTRACT(YEAR FROM e.datetime) = 2021
    GROUP BY d.department, j.job
    ORDER BY d.department, j.job
    """)
    with get_db() as conn:
        df = pd.read_sql(employees_report_query, conn)

    result = df.to_dict(orient="records")
    print(result)
        
    return result



