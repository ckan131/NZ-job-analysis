import os
import pandas as pd
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv
import pymysql


load_dotenv()
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASS")


engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')


inspector = inspect(engine)
tables = inspector.get_table_names()  


for table in tables:
    try:
        df = pd.read_sql_table(table, engine)
        df.to_csv(f"{table}.csv", index=False)
        print(f"✅ 导出成功：{table}.csv")
    except Exception as e:
        print(f"❌ 跳过表 {table}，因错误：{e}")
