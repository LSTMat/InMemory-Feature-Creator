from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass(slots=True)
class Value:
    _value: str  # Stores the actual value of the column

    def __init__(self, value: str):
        # Use object.__setattr__ to set values since the class is frozen
        object.__setattr__(self, "_value", value)

    def set_value(self, new_value: str):
        self._value = new_value
    
    def get_value(self) -> str:
        return self._value
    
@dataclass(slots=True)
class Column:
    """Defines a Column with essential attributes such as name, type, and primary key status."""
    _value: Value  # Stores the actual value of the column
    _name: str  # Name of the column
    _is_pk: bool  # Indicates if the column is a Primary Key
    _column_type: str  # Data type of the column (e.g., Integer, String, DateTime, etc.)
    _reference_table_schema: Optional[str] = None
    _reference_table_name: Optional[str] = None
    _reference_column: Optional[str] = None

    def __init__(self, name: str, is_pk: bool, column_type: str
                 , value: Optional[str] = None
                 , reference_table_schema: Optional[str] = None
                 , reference_table_name: Optional[str] = None
                 , reference_column: Optional[str] = None):
        # Use object.__setattr__ to set values since the class is frozen
        object.__setattr__(self, "_value", Value(value))
        object.__setattr__(self, "_name", name)
        object.__setattr__(self, "_is_pk", is_pk)
        object.__setattr__(self, "_column_type", column_type)
        object.__setattr__(self, "_reference_table_schema", reference_table_schema)
        object.__setattr__(self, "_reference_table_name", reference_table_name)
        object.__setattr__(self, "_reference_column", reference_column)

    def set_value(self, new_value: str):
        if self._value is None:
            self._value = Value(new_value)
        else:
            self._value.set_value(new_value)
    
    def get_value(self) -> str:
        return self._value.get_value()
    
    def get_name(self) -> str:
        return self._name
    
    def is_primary_key(self) -> bool:
        return self._is_pk
    
    def get_reference_table_schema(self) -> str:
        return self._reference_table_schema
    
    def get_reference_table_name(self) -> str:
        return self._reference_table_name
    
    def get_reference_column(self) -> str:
        return self._reference_column

@dataclass(slots=True)
class Row:
    """Defines a Row with essential attributes, storing columns in a dictionary for fast access."""
    _row_number: int  # Unique row identifier
    _Columns: Dict[str, Column] = field(default_factory=dict)  # Dictionary of columns in the row

    def __init__(self, row_number: int, columns: Dict[str, Column]):
        object.__setattr__(self, "_row_number", row_number)
        object.__setattr__(self, "_Columns", columns if columns is not None else {})

    def __iter__(self):
        return iter(self._Columns)

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
    
    def row_exists(self, row_number: int) -> bool:
        for index in self._rows:
            if index == row_number:
                return True
        return False
    
    def get_schema_name(self) -> str:
        return self._schema_name
    
    def get_table_name(self) -> str:
        return self._table_name
    
    def get_rows(self) -> Dict[int, Row]:
        return self._rows

    def get_column_values(self, column_name: str) -> list[str]:
        return [row.get_column_value(column_name) for row in self._rows.values() if row.get_column_value(column_name) is not None]

    def filter_rows_by_condition(self, where_column_name: str, condition_value: str) -> list[Row]:
        return [row for row in self._rows.values() if row.get_columns()[where_column_name].get_value() == condition_value]
    
    def add_row(self, columns: Dict[str, Column]) -> int:
        """Adds a new row with auto-generated row number (max + 1)."""
        new_row_number = max(self._rows.keys(), default=-1) + 1  # Auto-increment row number
        self._rows[new_row_number] = Row(row_number=new_row_number, columns=columns)
        return new_row_number  # Return the new row number for reference

    def delete_row_by_row_number(self, row_number: int):
        """Deletes a single row by row_number."""
        if self.row_exists(row_number):
            del self._rows[row_number]
        else:
            raise ValueError(f"Row {row_number} does not exist.")

    def delete_rows_by_condition(self, where_column: str, where_value: str):
        """
        Deletes all rows where `where_column` matches `where_value`.

        Args:
            where_column (str): The column to filter rows by.
            where_value (str): The value that must match in `where_column`.
        """
        rows_to_delete = [row_number for row_number, row in self._rows.items()
                          if row.get_column_value(where_column) == where_value]

        if not rows_to_delete:
            raise ValueError(f"No rows found where {where_column} = '{where_value}'")

        for row_number in rows_to_delete:
            self.delete_row_by_row_number(row_number)

    def update_row_value_by_row_number(self, row_number: int, column_name: str, new_value: str):
        """Updates a specific column value within a row."""
        if row_number not in self._rows:
            raise ValueError(f"Row {row_number} does not exist.")
        if column_name not in self._rows[row_number].get_columns():
            raise ValueError(f"Column {column_name} does not exist in row {row_number}.")

        self._rows[row_number].get_columns()[column_name].set_value(new_value)

    def update_row_values_by_row_number(self, row_number: int, update_columns: Dict[str, str]):
        """Updates specific column values within a row."""
        if row_number not in self._rows:
            raise ValueError(f"Row {row_number} does not exist.")

        row = self._rows[row_number]
        for col_name, new_val in update_columns.items():
            if col_name in row.get_columns():
                row.get_columns()[col_name].set_value(new_val)
            else:
                raise ValueError(f"Column {col_name} does not exist in row {row_number}.")

    def update_row_value_by_condition(self, where_column: str, where_value: str, column_name: str, new_value: str):
        """
        Updates all rows where `where_column` matches `where_value`, modifying given column values.

        Args:
            where_column (str): The column to filter rows by.
            where_value (str): The value that must match in `where_column`.
            update_columns (Dict[str, str]): Dictionary of columns to update with new values.
        """
        rows_updated = 0
        for row_number, row in self._rows.items():
            if row.get_column_value(where_column) == where_value:
                self.update_row_value_by_row_number(row_number=row_number, column_name=column_name, new_value=new_value)
                rows_updated += 1

        if rows_updated == 0:
            raise ValueError(f"No rows found where {where_column} = '{where_value}'")
        else:
            print(f"Updated {rows_updated} row(s) where {where_column} = '{where_value}'")


    def update_row_values_by_condition(self, where_column: str, where_value: str, update_columns: Dict[str, str]):
        """
        Updates all rows where `where_column` matches `where_value`, modifying given column values.

        Args:
            where_column (str): The column to filter rows by.
            where_value (str): The value that must match in `where_column`.
            update_columns (Dict[str, str]): Dictionary of columns to update with new values.
        """
        rows_updated = 0
        for row_number, row in self._rows.items():
            if row.get_column_value(where_column) == where_value:
                self.update_row_values_by_row_number(row_number=row_number, update_columns=update_columns)
                rows_updated += 1

        if rows_updated == 0:
            raise ValueError(f"No rows found where {where_column} = '{where_value}'")
        else:
            print(f"Updated {rows_updated} row(s) where {where_column} = '{where_value}'")

@dataclass(slots=True, frozen=True)
class ModelConfiguration:
    """Configuration class that holds multiple tables, representing an in-memory database schema."""
    Name: str  # Name of the configuration
    Tables: List[Table] = field(default_factory=list)  # List of tables in the configuration

    def get_column_values(self, table_name: str, column_name: str) -> List[str]:
        for table in self.Tables:
            if table.get_table_name() == table_name:
                return table.get_column_values(column_name)  # Retrieve column values from the matching table
        return []  # Return an empty list if no matching table is found
    
    def get_Table(self, table_name: str) -> Table:
        for table in self.Tables:
            if table.get_table_name() == table_name:
                return  table # Retrieve the matched table
        return None  # Return an empty list if no matching table is found
    
    def add_row_to_table(self, table_name: str, columns: Dict[str, Column]) -> int:
        for table in self.Tables:
            if table.get_table_name() == table_name:
                return table.add_row(columns)  # Retrieve column values from the matching table
        return None  # Return an empty list if no matching table is found
    
    def set_column_value_by_row_number(self, table_name: str, row_number: str, column_name: str, new_value: str) -> List[str]:
        for table in self.Tables:
            if table.get_table_name() == table_name:
                return table.update_row_value_by_row_number(row_number, column_name=column_name, new_value=new_value)  # Retrieve column values from the matching table
        return []  # Return an empty list if no matching table is found
    
    def set_column_values_by_row_number(self, table_name: str, row_number: str, update_columns: Dict[str, str]) -> List[str]:
        for table in self.Tables:
            if table.get_table_name() == table_name:
                return table.update_row_values_by_row_number(row_number, update_columns)  # Retrieve column values from the matching table
        return []  # Return an empty list if no matching table is found
    
    def set_column_value_by_condition(self, table_name: str, where_column: str, where_value: str, column_name: str, new_value: str) -> List[str]:
        for table in self.Tables:
            if table.get_table_name() == table_name:
                return table.update_row_value_by_condition(where_column, where_value, column_name=column_name, new_value=new_value)  # Retrieve column values from the matching table
        return []  # Return an empty list if no matching table is found
    
    def set_column_values_by_condition(self, table_name: str, where_column: str, where_value: str, update_columns: Dict[str, str]) -> List[str]:
        for table in self.Tables:
            if table.get_table_name() == table_name:
                return table.update_row_values_by_condition(where_column, where_value, update_columns)  # Retrieve column values from the matching table
        return []  # Return an empty list if no matching table is found

    def get_column_values_filtered(self, table_name: str, column_name: str, FilterColumn: str, FilterValue : str) -> List[str]:
        for table in self.Tables:
            if table.get_table_name() == table_name:
                print("Table Name: ", table_name)
                Rows = table.filter_rows_by_condition(FilterColumn, FilterValue)
                for Row in Rows:
                    return Row.get_column_value(column_name)  # Retrieve column values from the matching table
        return []  # Return an empty list if no matching table is found