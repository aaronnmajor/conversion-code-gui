"""Database module for conversion code management."""
import sqlite3
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class ConversionCodeDB:
    """Database handler for conversion codes."""
    
    def __init__(self, db_path: str = "conversion_codes.db"):
        """Initialize database connection."""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create the conversion codes table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS S_CONVERSION_CODE_G97 (
                    CONVERSION_CODE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    FIELD_NAME VARCHAR(50),
                    SOURCE_VALUE VARCHAR(20),
                    SPECTRUM_VALUE VARCHAR(10),
                    IS_IMPORTED CHAR(1) NOT NULL DEFAULT 'N',
                    UPDATE_COUNT INTEGER NOT NULL DEFAULT 0,
                    CHANGE_DATE_TIME TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def get_all_records(self, field_name_filter: Optional[str] = None) -> List[Dict]:
        """Get all records, optionally filtered by field name."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if field_name_filter:
                cursor.execute('''
                    SELECT * FROM S_CONVERSION_CODE_G97 
                    WHERE FIELD_NAME LIKE ? 
                    ORDER BY CONVERSION_CODE_ID
                ''', (f'%{field_name_filter}%',))
            else:
                cursor.execute('''
                    SELECT * FROM S_CONVERSION_CODE_G97 
                    ORDER BY CONVERSION_CODE_ID
                ''')
            
            return [dict(row) for row in cursor.fetchall()]
    
    def add_record(self, field_name: str, source_value: str, spectrum_value: str, 
                   is_imported: str = 'N') -> int:
        """Add a new record."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO S_CONVERSION_CODE_G97 
                (FIELD_NAME, SOURCE_VALUE, SPECTRUM_VALUE, IS_IMPORTED, UPDATE_COUNT, CHANGE_DATE_TIME)
                VALUES (?, ?, ?, ?, 0, ?)
            ''', (field_name, source_value, spectrum_value, is_imported, datetime.now()))
            conn.commit()
            return cursor.lastrowid
    
    def update_record(self, conversion_code_id: int, field_name: str, source_value: str, 
                      spectrum_value: str, is_imported: str) -> bool:
        """Update an existing record."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE S_CONVERSION_CODE_G97 
                SET FIELD_NAME = ?, SOURCE_VALUE = ?, SPECTRUM_VALUE = ?, 
                    IS_IMPORTED = ?, UPDATE_COUNT = UPDATE_COUNT + 1, 
                    CHANGE_DATE_TIME = ?
                WHERE CONVERSION_CODE_ID = ?
            ''', (field_name, source_value, spectrum_value, is_imported, 
                  datetime.now(), conversion_code_id))
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_record(self, conversion_code_id: int) -> bool:
        """Delete a record."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM S_CONVERSION_CODE_G97 WHERE CONVERSION_CODE_ID = ?', 
                          (conversion_code_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_record_by_id(self, conversion_code_id: int) -> Optional[Dict]:
        """Get a single record by ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM S_CONVERSION_CODE_G97 WHERE CONVERSION_CODE_ID = ?', 
                          (conversion_code_id,))
            row = cursor.fetchone()
            return dict(row) if row else None