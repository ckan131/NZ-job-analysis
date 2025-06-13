import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 从环境变量中读取数据库信息
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASS")

# 创建数据库连接
try:
    engine = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{database}')
    df = pd.read_sql('SELECT * FROM job_positions LIMIT 5;', con=engine)
    print(df)
except Exception as e:
    print("Error message")
    print(e)
