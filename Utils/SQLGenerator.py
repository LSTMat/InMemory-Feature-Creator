from .TableModel import Table

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
        col_names = "], [".join(columns.keys())
        col_values = ", ".join(f"'{col.get_value()}'" for col in columns.values())
        sql_statements.append(f"INSERT INTO [{table_schema}].[{table_name}] ([{col_names}]) VALUES ({col_values});")
    
    return "\n".join(sql_statements)

# Example Usage
# Assuming you have a Table object named `table`
# sql_script = generate_insert_sql(table)
# print(sql_script)
