import pymysql
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# โหลดค่าจากไฟล์ .env เพื่อความปลอดภัย
# ตัวอย่างไฟล์ .env
# DB_HOST=localhost
# DB_USER=admin
# DB_PASSWORD=123456
# DB_NAME=hosxp
# DB_PORT=3306
load_dotenv()

# 1. ตั้งค่าการเชื่อมต่อฐานข้อมูลจาก Environment Variables
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'hosxp'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'charset': 'utf8'
}

def export_data_for_ai_audit():
    
    conn = None
    try:
        # 2. เชื่อมต่อ MySQL
        print("Connecting to the database for AI data export...")
        conn = pymysql.connect(**db_config)
        print("Connection successful.")

        # 3. SQL Query
        sql_query = """
        SELECT
            p.hn,                       -- Pseudonym
            p.sex,                      -- เพศ
            p.birth,                    -- วันเกิด (คำนวณอายุ)
            p.typelive,                 -- ประเภทที่อยู่อาศัย
            v.villname AS village_name  -- ระดับหมู่บ้าน
        FROM
            person p
        INNER JOIN house h ON p.hcode = h.hcode
        INNER JOIN village v 
            ON h.pcucode = v.pcucode 
            AND h.villcode = v.villcode
        WHERE
            p.typelive IN (1, 3)
            AND p.dischargetype = '9'
        """

        # 4. ดึงข้อมูลเข้า Pandas DataFrame
        print("Executing query and fetching data...")
        df = pd.read_sql(sql_query, conn)
        print(f"Fetched {len(df)} records for AI audit.")

        if df.empty:
            print("No data found matching the criteria. Exiting.")
            return

        # --- [ 5. Data Transformation ] ---

        # แปลงเพศ
        df['gender'] = df['sex'].replace({
            1: 'Male',
            2: 'Female',
            '1': 'Male',
            '2': 'Female'
        })

        # คำนวณอายุ
        birth_dates = pd.to_datetime(df['birth'], errors='coerce')
        current_year = datetime.now().year
        df['age'] = current_year - birth_dates.dt.year

        # จัดการค่าว่าง
        df['age'] = df['age'].fillna(0).astype(int)

        # เลือกและเปลี่ยนชื่อคอลัมน์สำหรับส่งออก
        final_columns = {
            'hn': 'patient_id',
            'age': 'age',
            'gender': 'gender',
            'typelive': 'residence_type',
            'village_name': 'village_name'
        }
        df_final = df[list(final_columns.keys())].rename(columns=final_columns)

        # 6. ส่งออกเป็น CSV
        filename = "ai_audit_patient_data.csv"
        df_final.to_csv(filename, index=False, encoding='utf-8-sig')

        print(
            "-" * 40,
            "Successfully exported data for AI audit",
            f"File: {filename}",
            f"Columns: {list(df_final.columns)}",
            "-" * 40,
            sep="\n"
        )

    except pymysql.Error as db_err:
        print(f"Database Error: {db_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    export_data_for_ai_audit()
