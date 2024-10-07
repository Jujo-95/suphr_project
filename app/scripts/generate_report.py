

import numpy as np
import pandas as pd
import requests


def employees_report():
    url = "http://127.0.0.1:8000/employees-report"
    response = requests.get(url)
    print(response.json())

def hiring_report():
    url = "http://127.0.0.1:8000/hiring-kpi"
    response = requests.get(url)
    print(response.json())


if __name__ == "__main__":
    employees_report()
    hiring_report()