"""Main GUI application for conversion code management."""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Optional
from database import ConversionCodeDB
from datetime import datetime


class ConversionCodeGUI:
    """Main GUI application for managing conversion codes."""
    
    def __init__(self):
        """Initialize the GUI application."""
        self.db = ConversionCodeDB()
        self.root = tk.Tk()
        self.root.title("Conversion Code Manager")
        self.root.geometry("1000x600")
        
        self.setup_ui()
        self.refresh_data()
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Conversion Code Manager", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Filter section
        filter_frame = ttk.LabelFrame(main_frame, text="Filter", padding="5")
        filter_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        filter_frame.columnconfigure(1, weight=1)
        
        ttk.Label(filter_frame, text="Field Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.filter_var = tk.StringVar()
        self.filter_entry = ttk.Entry(filter_frame, textvariable=self.filter_var, width=30)
        self.filter_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.filter_entry.bind('<KeyRelease>', self.on_filter_change)
        
        ttk.Button(filter_frame, text="Clear Filter", 
                  command=self.clear_filter).grid(row=0, column=2, padx=5)
        
        # Data table
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        # Treeview with scrollbars
        self.tree = ttk.Treeview(table_frame, columns=(
            'ID', 'FIELD_NAME', 'SOURCE_VALUE', 'SPECTRUM_VALUE', 
            'IS_IMPORTED', 'UPDATE_COUNT', 'CHANGE_DATE_TIME'
        ), show='headings', height=15)
        
        # Configure columns
        columns = {
            'ID': ('ID', 80),
            'FIELD_NAME': ('Field Name', 150),
            'SOURCE_VALUE': ('Source Value', 120),
            'SPECTRUM_VALUE': ('Spectrum Value', 120),
            'IS_IMPORTED': ('Imported', 80),
            'UPDATE_COUNT': ('Updates', 80),
            'CHANGE_DATE_TIME': ('Last Changed', 150)
        }
        
        for col_id, (heading, width) in columns.items():
            self.tree.heading(col_id, text=heading)
            self.tree.column(col_id, width=width, minwidth=width)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(button_frame, text="Add New", 
                  command=self.add_record).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Edit Selected", 
                  command=self.edit_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Selected", 
                  command=self.delete_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh", 
                  command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", 
                  command=self.root.quit).pack(side=tk.RIGHT)
        
        # Double-click to edit
        self.tree.bind('<Double-1>', lambda e: self.edit_record())
    
    def refresh_data(self):
        """Refresh the data in the table."""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get filtered data
        filter_text = self.filter_var.get().strip()
        records = self.db.get_all_records(filter_text if filter_text else None)
        
        # Populate tree
        for record in records:
            # Format datetime for display
            change_date = record['CHANGE_DATE_TIME']
            if isinstance(change_date, str):
                # Parse if it's a string
                try:
                    dt = datetime.fromisoformat(change_date.replace('Z', '+00:00'))
                    formatted_date = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    formatted_date = change_date
            else:
                formatted_date = str(change_date)
            
            self.tree.insert('', tk.END, values=(
                record['CONVERSION_CODE_ID'],
                record['FIELD_NAME'] or '',
                record['SOURCE_VALUE'] or '',
                record['SPECTRUM_VALUE'] or '',
                record['IS_IMPORTED'],
                record['UPDATE_COUNT'],
                formatted_date
            ))
    
    def on_filter_change(self, event=None):
        """Handle filter text change."""
        self.refresh_data()
    
    def clear_filter(self):
        """Clear the filter."""
        self.filter_var.set('')
        self.refresh_data()
    
    def get_selected_id(self) -> Optional[int]:
        """Get the ID of the currently selected record."""
        selection = self.tree.selection()
        if not selection:
            return None
        item = self.tree.item(selection[0])
        return int(item['values'][0])
    
    def add_record(self):
        """Add a new record."""
        dialog = RecordDialog(self.root, "Add New Record")
        if dialog.result:
            try:
                self.db.add_record(
                    dialog.result['field_name'],
                    dialog.result['source_value'],
                    dialog.result['spectrum_value'],
                    dialog.result['is_imported']
                )
                self.refresh_data()
                messagebox.showinfo("Success", "Record added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add record: {str(e)}")
    
    def edit_record(self):
        """Edit the selected record."""
        record_id = self.get_selected_id()
        if not record_id:
            messagebox.showwarning("No Selection", "Please select a record to edit.")
            return
        
        # Get current record data
        current_record = self.db.get_record_by_id(record_id)
        if not current_record:
            messagebox.showerror("Error", "Record not found.")
            return
        
        dialog = RecordDialog(self.root, "Edit Record", current_record)
        if dialog.result:
            try:
                self.db.update_record(
                    record_id,
                    dialog.result['field_name'],
                    dialog.result['source_value'],
                    dialog.result['spectrum_value'],
                    dialog.result['is_imported']
                )
                self.refresh_data()
                messagebox.showinfo("Success", "Record updated successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update record: {str(e)}")
    
    def delete_record(self):
        """Delete the selected record."""
        record_id = self.get_selected_id()
        if not record_id:
            messagebox.showwarning("No Selection", "Please select a record to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete record ID {record_id}?"):
            try:
                self.db.delete_record(record_id)
                self.refresh_data()
                messagebox.showinfo("Success", "Record deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete record: {str(e)}")
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


class RecordDialog:
    """Dialog for adding/editing records."""
    
    def __init__(self, parent, title: str, record_data: Optional[dict] = None):
        """Initialize the dialog."""
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (parent.winfo_screenwidth() // 2) - (400 // 2)
        y = (parent.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"400x300+{x}+{y}")
        
        self.setup_dialog(record_data)
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def setup_dialog(self, record_data: Optional[dict]):
        """Set up the dialog UI."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Field Name
        ttk.Label(main_frame, text="Field Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.field_name_var = tk.StringVar()
        field_name_entry = ttk.Entry(main_frame, textvariable=self.field_name_var, width=40)
        field_name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Source Value
        ttk.Label(main_frame, text="Source Value:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.source_value_var = tk.StringVar()
        source_value_entry = ttk.Entry(main_frame, textvariable=self.source_value_var, width=40)
        source_value_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Spectrum Value
        ttk.Label(main_frame, text="Spectrum Value:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.spectrum_value_var = tk.StringVar()
        spectrum_value_entry = ttk.Entry(main_frame, textvariable=self.spectrum_value_var, width=40)
        spectrum_value_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Is Imported
        ttk.Label(main_frame, text="Is Imported:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.is_imported_var = tk.StringVar()
        is_imported_combo = ttk.Combobox(main_frame, textvariable=self.is_imported_var, 
                                        values=['Y', 'N'], state='readonly', width=37)
        is_imported_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        is_imported_combo.set('N')
        
        # Populate with existing data if editing
        if record_data:
            self.field_name_var.set(record_data['FIELD_NAME'] or '')
            self.source_value_var.set(record_data['SOURCE_VALUE'] or '')
            self.spectrum_value_var.set(record_data['SPECTRUM_VALUE'] or '')
            self.is_imported_var.set(record_data['IS_IMPORTED'])
        
        # Configure grid
        main_frame.columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Save", 
                  command=self.save_record).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", 
                  command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Focus on first field
        field_name_entry.focus_set()
    
    def save_record(self):
        """Save the record and close dialog."""
        # Validate required fields
        field_name = self.field_name_var.get().strip()
        source_value = self.source_value_var.get().strip()
        spectrum_value = self.spectrum_value_var.get().strip()
        is_imported = self.is_imported_var.get()
        
        if not field_name:
            messagebox.showerror("Validation Error", "Field Name is required.")
            return
        
        if len(field_name) > 50:
            messagebox.showerror("Validation Error", "Field Name cannot exceed 50 characters.")
            return
        
        if len(source_value) > 20:
            messagebox.showerror("Validation Error", "Source Value cannot exceed 20 characters.")
            return
        
        if len(spectrum_value) > 10:
            messagebox.showerror("Validation Error", "Spectrum Value cannot exceed 10 characters.")
            return
        
        if is_imported not in ['Y', 'N']:
            messagebox.showerror("Validation Error", "Is Imported must be Y or N.")
            return
        
        self.result = {
            'field_name': field_name,
            'source_value': source_value,
            'spectrum_value': spectrum_value,
            'is_imported': is_imported
        }
        self.dialog.destroy()


if __name__ == "__main__":
    app = ConversionCodeGUI()
    app.run()