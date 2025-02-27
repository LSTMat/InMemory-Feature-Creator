from enum import Enum
from datetime import datetime

DD_MODEL_FILE = "DD\\DD Model only necessary.xml"

class DataType:

    class Type(Enum):
        STRING = str
        INTEGER = int
        SMALLINT = int
        FLOAT = float
        DECIMAL = float
        BIT = int
        BOOLEAN = bool
        LIST = list
        DICTIONARY = dict
        DATETIME = datetime
        BINARY = bytes

    class TypeName(Enum):
        STRING = "STRING"
        INTEGER = "INTEGER"
        SMALLINT = "SMALLINT"
        FLOAT = "FLOAT"
        DECIMAL = "DECIMAL"
        BIT = "BIT"
        BOOLEAN = "BOOLEAN"
        LIST = "LIST"
        DICTIONARY = "DICTIONARY"
        DATETIME = "DATETIME"
        BINARY = "BINARY"

    class DSType(Enum):
        STRING = 12
        INTEGER = 8
        SMALLINT = 16
        FLOAT = 6
        DECIMAL = 5
        BIT = 2
        BOOLEAN = 2
        DATETIME = 4
        BINARY = 7
        

    @staticmethod
    def get_variable_type(type_name: str) -> Type:
        return {
            DataType.TypeName.STRING.value: DataType.Type.STRING,
            "NVARCHAR": DataType.Type.STRING,
            DataType.TypeName.INTEGER.value: DataType.Type.INTEGER,
            "INT": DataType.Type.INTEGER,
            DataType.TypeName.FLOAT.value: DataType.Type.FLOAT,
            DataType.TypeName.DECIMAL.value: DataType.Type.DECIMAL,
            DataType.TypeName.BIT.value: DataType.Type.BIT,
            DataType.TypeName.BOOLEAN.value: DataType.Type.BOOLEAN,
            DataType.TypeName.LIST.value: DataType.Type.LIST,
            DataType.TypeName.DICTIONARY.value: DataType.Type.DICTIONARY,
            DataType.TypeName.DATETIME.value: DataType.Type.DATETIME,
            "DATE": DataType.Type.DATETIME,
            DataType.TypeName.BINARY.value: DataType.Type.BINARY,
            "IMAGE": DataType.Type.BINARY
        }.get(type_name.upper(), DataType.Type.STRING)
    
    @staticmethod
    def get_variable_DSType(type_name: str) -> DSType:
        return {
            DataType.TypeName.STRING.value: DataType.DSType.STRING,
            "NVARCHAR": DataType.DSType.STRING,
            DataType.TypeName.INTEGER.value: DataType.DSType.INTEGER,
            "INT": DataType.DSType.INTEGER,
            DataType.TypeName.FLOAT.value: DataType.DSType.FLOAT,
            DataType.TypeName.DECIMAL.value: DataType.DSType.DECIMAL,
            DataType.TypeName.BIT.value: DataType.DSType.BIT,
            DataType.TypeName.BOOLEAN.value: DataType.DSType.BOOLEAN,
            DataType.TypeName.DATETIME.value: DataType.DSType.DATETIME,
            "DATE": DataType.DSType.DATETIME,
            DataType.TypeName.BINARY.value: DataType.DSType.BINARY,
            "IMAGE": DataType.DSType.BINARY
        }.get(type_name.upper(), DataType.DSType.STRING)
    
    @staticmethod
    def get_variable_Aggregation(type_name: str) -> str:
        return {
            DataType.TypeName.STRING.value: "FirstChildStringStdOp",
            "NVARCHAR": "FirstChildStringStdOp",
            DataType.TypeName.INTEGER.value: "SumNumStdOp",
            "INT": "SumNumStdOp",
            DataType.TypeName.FLOAT.value: "SumNumStdOp",
            DataType.TypeName.DECIMAL.value: "SumNumStdOp",
            DataType.TypeName.BIT.value: "FirstChildStringStdOp",
            DataType.TypeName.BOOLEAN.value: "FirstChildStringStdOp",
            DataType.TypeName.DATETIME.value: "FirstChildDateTimeStdOp",
            "DATE": "FirstChildDateTimeStdOp",
            DataType.TypeName.BINARY.value: "FirstChildStringStdOp",
            "IMAGE": "FirstChildStringStdOp"
        }.get(type_name.upper(), "FirstChildStringStdOp")

    @staticmethod
    def get_variable_Allocation(type_name: str) -> str:
        return {
            DataType.TypeName.STRING.value: "ReplicateStringSplitStdOp",
            "NVARCHAR": "ReplicateStringSplitStdOp",
            DataType.TypeName.INTEGER.value: "ProportionalNumStdOp",
            "INT": "ProportionalNumStdOp",
            DataType.TypeName.FLOAT.value: "ProportionalNumStdOp",
            DataType.TypeName.DECIMAL.value: "ProportionalNumStdOp",
            DataType.TypeName.BIT.value: "ProportionalNumStdOp",
            DataType.TypeName.BOOLEAN.value: "ProportionalNumStdOp",
            DataType.TypeName.DATETIME.value: "ReplicateDateTimeSplitStdOp",
            "DATE": "ReplicateDateTimeSplitStdOp",
            DataType.TypeName.BINARY.value: "ReplicateStringSplitStdOp",
            "IMAGE": "ReplicateStringSplitStdOp"
        }.get(type_name.upper(), "ReplicateStringSplitStdOp")


class Table1ColumnName(Enum):
    COLUMN_TABLE_NAME           = "Table Name"
    COLUMN_IS_ENTITY            = "Is Entity"
    COLUMN_IS_DOMAIN            = "Is Domain"
    COLUMN_IS_VIEW              = "Is View"
    COLUMN_IS_ALIAS_SPECIFIC    = "Is Alias Specific"

class Table1ColumnType(Enum):
    COLUMN_TABLE_NAME = DataType.Type.STRING
    COLUMN_IS_ENTITY = DataType.Type.BOOLEAN
    COLUMN_IS_DOMAIN = DataType.Type.BOOLEAN
    COLUMN_IS_VIEW = DataType.Type.BOOLEAN
    COLUMN_IS_ALIAS_SPECIFIC = DataType.Type.BOOLEAN

class Table1ColumnOrder(Enum):
    COLUMN_TABLE_NAME           = 1
    COLUMN_IS_ENTITY            = 2
    COLUMN_IS_DOMAIN            = 3
    COLUMN_IS_VIEW              = 4
    COLUMN_IS_ALIAS_SPECIFIC    = 5

class Table2ColumnName(Enum):
    COLUMN_VARIABLE_NAME    = "Variable Name"
    COLUMN_PK               = "PK"
    COLUMN_TABLE_NAME       = "Table Name"
    COLUMN_ALLOCATION       = "Allocation"
    COLUMN_DOMAIN           = "Domain"

class Table2ColumnType(Enum):
    COLUMN_VARIABLE_NAME = DataType.Type.STRING
    COLUMN_PK = DataType.Type.BOOLEAN
    COLUMN_TABLE_NAME = DataType.Type.STRING
    COLUMN_ALLOCATION = DataType.Type.STRING
    COLUMN_DOMAIN = DataType.Type.STRING

class Table2ColumnOrder(Enum):
    COLUMN_VARIABLE_NAME    = 1
    COLUMN_PK               = 2
    COLUMN_TABLE_NAME       = 3
    COLUMN_ALLOCATION       = 4
    COLUMN_DOMAIN           = 5

class Table3ColumnName(Enum):
    COLUMN_TABLE_NAME           = "Table Name"
    COLUMN_VARIABLE_NAME        = "Variable Name"
    COLUMN_IS_PK                = "Is PK"
    COLUMN_IS_DOMAIN            = "Is Domain"
    COLUMN_IS_VARIABLE          = "Is Variable"
    COLUMN_VARIABLE_TYPE        = "Variable Type"
    COLUMN_VARIABLE_PRECISION   = "Variable Precision"
    COLUMN_VARIABLE_SCALE       = "Variable Scale"
    COLUMN_VARIABLE_LENGHT      = "Variable Lenght"
    INTERN_ROW_NUMBER           = "Row Number"

class Table3ColumnType(Enum):
    COLUMN_TABLE_NAME           = DataType.Type.STRING
    COLUMN_VARIABLE_NAME        = DataType.Type.STRING
    COLUMN_IS_PK                = DataType.Type.BOOLEAN
    COLUMN_IS_DOMAIN            = DataType.Type.BOOLEAN
    COLUMN_IS_VARIABLE          = DataType.Type.BOOLEAN
    COLUMN_VARIABLE_TYPE        = DataType.Type.STRING
    COLUMN_VARIABLE_PRECISION   = DataType.Type.INTEGER
    COLUMN_VARIABLE_SCALE       = DataType.Type.INTEGER
    COLUMN_VARIABLE_LENGHT      = DataType.Type.INTEGER
    INTERN_ROW_NUMBER           = DataType.Type.INTEGER

class Table3ColumnOrder(Enum):
    COLUMN_TABLE_NAME           = 0
    COLUMN_VARIABLE_NAME        = 1
    COLUMN_IS_PK                = 2
    COLUMN_IS_DOMAIN            = 3
    COLUMN_IS_VARIABLE          = 4
    COLUMN_VARIABLE_TYPE        = 5
    COLUMN_VARIABLE_PRECISION   = 6
    COLUMN_VARIABLE_SCALE       = 7
    COLUMN_VARIABLE_LENGHT      = 8
    INTERN_ROW_NUMBER           = 9

class VariableType(Enum):
    INTEGER     = "INTEGER"
    NVARCHAR    = "NVARCHAR"
    DECIMAL     = "DECIMAL"
    DATE        = "DATE"
    DATETIME    = "DATETIME"

class TabName(Enum):
    TAB1    = "Tabelle"
    TAB2    = "Calculation Plan"
    TAB3    = "Variabili"

class IMConfigurationTable(Enum):
    DOMAIN              = "DMDomain"
    MODELTABLE          = "DMModelTable"
    MODELTABLECOLUMN    = "DMModelTableColumn"

class IMConfigurationDomain(Enum):
    NAME        = "Name"
    ENTITYID    = "EntityID"

class IMConfigurationModelTable(Enum):
    MODELID         = "ModelID"
    PHYSICALNAME    = "PhysicalName"

class IMConfigurationModelTableColumn(Enum):
    MODELID         = "ModelID"
    FIELDNAME       = "FieldName"