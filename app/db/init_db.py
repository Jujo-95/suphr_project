from app.db.connection import get_db

#careate tables

def init_db():

    create_departments_table = """
    CREATE TABLE IF NOT EXISTS departments (
        id SERIAL PRIMARY KEY,
        department VARCHAR(50)
    );
    """

    create_jobs_table = """
    CREATE TABLE IF NOT EXISTS jobs (
        id SERIAL PRIMARY KEY,
        job VARCHAR(50)
    );
    """

    create_employees_table = """
    CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150),
    datetime TIMESTAMP,
    department_id INTEGER,
    job_id INTEGER
    )
    """


    with get_db() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(create_departments_table)
                cursor.execute(create_jobs_table)
                cursor.execute(create_employees_table)
                print("Tables Created successfuly")
            except Exception as e:
                print("Faield to create tables {e}")
        conn.commit()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")


