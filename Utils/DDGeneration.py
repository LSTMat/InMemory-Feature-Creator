import xml.etree.ElementTree as ET
import os
from dataclasses import dataclass, field
from typing import List, Optional
from .TableModel import ModelConfiguration, Table, Row, Column, Value


def get_DD_ModelConfiguration_Structure(file_path: str) -> ModelConfiguration:
    
    def get_xml_from_file(file_path: str) -> Optional[ET.Element]:
        try:
            base_path = os.path.dirname(os.path.dirname(__file__))  # Get one folder before the current file's directory
            full_path = os.path.join(base_path, file_path)
            with open(full_path, "r", encoding="utf-8", errors="ignore") as file:
                return ET.fromstring(file.read())  # Parse the XML file into an ElementTree object
        except ET.ParseError as e:
            print(f"Error parsing XML file {full_path}: {e}")
            return None
    
    root = get_xml_from_file(file_path)
    if root is None:
        return ModelConfiguration(name="Invalid Model", tables=[])
    
    model_name = root.find('Name').text
    tables = []
    
    for table_element in root.findall(".//Table"):
        schema_name = table_element.get("SchemaName")
        table_name = table_element.get("TableName")
        columns = {}
        
        for column_element in table_element.findall(".//Column"):
            name = column_element.get("Name")
            type = column_element.get("Type")
            is_pk = column_element.get("IsPK", "false").lower() == "true"
            is_identity = column_element.get("IsIdentity", "false").lower() == "true"
            reference_table_schema = column_element.get("ReferenceTableSchema")
            reference_table_name = column_element.get("ReferenceTableName")
            reference_column = column_element.get("ReferenceColumn")
            
            column = Column(
                column_name=name,
                column_type=type,
                is_pk=is_pk,
                is_identity=is_identity,
                reference_table_schema=reference_table_schema,
                reference_table_name=reference_table_name,
                reference_column=reference_column
            )
            columns[name] = (column)
        
        table = Table(
            schema_name=schema_name,
            table_name=table_name,
            rows={1: Row(1, columns=columns)}
        )
        tables.append(table)
    
    model = ModelConfiguration(
        Name=model_name,
        Tables=tables
    )
    
    return model

# Example usage
# file_path = "G:/Git Repository/InMemory-Feature-Creator/TestFiles/DD Model only necessary.xml"
# model = get_DD_ModelConfiguration_Structure(file_path)
# model.set_column_values_by_row_number("DDDomain", 1, {"FeatureKey": "1", "CRUDStatus": "C"})
# # Print the parsed model for verification
# print(model)