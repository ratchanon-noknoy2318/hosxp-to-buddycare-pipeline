import os
import logging
import urllib.parse
from dataclasses import dataclass
from typing import Optional

import pandas as pd
from sqlalchemy import create_engine, Engine
from sqlalchemy.exc import SQLAlchemyError

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@dataclass
class DatabaseConfig:
    """Configuration for database connection."""
    host: str
    user: str
    password: str
    name: str
    port: str = "3300"

    @property
    def connection_string(self) -> str:
        encoded_password = urllib.parse.quote_plus(self.password)
        return f"mysql+pymysql://{self.user}:{encoded_password}@{self.host}:{self.port}/{self.name}?charset=utf8mb4"

class PatientDataExtractor:
    """Handles extraction of patient data from HOSxP database."""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.engine: Optional[Engine] = None
        self._init_engine()

    def _init_engine(self) -> None:
        try:
            self.engine = create_engine(self.config.connection_string)
            logger.debug("Database engine initialized.")
        except Exception as e:
            logger.error(f"Failed to initialize database engine: {e}")
            raise

    def _get_query(self) -> str:
        return """
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

    def extract(self) -> Optional[pd.DataFrame]:
        """
        Executes the query and returns a pandas DataFrame.
        """
        if not self.engine:
            logger.error("Database engine is not ready.")
            return None

        try:
            query = self._get_query()
            logger.info("Starting data extraction...")
            
            with self.engine.connect() as connection:
                df = pd.read_sql(query, connection)
            
            logger.info(f"Extraction complete. Retrieved {len(df)} records.")
            return df

        except SQLAlchemyError as e:
            logger.error(f"Database error during extraction: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None

if __name__ == "__main__":
    # Load config from env or defaults
    config = DatabaseConfig(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'sa'),
        password=os.getenv('DB_PASSWORD', 'sa'),
        name=os.getenv('DB_NAME', 'hosxp'),
        port=os.getenv('DB_PORT', '3300')
    )

    extractor = PatientDataExtractor(config)
    df = extractor.extract()
    
    if df is not None:
        print(df.head())