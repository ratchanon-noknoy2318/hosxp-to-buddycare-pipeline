# HOSxP Data Integration Pipeline

Developed and optimized SQL-based data integration pipelines using HOSxP data (400K+ records) to support executive analytics, AI-driven data quality, and operational automation.

---

## Data Governance & Security
To ensure compliance with **PDPA (Thailand's Personal Data Protection Act)** and handle sensitive healthcare information securely, this project adheres to the following principles:

* **Data Minimization:** Only essential PII (Personally Identifiable Information) is extracted for specific workflow requirements.
* **Sensitive Data Handling:** Strict management of 400K+ patient records, ensuring end-to-end data reliability and integrity.
* **Security by Design:** Database schemas are structured with unique constraints and strict data typing to prevent unauthorized duplication or leakage.

---

## Patients Table Schema
The following table describes the mapping from the source HOSxP system to the integrated patients table:

| HOSxP Field (person table) | patients Table Field | Type | Description | PDPA/Security Note |
| :--- | :--- | :--- | :--- | :--- |
| p.cid | citizen_id | VARCHAR(13) | National ID (UNIQUE, NOT NULL) | PII - Sensitive Unique ID |
| p.pname | title | VARCHAR(20) | Title (e.g., Mr., Mrs., Ms.) | Identity Data |
| p.fname | first_name | VARCHAR(100) | First Name | Identity Data |
| p.lname | last_name | VARCHAR(100) | Last Name | Identity Data |
| p.birthdate | birthdate | DATE | Full Date of Birth | Sensitive - For Age Logic |
| p.sex | gender | INT | Gender (1=Male, 2=Female) | Demographic Data |
| h.address | house_number | VARCHAR(50) | House Number (parsed) | Location Data |
| h.road | road | VARCHAR(100) | Road Name | Location Data |
| v.village_name| village_name | VARCHAR(100) | Village Name | Location Data |

---

## Data Utilization & Use Cases
The integrated data is utilized across various organizational levels to drive efficiency and accuracy:

### 1. Executive Decision Support (Strategic Insights)
* **High-Level Dashboards:** Aggregated hospital statistics and resource metrics delivered to **top-level management** for strategic planning and policy making.
* **Resource Allocation:** Trend analysis of daily/monthly patient visits to optimize budget management and human resource allocation based on actual workload.

### 2. AI-Powered Data Quality Assurance
* **Anomaly Detection:** Data is fed into AI models to identify outliers or irregularities, such as mismatched birthdates relative to age or invalid National ID formats.
* **Data Integrity Audit:** AI-driven identification of duplicate or inconsistent records, streamlining the **Master Data Management (MDM)** process for staff verification.

### 3. Workflow Automation (Staff Alerts)
* **Staff Notifications:** Integration with **LINE Messaging API** to send automated alerts directly to responsible staff for upcoming appointments or urgent cases requiring immediate action.
* **Registration Sync:** Automated synchronization of patient data across specialized internal systems to reduce manual entry, minimize human error, and save administrative time.

---

## Contact and Profiles
* **Name:** Ratchanon Noknoy
* **Email:** ratchanon.noknoy2318@gmail.com
* **LinkedIn:** [linkedin.com/in/ratchanon-noknoy/](https://linkedin.com/in/ratchanon-noknoy/)
* **GitLab/GitHub:** [ratchanon.noknoy2318](https://github.com/ratchanon.noknoy2318)
