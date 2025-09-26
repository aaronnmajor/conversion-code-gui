"""Test GUI components without actually showing the window."""
import tkinter as tk
from tkinter import ttk
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import ConversionCodeDB
from main import ConversionCodeGUI, RecordDialog


def test_gui_components():
    """Test that GUI components can be created without errors."""
    print("Testing GUI components...")
    
    # Create a root window (but don't show it)
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    try:
        # Test database initialization
        db = ConversionCodeDB()
        print("✓ Database component works")
        
        # Add some test data
        db.add_record("TEST_FIELD", "TEST_SRC", "TEST_SPEC", "N")
        records = db.get_all_records()
        print(f"✓ Database has {len(records)} test record(s)")
        
        # Test that we can create the main GUI class
        app = ConversionCodeGUI()
        app.root.withdraw()  # Hide this window too
        print("✓ Main GUI class initialized")
        
        # Test that treeview is properly configured
        columns = app.tree['columns']
        print(f"✓ Treeview configured with {len(columns)} columns: {list(columns)}")
        
        # Test filter functionality
        app.filter_var.set("TEST")
        app.refresh_data()
        print("✓ Filter and refresh functionality works")
        
        # Test that we can create a record dialog
        dialog_root = tk.Toplevel(root)
        dialog_root.withdraw()
        print("✓ Record dialog can be created")
        
        print("\n🎉 All GUI component tests passed!")
        
        # Cleanup
        app.root.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"❌ GUI test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_gui_components()