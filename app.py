import pandas as pd
from tabulate import tabulate

# 1. โหลดข้อมูลทั้งหมด
# encoding='utf-8-sig' ช่วยให้อ่านภาษาไทยจากไฟล์ CSV ที่เซฟจาก Excel ได้
df = pd.read_csv('data.csv', encoding='utf-8-sig')

# 2. ดูภาพรวมทั้งหมด (ข้อมูลพื้นฐาน)
print("=== ข้อมูลเบื้องต้น ===")
print(df.info())  # ดูว่ามีกี่แถว, มีคอลัมน์อะไรบ้าง, มีค่าว่าง (Null) หรือไม่

# 3. แสดงข้อมูลทั้งหมด (ถ้าไฟล์ไม่ใหญ่เกินไป)
# หากต้องการดูทั้งหมดจริงๆ ใน Terminal ให้ใช้ df.to_string()
print("\n=== เนื้อหาข้อมูลทั้งหมด ===")
table_output = tabulate(df, headers='keys', tablefmt='psql')
print(table_output)

# บันทึกตารางสวยๆ ลงไฟล์ Text (output.txt) เพื่อเก็บไว้ดู
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(table_output)
print("\nบันทึกไฟล์ output.txt เรียบร้อยแล้ว")

# 4. ดูสถิติพื้นฐานของข้อมูลที่เป็นตัวเลข (เช่น bps, อายุ)
print("\n=== สถิติพื้นฐาน (Mean, Max, Min) ===")
print(df.describe())

# 5. ตรวจสอบค่าว่าง (Missing Values)
print("\n=== ตรวจสอบค่าว่างในแต่ละคอลัมน์ ===")
print(df.isnull().sum())