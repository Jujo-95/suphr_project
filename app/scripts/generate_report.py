

import numpy as np
import pandas as pd
import requests


def employees_report():
    url = "http://127.0.0.1:8000/employees-report"
    response = requests.get(url)
    print(response.json())

employees_report()