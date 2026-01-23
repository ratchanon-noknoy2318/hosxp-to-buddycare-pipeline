import os
import pandas as pd
from sqlalchemy import create_engine
import urllib.parse

# Database Configuration
# Ideally, load these from environment variables or a secure config file
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'sa')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'sa')
DB_NAME = os.getenv('DB_NAME', 'hosxp')
DB_PORT = os.getenv('DB_PORT', '3306')

def extract_patient_data():
    """
    Connects to the HOSxP database and extracts patient data.
    """
    try:
        # Create SQLAlchemy engine (MySQL/MariaDB compatible)
        # Ensure you have pymysql installed: pip install pymysql
        encoded_password = urllib.parse.quote_plus(DB_PASSWORD)
        connection_string = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
        engine = create_engine(connection_string)

        # SQL Query
        sql_query = """
        SELECT
          CASE WHEN p.sex = 1 THEN '003'
               WHEN p.sex = 2 THEN '004'
           END AS 'คำนำหน้า',
          p.fname AS "ชื่อ",
          p.lname AS "นามสกุล",
          p.sex AS "เพศ",
          RIGHT(CONCAT('0', DAY(p.birthdate)), 2) AS "วันเกิด",
          RIGHT(CONCAT('0', MONTH(p.birthdate)), 2) AS "เดือนเกิด",
          YEAR(p.birthdate) AS "ปีเกิด",
          p.cid AS "เลขบัตรประชาชน",
          p.house_regist_type_id AS "ประเภทที่อยู่อาศัย",
          CONCAT(v.address_id, RIGHT(CONCAT('0', v.village_moo), 2)) AS "เลขที่อยู่อาศัย",
          v.village_name AS "ชื่อหมู่บ้าน",
          REGEXP_REPLACE(h.address, '[^0-9]', '') AS "บ้านเลขที่",
          h.road AS "ชื่อถนน"
        FROM person p
        LEFT JOIN pname p2 ON p.pname = p2.`name`
        LEFT JOIN house h ON p.house_id = h.house_id
        LEFT JOIN village v ON h.village_id = v.village_id
        LEFT JOIN patient p3 ON p.patient_hn = p3.hn
        WHERE p.house_regist_type_id IN (1, 3) 
          AND v.village_moo <> 0 
          AND p.nationality = 99 
          AND p.person_discharge_id = 9
          AND p.birthdate IS NOT NULL;
        """

        # Execute query
        df = pd.read_sql(sql_query, engine)
        return df

    except Exception as e:
        print(f"Error extracting data: {e}")
        return None

if __name__ == "__main__":
    df = extract_patient_data()
    if df is not None:
        print(f"Extracted {len(df)} records.")
        print(df.head())