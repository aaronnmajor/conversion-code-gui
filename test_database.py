"""Test script for the conversion code database functionality."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import ConversionCodeDB
import tempfile
import os


def test_database_functionality():
    """Test basic database operations."""
    # Use a temporary database file
    temp_db = os.path.join(tempfile.gettempdir(), 'test_conversion_codes.db')
    
    try:
        # Initialize database
        db = ConversionCodeDB(temp_db)
        print("✓ Database initialized successfully")
        
        # Test adding records
        id1 = db.add_record("TEST_FIELD_1", "SRC001", "SPEC001", "N")
        id2 = db.add_record("TEST_FIELD_2", "SRC002", "SPEC002", "Y")
        print(f"✓ Added records with IDs: {id1}, {id2}")
        
        # Test getting all records
        records = db.get_all_records()
        print(f"✓ Retrieved {len(records)} records")
        assert len(records) == 2, f"Expected 2 records, got {len(records)}"
        
        # Test filtering
        filtered = db.get_all_records("TEST_FIELD_1")
        print(f"✓ Filtered records: {len(filtered)}")
        assert len(filtered) == 1, f"Expected 1 filtered record, got {len(filtered)}"
        
        # Test updating a record
        success = db.update_record(id1, "UPDATED_FIELD", "NEWSRC", "NEWSPEC", "Y")
        assert success, "Update should have succeeded"
        print("✓ Record updated successfully")
        
        # Verify update
        updated_record = db.get_record_by_id(id1)
        assert updated_record['FIELD_NAME'] == "UPDATED_FIELD", "Field name not updated correctly"
        assert updated_record['UPDATE_COUNT'] == 1, "Update count not incremented"
        print("✓ Update verification passed")
        
        # Test deleting a record
        success = db.delete_record(id2)
        assert success, "Delete should have succeeded"
        print("✓ Record deleted successfully")
        
        # Verify deletion
        remaining_records = db.get_all_records()
        assert len(remaining_records) == 1, f"Expected 1 record after deletion, got {len(remaining_records)}"
        print("✓ Deletion verification passed")
        
        print("\n🎉 All database tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False
    
    finally:
        # Clean up
        if os.path.exists(temp_db):
            os.remove(temp_db)


if __name__ == "__main__":
    test_database_functionality()