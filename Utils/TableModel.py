from dataclasses import dataclass, field
from typing import Dict

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

    def __post_init__(self):
        # Create an index for quick lookups by column values
        object.__setattr__(self, "_index", {})
        for row in self._rows.values():
            for column_name, column in row.get_columns().items():
                if column_name not in self._index:
                    self._index[column_name] = {}
                if column.get_value() not in self._index[column_name]:
                    self._index[column_name][column.get_value()] = []
                self._index[column_name][column.get_value()].append(row)

    def get_schema_name(self) -> str:
        return self._schema_name
    
    def get_table_name(self) -> str:
        return self._table_name
    
    def get_rows(self) -> Dict[int, Row]:
        return self._rows

    def get_column_values(self, column_name: str) -> list[str]:
        return [row.get_column_value(column_name) for row in self._rows.values() if row.get_column_value(column_name) is not None]

    def filter_rows_by_condition(self, where_column_name: str, condition_value: str) -> list[Row]:
        return self._index.get(where_column_name, {}).get(condition_value, [])
