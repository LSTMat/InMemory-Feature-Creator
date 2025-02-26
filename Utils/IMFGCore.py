from enum import Enum
from datetime import datetime

DD_MODEL_FILE = "DD\\DD Model only necessary.xml"

class DataType:

    class Type(Enum):
        STRING = str
        INTEGER = int
        FLOAT = float
        BOOLEAN = bool
        LIST = list
        DICTIONARY = dict
        DATETIME = datetime
        BINARY = bytes

    class TypeName(Enum):
        STRING = "String"
        INTEGER = "Integer"
        FLOAT = "Float"
        BOOLEAN = "Boolean"
        LIST = "List"
        DICTIONARY = "Dictionary"
        DATETIME = "DateTime"
        BINARY = "Binary"

def get_variable_type(type_name: str) -> DataType.Type:
    match type_name:
        case DataType.TypeName.STRING.value:
            return DataType.Type.STRING
        case DataType.TypeName.INTEGER.value:
            return DataType.Type.INTEGER
        case DataType.TypeName.FLOAT.value:
            return DataType.Type.FLOAT
        case DataType.TypeName.BOOLEAN.value:
            return DataType.Type.BOOLEAN
        case DataType.TypeName.LIST.value:
            return DataType.Type.LIST
        case DataType.TypeName.DICTIONARY.value:
            return DataType.Type.DICTIONARY
        case DataType.TypeName.DATETIME.value:
            return DataType.Type.DATETIME
        case DataType.TypeName.BINARY.value:
            return DataType.Type.BINARY
        case _:
            return DataType.Type.STRING

class Table1ColumnName(Enum):
    COLUMN_TABLE_NAME = "Table Name"
    COLUMN_IS_ENTITY = "Is Entity"
    COLUMN_IS_DOMAIN = "Is Domain"
    COLUMN_IS_VIEW = "Is View"
    COLUMN_IS_ALIAS_SPECIFIC = "Is Alias Specific"

class Table1ColumnType(Enum):
    COLUMN_TABLE_NAME = DataType.Type.STRING
    COLUMN_IS_ENTITY = DataType.Type.BOOLEAN
    COLUMN_IS_DOMAIN = DataType.Type.BOOLEAN
    COLUMN_IS_VIEW = DataType.Type.BOOLEAN
    COLUMN_IS_ALIAS_SPECIFIC = DataType.Type.BOOLEAN

class Table1ColumnOrder(Enum):
    COLUMN_TABLE_NAME = 1
    COLUMN_IS_ENTITY = 2
    COLUMN_IS_DOMAIN = 3
    COLUMN_IS_VIEW = 4
    COLUMN_IS_ALIAS_SPECIFIC = 5

class Table2ColumnName(Enum):
    COLUMN_VARIABLE_NAME = "Variable Name"
    COLUMN_PK = "PK"
    COLUMN_TABLE_NAME = "Table Name"
    COLUMN_ALLOCATION = "Allocation"
    COLUMN_DOMAIN = "Domain"

class Table2ColumnType(Enum):
    COLUMN_VARIABLE_NAME = DataType.Type.STRING
    COLUMN_PK = DataType.Type.BOOLEAN
    COLUMN_TABLE_NAME = DataType.Type.STRING
    COLUMN_ALLOCATION = DataType.Type.STRING
    COLUMN_DOMAIN = DataType.Type.STRING

class Table2ColumnOrder(Enum):
    COLUMN_VARIABLE_NAME = 1
    COLUMN_PK = 2
    COLUMN_TABLE_NAME = 3
    COLUMN_ALLOCATION = 4
    COLUMN_DOMAIN = 5

class IMConfigurationTable(Enum):
    DOMAIN = "DMDomain"

class IMConfigurationTableDomain(Enum):
    NAME = "Name"
    ENTITYID = "EntityID"