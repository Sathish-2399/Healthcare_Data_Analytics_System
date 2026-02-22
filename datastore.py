import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("Healthcare_Transformed.csv")

username = "root"
password = "Sathish3718"
host = "localhost"
port = "3306"
database = "healthcare_db"
engine = create_engine(
    f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
)

df.to_sql(
    name="healthcare_data",
    con=engine,
    if_exists="replace",
    index=False
)

print("Data successfully loaded into MySQL")
