# Conversion Code GUI

A Python GUI application for managing conversion codes in the `S_CONVERSION_CODE_G97` database table. This application provides a user-friendly interface for performing CRUD (Create, Read, Update, Delete) operations on conversion code records with filtering capabilities.

## Features

- **CRUD Operations**: Add, edit, view, and delete conversion code records
- **Filtering**: Filter records by field name with real-time search
- **Data Validation**: Input validation to ensure data integrity
- **User-Friendly Interface**: Clean, intuitive GUI built with tkinter
- **Database Management**: Uses SQLite for local development/testing

## Database Schema

The application manages records in the `S_CONVERSION_CODE_G97` table with the following structure:

```sql
CREATE TABLE [dbo].[S_CONVERSION_CODE_G97](
    [CONVERSION_CODE_ID] [bigint] IDENTITY(1,1) NOT NULL,
    [FIELD_NAME] [varchar](50) NULL,
    [SOURCE_VALUE] [varchar](20) NULL,
    [SPECTRUM_VALUE] [varchar](10) NULL,
    [IS_IMPORTED] [char](1) NOT NULL,
    [UPDATE_COUNT] [int] NOT NULL,
    [CHANGE_DATE_TIME] [smalldatetime] NOT NULL)
```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/aaronnmajor/conversion-code-gui.git
   cd conversion-code-gui
   ```

2. No additional dependencies are required as the application uses built-in Python libraries (tkinter, sqlite3).

## Usage

### Running the Application

To start the application with an empty database:
```bash
python main.py
```

To start with sample data for demonstration:
```bash
python demo.py
```

### Application Features

#### Main Interface
- **Data Table**: Displays all conversion code records in a sortable table
- **Filter Box**: Enter text to filter records by field name
- **Action Buttons**: Add, Edit, Delete, Refresh, and Exit

#### Adding Records
1. Click "Add New" button
2. Fill in the required fields:
   - Field Name (required, max 50 characters)
   - Source Value (max 20 characters)
   - Spectrum Value (max 10 characters)
   - Is Imported (Y/N dropdown)
3. Click "Save" to add the record

#### Editing Records
1. Select a record in the table
2. Click "Edit Selected" or double-click the record
3. Modify the fields as needed
4. Click "Save" to update the record

#### Deleting Records
1. Select a record in the table
2. Click "Delete Selected"
3. Confirm the deletion in the dialog

#### Filtering Records
- Type in the "Field Name" filter box to filter records in real-time
- Click "Clear Filter" to show all records

## Files Structure

- `main.py` - Main GUI application
- `database.py` - Database operations and SQLite management
- `demo.py` - Demo script with sample data
- `test_database.py` - Unit tests for database functionality
- `requirements.txt` - Dependencies (none required for basic functionality)
- `README.md` - This documentation

## Database Configuration

By default, the application uses SQLite with a local file `conversion_codes.db`. The database is automatically created when the application first runs.

For SQL Server integration, you can modify the `database.py` file to use `pyodbc` instead of `sqlite3`.

## Testing

Run the database tests:
```bash
python test_database.py
```

This will verify that all CRUD operations work correctly.

## Requirements

- Python 3.6 or higher
- tkinter (included with Python)
- sqlite3 (included with Python)

## License

This project is open source and available under the MIT License.