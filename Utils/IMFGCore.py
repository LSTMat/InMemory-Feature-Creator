from enum import Enum

class Table1ColumnName(Enum):
    COLUMN_TABLE_NAME = "Table Name"
    COLUMN_IS_ENTITY = "Is Entity"
    COLUMN_IS_DOMAIN = "Is Domain"
    COLUMN_IS_VIEW = "Is View"
    COLUMN_IS_ALIAS_SPECIFIC = "Is Alias Specific"

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