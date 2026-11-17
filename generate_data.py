from sqlalchemy import create_engine
import pandas as pd
import random
from datetime import datetime, timedelta

engine = create_engine(
    "postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/odis_scaffold"
)

employees = pd.DataFrame(
    {
        "employee_name":
        [f"Employee {i}" for i in range(1, 1001)]
    }
)

employees.to_sql(
    "dim_employee",
    engine,
    if_exists="append",
    index=False
)

print("1000 Employees Created")