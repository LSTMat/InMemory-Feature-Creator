# Utils/__init__.py

# ✅ Import classes
from .TableModel import ModelConfiguration, Table, Row, Column, Value

# ✅ Import function after classes
from .InMemoryConfiguration import load_xml_to_config
from .DDGeneration import get_DD_ModelConfiguration_Structure
from .SQLGenerator import generate_insert_sql

# ✅ Import function after classes
from .IMFGCore import Table1ColumnName, Table1ColumnOrder, Table2ColumnName, Table2ColumnOrder, IMConfigurationTable, IMConfigurationTableDomain

# Define what is available when using `import Utils`
__all__ = ["load_xml_to_config", "get_DD_ModelConfiguration_Structure", "generate_insert_sql"
           , "ModelConfiguration", "Table", "Row", "Column", "Value"
           , "Table1ColumnName", "Table1ColumnOrder", "Table2ColumnName", "Table2ColumnOrder", "IMConfigurationTable", "IMConfigurationTableDomain"]
