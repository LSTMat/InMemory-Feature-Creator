# Utils/__init__.py

# ✅ Import classes
from .TableModel import ModelConfiguration, Table, Row, Column, Value

# ✅ Import function 
from .InMemoryConfiguration import load_xml_to_config
from .DDGeneration import get_DD_ModelConfiguration_Structure
from .SQLGenerator import generate_insert_sql
from .FeatureGenerator import generate_sql_Feature_creation


# ✅ Import enum
from .IMFGCore import (
                DataType,
                Table1ColumnName, Table1ColumnType, Table1ColumnOrder,
                Table2ColumnName, Table2ColumnType, Table2ColumnOrder,
                Table3ColumnName, Table3ColumnType, Table3ColumnOrder,
                VariableType, TabName,
                IMConfigurationTable, IMConfigurationDomain, IMConfigurationModelTable, IMConfigurationModelTableColumn
                )

# ✅ Import variables
from .IMFGCore import DD_MODEL_FILE

# Define what is available when using `import Utils`
__all__ = ["load_xml_to_config", "get_DD_ModelConfiguration_Structure", "generate_insert_sql", "generate_sql_Feature_creation",
           
           "ModelConfiguration", "Table", "Row", "Column", "Value",
           
           "Data",
           "Table1ColumnName", "Table1ColumnType", "Table1ColumnOrder",
           "Table2ColumnName", "Table2ColumnType", "Table2ColumnOrder",
           "Table3ColumnName", "Table3ColumnType", "Table3ColumnOrder",
           "VariableType", "TabName",
           "IMConfigurationTable", "IMConfigurationDomain", "IMConfigurationModelTable",
           "IMConfigurationModelTableColumn",

           "DD_MODEL_FILE"]
