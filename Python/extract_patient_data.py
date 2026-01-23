import pymysql
import pandas as pd
from datetime import datetime

# 1. ตั้งค่าการเชื่อมต่อฐานข้อมูล
db_config = {
    'host': 'localhost',
    'user': 'admin',
    'password': '123456',
    'database': 'hosxp',
    'port': 3306,
    'charset': 'utf8'
}
def test_connection():
    # Database configuration
    db_config = {
        'host': 'localhost',
        'user': 'admin',
        'password': '123456',
        'database': 'hosxp',
        'port': 3306,
        'charset': 'utf8'
    }

def export_full_report():
    conn = None
    try:
        # 2. เชื่อมต่อ MySQL
        print("Connecting to Database...")
        print("Connecting to database...")
        conn = pymysql.connect(**db_config)
        
        # 3. SQL Query (ชุดที่คุณให้มา)
        sql_query = """
        SELECT
            person.prename AS `คํานําหน้า`,
            person.fname AS `ชื่อ`,
            person.lname AS `นามสกุล`,
            person.sex AS `เพศ`,
            right(birth,2) AS `วันเกิด`,
            mid(birth,6,2) AS `เดือนเกิด`,
            YEAR(birth) AS `ปีเกิด`,
            person.idcard AS `เลขบัตรประชาชน`,
            person.typelive AS `ประเภทที่อยู่อาศัย`,
            house.villcode AS `เลขที่อยู่อาศัย`,
            village.villname AS `ชื่อหมู่บ้าน`,
            person.hnomoi AS `บ้านเลขที่`,
            house.road AS `ชื่อถนน`,
            house.xgis AS `ละติจูด`,
            house.ygis AS `ลองติจูด`
        FROM
            person
        INNER JOIN house ON person.hcode = house.hcode
        INNER JOIN village ON house.pcucode = village.pcucode AND house.villcode = village.villcode
        WHERE
            person.typelive IN(1,3) AND
            person.dischargetype = '9'
        """
        
        # 4. ดึงข้อมูลเข้า Pandas DataFrame
        df = pd.read_sql(sql_query, conn)
        print(f"ดึงข้อมูลมาได้ทั้งหมด: {len(df)} รายการ")
        print("Connection successful!")

        # --- [ 5. ส่วนจัดการข้อมูล (Data Transformation) ] ---
        
        # ก. รวมชื่อ-นามสกุล และลบช่องว่าง
        df['ชื่อ-นามสกุล'] = df['ชื่อ'].str.strip() + " " + df['นามสกุล'].str.strip()
        
        # ข. แปลงเพศ 1, 2 เป็น ชาย, หญิง
        df['เพศ'] = df['เพศ'].replace({1: 'ชาย', 2: 'หญิง', '1': 'ชาย', '2': 'หญิง'})
        
        # ค. คำนวณอายุ (ปีปัจจุบัน - ปีเกิด)
        this_year = datetime.now().year + 543  # ใช้ปี พ.ศ.
        df['อายุ'] = this_year - df['ปีเกิด'].fillna(this_year).astype(int)
        
        # ง. จัดการค่าว่าง (Null) ให้ดูสวยงาม
        df['ชื่อถนน'] = df['ชื่อถนน'].fillna('-')
        df['ละติจูด'] = df['ละติจูด'].fillna(0)
        df['ลองติจูด'] = df['ลองติจูด'].fillna(0)
        with conn.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"Database version: {version[0]}")

        # จ. เลือกและเรียงลำดับคอลัมน์ที่จะเอาลง Excel
        final_columns = [
            'คํานําหน้า', 'ชื่อ-นามสกุล', 'เพศ', 'อายุ', 
            'เลขบัตรประชาชน', 'ชื่อหมู่บ้าน', 'บ้านเลขที่', 
            'ชื่อถนน', 'ละติจูด', 'ลองติจูด'
        ]
        df_final = df[final_columns]

        # --- [ 6. ส่งออกเป็นไฟล์ Excel ] ---
        filename = "Buddy_Care_Report.xlsx"
        
        # ใช้ Engine 'openpyxl' (ต้องติดตั้งด้วย: pip install openpyxl)
        df_final.to_excel(filename, index=False, sheet_name='Data_Patient')
        
        print("-" * 30)
        print(f"สำเร็จ! ไฟล์ถูกบันทึกที่: {filename}")
        print("-" * 30)

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        print(f"Error: {e}")
    finally:
      
        if conn:
            conn.close()
            print("Connection closed.")

if __name__ == "__main__":
    export_full_report()
    test_connection()