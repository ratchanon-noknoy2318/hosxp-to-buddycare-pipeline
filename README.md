# HOSxP Data Integration Pipeline

Developed and optimized SQL-based data integration pipelines using HOSxP data (400K+ records) to support analytics, reporting, and automation use cases.

---

## Data Governance & Security
To ensure compliance with PDPA (Thailand's Personal Data Protection Act) and handle sensitive healthcare information securely, this project adheres to the following principles:

* **Data Minimization:** Only essential PII (Personally Identifiable Information) is extracted for workflow automation.
* **Sensitive Data Handling:** Strict management of patient records (400K+ entries) ensuring data reliability and integrity.
* **Security by Design:** Database schemas are structured with unique constraints and clear data typing to prevent unauthorized data duplication or leakage.

---

## Patients Table Schema
The following table describes the mapping from the source HOSxP system to the integrated patients table:

| HOSxP Field (person table) | patients Table Field | Type | Description | PDPA/Security Note |
| :--- | :--- | :--- | :--- | :--- |
| p.cid | citizen_id | VARCHAR(13) | National ID (UNIQUE, NOT NULL) | PII - Sensitive Unique ID |
| p.pname | title | VARCHAR(20) | Title (e.g., นาย, นาง, นางสาว) | Identity Data |
| p.fname | first_name | VARCHAR(100) | First Name | Identity Data |
| p.lname | last_name | VARCHAR(100) | Last Name | Identity Data |
| p.birthdate | birthdate | DATE | Full Date of Birth | Sensitive - For Age Logic |
| p.sex | gender | INT | Gender (1=Male, 2=Female) | Demographic Data |
| h.address | house_number | VARCHAR(50) | House Number (parsed) | Location Data |
| h.road | road | VARCHAR(100) | Road Name | Location Data |
| v.village_name| village_name | VARCHAR(100) | Village Name | Location Data |

---

## Data Utilization & Use Cases
ข้อมูลที่ผ่านกระบวนการ Integration นี้ถูกนำไปใช้เพื่อสร้างมูลค่าในด้านต่างๆ ดังนี้:

### 1. Executive Decision Support (Strategic Insights)
* **High-Level Dashboards:** สรุปภาพรวมสถิติผู้ป่วยและทรัพยากรในโรงพยาบาลส่งตรงถึง **ผู้บริหารสูงสุด** เพื่อใช้ในการตัดสินใจเชิงกลยุทธ์และบริหารนโยบายองค์กร
* **Resource Allocation:** วิเคราะห์แนวโน้มผู้รับบริการรายวัน/รายเดือน เพื่อการบริหารงบประมาณและกำลังคนให้สอดคล้องกับภาระงานจริง

### 2. AI-Powered Data Quality Assurance
* **Anomaly Detection:** นำข้อมูลเข้าสู่โมเดล AI เพื่อตรวจหาข้อมูลที่ผิดปกติ (Outliers) เช่น ข้อมูลวันเกิดที่ไม่สัมพันธ์กับอายุจริง หรือรูปแบบรหัสบัตรประชาชนที่ไม่ถูกต้อง
* **Data Integrity Audit:** ระบบ AI ช่วยระบุและคัดกรองข้อมูลที่อาจมีความคลาดเคลื่อนหรือซ้ำซ้อน เพื่อส่งให้เจ้าหน้าที่ตรวจสอบและแก้ไขให้ถูกต้อง (Master Data Management)

### 3. Workflow Automation (Staff Alerts)
* **Staff Notifications:** เชื่อมต่อกับ LINE Messaging API เพื่อส่งข้อความ **แจ้งเตือนเจ้าหน้าที่ผู้รับผิดชอบโดยตรง** เช่น แจ้งเตือนคิวนัดหมายล่วงหน้า หรือแจ้งเตือนสถานะเคสที่ต้องดำเนินการเร่งด่วน
* **Registration Sync:** ระบบอัตโนมัติในการ Sync ข้อมูลผู้ป่วยไปยังระบบเฉพาะทางอื่นๆ ภายในเครือข่าย เพื่อลดภาระการกรอกข้อมูลใหม่และป้องกัน Human Error

---

## Contact and Profiles
* **Name:** Ratchanon Noknoy
* **Email:** ratchanon.noknoy2318@gmail.com
* **LinkedIn:** [linkedin.com/in/ratchanon-noknoy/](https://linkedin.com/in/ratchanon-noknoy/)
* **GitLab/GitHub:** [ratchanon.noknoy2318](https://github.com/ratchanon.noknoy2318)
