CREATE TABLE patients (
    -- 1. Identity จาก Webhook (Primary Key)
    user_id VARCHAR(100) PRIMARY KEY,
    
    -- 2. ข้อมูลยืนยันตัวตน
    citizen_id VARCHAR(13) UNIQUE,
    
    -- 3. ข้อมูลชื่อ-นามสกุล
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    
    -- 4. ข้อมูลส่วนตัว (ใช้ INT ทั้งหมด)
    birth_year INT COMMENT 'ปีเกิด พ.ศ. หรือ ค.ศ.',
    age INT COMMENT 'อายุคนไข้',
    gender INT COMMENT '1 = ผู้ชาย, 2 = ผู้หญิง',
    
    -- 5. ข้อมูลที่อยู่
    district VARCHAR(100) COMMENT 'เขต หรือ อำเภอ',
    
    -- 6. ข้อมูลระบบ
    provider VARCHAR(50) NOT NULL,
    raw_payload JSON,
    
    -- 7. บันทึกเวลา
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;