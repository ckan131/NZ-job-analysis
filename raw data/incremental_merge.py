import os
import pandas as pd
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv
import pymysql
import datetime

# 加载环境变量
load_dotenv()
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASS")

# 创建数据库连接
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')

inspector = inspect(engine)
tables = inspector.get_table_names()

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

for table in tables:
    try:
        # 假设有created_at字段
        sql = f"SELECT * FROM {table} WHERE created_at >= '{yesterday}' AND created_at < '{today}'"
        df_incr = pd.read_sql_query(sql, engine)
        csv_path = os.path.join(os.path.dirname(__file__), f"{table}.csv")
        if os.path.exists(csv_path):
            df_full = pd.read_csv(csv_path)
            # 合并并按id去重，优先保留新数据
            df_merged = pd.concat([df_full, df_incr], ignore_index=True)
            if 'id' in df_merged.columns:
                df_merged = df_merged.drop_duplicates(subset=['id'], keep='last')
            else:
                print(f"⚠️ 表 {table} 没有'id'主键，无法去重，仅追加。")
        else:
            df_merged = df_incr.copy()
        df_merged.to_csv(csv_path, index=False)
        print(f"✅ 增量合并并保存全量：{csv_path}")
    except Exception as e:
        print(f"❌ 跳过表 {table}，因错误：{e}")
