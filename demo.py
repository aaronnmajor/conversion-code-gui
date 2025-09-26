"""Demo script to populate sample data and show the GUI."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import ConversionCodeDB


def create_sample_data():
    """Create sample data for demonstration."""
    db = ConversionCodeDB()
    
    # Sample conversion code data
    sample_data = [
        ("CUSTOMER_TYPE", "INDIVIDUAL", "IND", "Y"),
        ("CUSTOMER_TYPE", "BUSINESS", "BUS", "Y"),
        ("CUSTOMER_TYPE", "GOVERNMENT", "GOV", "N"),
        ("STATUS_CODE", "ACTIVE", "A", "Y"),
        ("STATUS_CODE", "INACTIVE", "I", "Y"),
        ("STATUS_CODE", "PENDING", "P", "N"),
        ("PRIORITY_LEVEL", "HIGH", "H", "Y"),
        ("PRIORITY_LEVEL", "MEDIUM", "M", "Y"),
        ("PRIORITY_LEVEL", "LOW", "L", "Y"),
        ("REGION_CODE", "NORTH_AMERICA", "NA", "Y"),
        ("REGION_CODE", "EUROPE", "EU", "Y"),
        ("REGION_CODE", "ASIA_PACIFIC", "AP", "N"),
        ("DEPARTMENT", "SALES", "SLS", "Y"),
        ("DEPARTMENT", "MARKETING", "MKT", "Y"),
        ("DEPARTMENT", "ENGINEERING", "ENG", "N"),
        ("PRODUCT_LINE", "SOFTWARE", "SW", "Y"),
        ("PRODUCT_LINE", "HARDWARE", "HW", "Y"),
        ("PRODUCT_LINE", "SERVICES", "SRV", "N")
    ]
    
    print("Creating sample data...")
    for field_name, source_value, spectrum_value, is_imported in sample_data:
        db.add_record(field_name, source_value, spectrum_value, is_imported)
    
    print(f"✓ Created {len(sample_data)} sample records")
    
    # Show summary
    all_records = db.get_all_records()
    print(f"Total records in database: {len(all_records)}")
    
    # Show field name distribution
    field_names = {}
    for record in all_records:
        field_name = record['FIELD_NAME']
        field_names[field_name] = field_names.get(field_name, 0) + 1
    
    print("\nField name distribution:")
    for field_name, count in sorted(field_names.items()):
        print(f"  {field_name}: {count} records")


if __name__ == "__main__":
    create_sample_data()
    print("\nStarting GUI application...")
    
    # Import and run the GUI
    from main import ConversionCodeGUI
    app = ConversionCodeGUI()
    app.run()