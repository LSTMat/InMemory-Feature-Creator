from .TableModel import Table
from .IMFGCore import DataType

def generate_insert_sql(table: Table) -> str:
    """Generates an SQL INSERT statement for the given Table object."""
    if table is None:
        return ""
    
    table_schema = table.get_schema_name()
    table_name = table.get_table_name()
    rows = table.get_rows()
    
    sql_statements = []
    
    for row in rows.values():
        columns = row.get_columns()
        col_names = []
        col_values = []
        
        for col_name, col in columns.items():
            value = col.get_value()
            data_type = col.get_type()
            if value is not None:
                col_names.append(f"[{col_name}]")
                if data_type in [DataType.Type.INTEGER, DataType.Type.FLOAT]:
                    col_values.append(f"{value}")
                elif data_type == DataType.Type.BOOLEAN:
                    col_values.append(f"{1 if value else 0}")
                elif data_type == DataType.Type.STRING:
                    col_values.append(f"N'{value}'")
                # elif data_type == DataType.Type.LIST:
                #     col_values.append(f"N'{','.join(map(str, value))}'")
                # elif data_type == DataType.Type.DICTIONARY:
                #     col_values.append(f"N'{str(value)}'")
                elif data_type == DataType.Type.DATETIME:
                    col_values.append(f"'{value.isoformat()}'")
                elif data_type == DataType.Type.BINARY:
                    col_values.append(f"0x{value.hex()}")
        
        if col_names and col_values:
            col_names_str = ", ".join(col_names)
            col_values_str = ", ".join(col_values)
            sql_statements.append(f"INSERT INTO [{table_schema}].[{table_name}] ({col_names_str}) VALUES ({col_values_str});")

    return "\n".join(sql_statements)
# Example Usage
# Assuming you have a Table object named `table`
# sql_script = generate_insert_sql(table)
# print(sql_script)
