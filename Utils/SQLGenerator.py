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
        col_identity = []
        col_names = []
        col_values = []
        sql_declare_identity_variable = []
        sql_set_identity_variable = []
        
        for col_name, col in columns.items():
            value = col.get_value()
            if col.is_identity():
                sql_declare_identity_variable = f"DECLARE {col.get_value()} AS INTEGER; "
                sql_set_identity_variable = f" SET {col.get_value()} = SCOPE_IDENTITY();"
            else:
                data_type = col.get_type()
                if value is not None:
                    col_names.append(f"[{col_name}]")
                    if data_type in [DataType.Type.INTEGER, DataType.Type.FLOAT]:
                        col_values.append(f"{value}")
                    elif data_type == DataType.Type.BOOLEAN:
                        col_values.append(f"{1 if value else 0}")
                    elif data_type == DataType.Type.STRING:
                        col_values.append(f"N'{value}'")
                    elif data_type == DataType.Type.DATETIME:
                        col_values.append(f"'{value.isoformat()}'")
                    elif data_type == DataType.Type.BINARY:
                        col_values.append(f"0x{value.hex()}")
        
        if col_names and col_values:
            col_names_str = ", ".join(col_names)
            col_values_str = ", ".join(col_values)
            sql_insert = sql_declare_identity_variable + f"INSERT INTO [{table_schema}].[{table_name}] ({col_names_str}) VALUES ({col_values_str});" + sql_set_identity_variable
            sql_statements.append(sql_insert)

    return "\n".join(sql_statements)
# Example Usage
# Assuming you have a Table object named `table`
# sql_script = generate_insert_sql(table)
# print(sql_script)
