from typing import Dict
import xml.etree.ElementTree as ET
from .TableModel import ModelConfiguration, Table, Row, Column

def load_xml_to_config(file_path: str, metadata_file: str) -> ModelConfiguration:
    """Loads an XML file into an ModelConfiguration instance dynamically."""
    
    def parse_xml(file_path: str) -> ET.Element:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                return ET.fromstring(file.read())  # Parse the XML file into an ElementTree object
        except ET.ParseError as e:
            print(f"Error parsing XML file {file_path}: {e}")
            return None
    
    if not file_path:
        return ModelConfiguration(Name="Invalid File Path", Tables=[])

    root = parse_xml(file_path)
    metadata_root = parse_xml(metadata_file)
    if root is None or metadata_root is None:
        return ModelConfiguration(Name="Invalid Configuration", Tables=[])
    
    # Parse metadata file for table structure
    metadata_tables: Dict[str, Dict[str, Dict[str, str]]] = {}
    for table in metadata_root.findall(".//Table"):
        schema_name = table.get("SchemaName")
        table_name = table.get("TableName")
        if schema_name and table_name:
            columns = {
                col.get("Name"): {
                    "Type": col.get("Type", "str"),  # Default column type is string
                    "IsPK": col.get("IsPK", "false").lower() == "true",  # Convert primary key flag to boolean
                    "ReferenceTableSchema": col.get("ReferenceTableSchema", "false"),  # Name of the Reference Schema
                    "ReferenceTableName": col.get("ReferenceTableName", "false"),  # Name of the Reference Table
                    "ReferenceColumn": col.get("ReferenceColumn", "false")  # Name of the Reference Column Name
                }
                for col in table.findall("Columns/Column") if col.get("Name")  # Only process columns with a valid name
            }
            metadata_tables[f"{schema_name}.{table_name}"] = columns  # Store table metadata
    
    config_name = root.tag.replace("_x0020_", " ")  # Extract configuration name, replacing encoded spaces
    tables: Dict[str, Table] = {}
    
    # Parse main XML file for actual data records
    for record_element in root:
        if record_element is None or not hasattr(record_element, 'tag'):
            print("Warning: Skipping unexpected or malformed element in XML root.")
            continue
        
        table_key = record_element.tag  # Format is Schema.TableName
        if "." not in table_key:
            continue  # Skip invalid table keys
        schema_name, table_name = table_key.split(".", 1)
        
        if table_key not in tables:
            tables[table_key] = Table(schema_name=schema_name, table_name=table_name, rows={}) # Initialize table if not exists
        
        columns = {}
        for column_element in record_element:
            column_name = column_element.tag
            if not column_name:
                continue  # Skip columns without names
            column_value = column_element.text.strip() if column_element.text else None  # Use None for missing values
            metadata = metadata_tables.get(table_key, {}).get(column_name, {"Type": "str", "IsPK": False, "ReferenceTableSchema": None, "ReferenceTableName": None, "ReferenceColumn": None})  # Get column metadata
            columns[column_name] = Column(name=column_name, column_type=metadata["Type"], is_pk=metadata["IsPK"], value=column_value,
                                            reference_table_schema=metadata["ReferenceTableSchema"],
                                            reference_table_name=metadata["ReferenceTableName"],
                                            reference_column=metadata["ReferenceColumn"])

        row_number = max(tables[table_key].get_rows().keys(), default=-1) + 1
        row = Row(row_number=row_number, columns=columns)  # Create a new row with column data
        new_rows = {**tables[table_key].get_rows(), row_number: row}
        object.__setattr__(tables[table_key], "_rows", new_rows)  # Add the row to the respective table 
    
    return ModelConfiguration(Name=config_name, Tables=list(tables.values()))