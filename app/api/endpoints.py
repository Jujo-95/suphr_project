import os
from typing import List
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
import pandas as pd
import psycopg2
from app.models.csv_schemas import DepartmentsCreate, EmployeeCreate, JobsCreate
from app.db.connection import get_db
from app.db.migrate_tables import upload_employees as migrate_upload_employees, upload_department as migrate_upload_department, upload_jobs as migrate_upload_jobs

router = APIRouter()

@router.post("/upload-employees/")
def upload_employee(data: List[EmployeeCreate]):
    insert_employee_query = """
    INSERT INTO employees (id, name, datetime, department_id, job_id) 
    VALUES (%s, %s, %s, %s, %s)
    """
    
    print('tis has been executed')
    with get_db() as conn:
        with conn.cursor() as cursor:
            try :
                for employee in data:
                    query_values = (
                        employee.id,
                        employee.name,
                        employee.datetime,
                        employee.department_id,
                        employee.job_id,
                    )
                    cursor.execute(
                        insert_employee_query,query_values
                    ) 
                print(cursor.mogrify(insert_employee_query, query_values).decode('utf-8'))
                conn.commit()
                return {"message" : "Employees uploadesd successfully {}"}
            except Exception as e:
                conn.rollback()
                exeption = HTTPException(status_code=500, detail=str(e))
                return {"message" : f"failed {exeption}"}
            
    


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

@router.get('/hiring-kpi/')
def get_hiring_kpi_report():
    hiring_kpi_query = """
    WITH department_hiring AS (
        SELECT d.id, d.department, COUNT(e.id) AS hired
        FROM employees e
        JOIN departments d ON e.department_id = d.id
        WHERE EXTRACT(YEAR FROM e.datetime) = 2021
        GROUP BY d.id, d.department
    )
    SELECT id, department, hired
    FROM department_hiring
    WHERE hired > (SELECT AVG(hired) FROM department_hiring)
    ORDER BY hired DESC
    """

    with get_db() as conn:
        df_kpi = pd.read_sql(hiring_kpi_query,conn)

    hiring_kpi_results = df_kpi.to_dict(orient='records')

    return hiring_kpi_results

@router.post('/run-local-migration/')
def run_local_migration():

    try:

        migrate_upload_employees()
        migrate_upload_department()
        migrate_upload_jobs()

        result = {"message":f"Migration run successfully"}
        return result

    except Exception as e:
        result = {"message":f"{e}"}
        return result



