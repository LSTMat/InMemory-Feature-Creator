from dataclasses import dataclass, field
from typing import List, Dict
import xml.etree.ElementTree as ET

@dataclass(slots=True, frozen=True)
class Column:
    """Defines a Column with essential attributes such as name, type, and primary key status."""
    _value: str  # Stores the actual value of the column
    _name: str  # Name of the column
    _is_pk: bool  # Indicates if the column is a Primary Key
    _column_type: str  # Data type of the column (e.g., Integer, String, DateTime, etc.)

    def __init__(self, value: str, name: str, is_pk: bool, column_type: str):
        # Use object.__setattr__ to set values since the class is frozen
        object.__setattr__(self, "_value", value)
        object.__setattr__(self, "_name", name)
        object.__setattr__(self, "_is_pk", is_pk)
        object.__setattr__(self, "_column_type", column_type)

    def get_value(self) -> str:
        return self._value
    
    def get_name(self) -> str:
        return self._name
    
    def is_primary_key(self) -> bool:
        return self._is_pk
    
    def get_column_type(self) -> str:
        return self._column_type

@dataclass(slots=True, frozen=True)
class Row:
    """Defines a Row with essential attributes, storing columns in a dictionary for fast access."""
    _row_number: int  # Unique row identifier
    _Columns: Dict[str, Column] = field(default_factory=dict)  # Dictionary of columns in the row

    def __init__(self, row_number: int, columns: Dict[str, Column]):
        object.__setattr__(self, "_row_number", row_number)
        object.__setattr__(self, "_Columns", columns if columns is not None else {})

    def get_row_number(self) -> int:
        return self._row_number
    
    def get_columns(self) -> Dict[str, Column]:
        return self._Columns
    
    def get_column_value(self, column_name: str) -> str:
        column = self._Columns.get(column_name)
        return column.get_value() if column else None

@dataclass(slots=True, frozen=True)
class Table:
    """Defines a Table with a schema name, table name, and a dictionary of rows for quick access."""
    _schema_name: str  # Name of the database schema
    _table_name: str  # Name of the table
    _rows: Dict[int, Row] = field(default_factory=dict)  # Dictionary of row objects indexed by row number

    def __init__(self, schema_name: str, table_name: str, rows: Dict[int, Row] = None):
        object.__setattr__(self, "_schema_name", schema_name)
        object.__setattr__(self, "_table_name", table_name)
        object.__setattr__(self, "_rows", rows if rows is not None else {})

    def get_schema_name(self) -> str:
        return self._schema_name
    
    def get_table_name(self) -> str:
        return self._table_name
    
    def get_rows(self) -> Dict[int, Row]:
        return self._rows

    def get_column_values(self, column_name: str) -> List[str]:
        return [row.get_column_value(column_name) for row in self._rows.values() if row.get_column_value(column_name) is not None]

@dataclass(slots=True, frozen=True)
class InMemoryConfiguration:
    """Configuration class that holds multiple tables, representing an in-memory database schema."""
    Name: str  # Name of the configuration
    Tables: List[Table] = field(default_factory=list)  # List of tables in the configuration

    def get_column_values(self, table_name: str, column_name: str) -> List[str]:
        for table in self.Tables:
            if table.get_table_name() == table_name:
                return table.get_column_values(column_name)
        return []

def load_xml_to_config(file_path: str, metadata_file: str) -> InMemoryConfiguration:
    """Loads an XML file into an InMemoryConfiguration instance dynamically."""
    
    def parse_xml(file_path: str) -> ET.Element:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                return ET.fromstring(file.read())
        except ET.ParseError as e:
            print(f"Error parsing XML file {file_path}: {e}")
            return None
    
    root = parse_xml(file_path)
    metadata_root = parse_xml(metadata_file)
    if root is None or metadata_root is None:
        return InMemoryConfiguration(Name="Invalid Configuration", Tables=[])
    
    # Parse metadata file for table structure
    metadata_tables: Dict[str, Dict[str, Dict[str, str]]] = {}
    for table in metadata_root.findall(".//Table"):
        schema_name = table.get("SchemaName")
        table_name = table.get("TableName")
        if schema_name and table_name:
            columns = {
                col.get("Name"): {
                    "Type": col.get("Type", "str"),
                    "IsPK": col.get("IsPK", "false").lower() == "true"
                }
                for col in table.findall("Columns/Column") if col.get("Name")
            }
            metadata_tables[f"{schema_name}.{table_name}"] = columns
    
    config_name = root.tag.replace("_x0020_", " ")
    tables: Dict[str, Table] = {}
    
    # Parse main XML file for actual data records
    for record_element in root:
        if record_element is None or not hasattr(record_element, 'tag'):
            print("Warning: Skipping unexpected or malformed element in XML root.")
            continue
        
        table_key = record_element.tag
        if "." not in table_key:
            continue
        schema_name, table_name = table_key.split(".", 1)
        
        if table_key not in tables:
            tables[table_key] = Table(schema_name=schema_name, table_name=table_name, rows={})
        
        columns = {}
        for column_element in record_element:
            column_name = column_element.tag
            if not column_name:
                continue
            column_value = column_element.text.strip() if column_element.text else None
            metadata = metadata_tables.get(table_key, {}).get(column_name, {"Type": "str", "IsPK": False})
            columns[column_name] = Column(name=column_name, column_type=metadata["Type"], is_pk=metadata["IsPK"], value=column_value)

        row_number = max(tables[table_key].get_rows().keys(), default=-1) + 1
        row = Row(row_number=row_number, columns=columns)
        new_rows = {**tables[table_key].get_rows(), row_number: row}
        object.__setattr__(tables[table_key], "_rows", new_rows)
    
    return InMemoryConfiguration(Name=config_name, Tables=list(tables.values()))





config = load_xml_to_config(
    "C:\\Users\\aleru\\Desktop\\InMemory Feature Creator\\TestFiles\\DEV System.xml",
    "C:\\Users\\aleru\\Desktop\\InMemory Feature Creator\\XML\\Aptean Planning In Memory 2024.3.0.3.xml")
a = 1