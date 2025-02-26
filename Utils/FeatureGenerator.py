import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
from Utils import (
        Table1ColumnType, DataTypeName, get_variable_type,
        Table, Row, Column, ModelConfiguration
    )

table_def = [Table(schema_name="dbo", table_name="TableDefinition", rows={1: Row(row_number=1, columns={
                    "Table Name"        : Column(value="M_New_Table_1", column_name="Table Name", is_pk=True, column_type="String"),
                    "Entity"            : Column(value="True", column_name="Entity", is_pk=False, column_type="Boolean"),
                    "Domain"            : Column(value="False", column_name="Domain", is_pk=False, column_type="Boolean"),
                    "View"              : Column(value="False", column_name="View", is_pk=False, column_type="Boolean"),
                    "Alias Specific"    : Column(value="False", column_name="Alias Specific", is_pk=False, column_type="Boolean")
                })

                , 2: Row(row_number=2, columns={
                    "Table Name"        : Column(value="M_New_Table_2", column_name="Table Name", is_pk=True, column_type="String"),
                    "Entity"            : Column(value="True", column_name="Entity", is_pk=False, column_type="Boolean"),
                    "Domain"            : Column(value="False", column_name="Domain", is_pk=False, column_type="Boolean"),
                    "View"              : Column(value="False", column_name="View", is_pk=False, column_type="Boolean"),
                    "Alias Specific"    : Column(value="False", column_name="Alias Specific", is_pk=False, column_type="Boolean")
                })
                })]
table_Key = [Table(schema_name="dbo", table_name="KeyColumnDefinition", rows={1: Row(row_number=1, columns={
                    "Table Name"        : Column(value="M_New_Table_1", column_name="Table Name", is_pk=True, column_type="String"),
                    "Key"               : Column(value="Key_1", column_name="Key", is_pk=True, column_type="String"),
                    "PK"                : Column(value="True", column_name="PK", is_pk=False, column_type="Boolean"),
                    "Domain"            : Column(value="", column_name="Domain", is_pk=False, column_type="String")
                })


                , 2: Row(row_number=2, columns={
                    "Table Name"        : Column(value="M_New_Table_2", column_name="Table Name", is_pk=True, column_type="String"),
                    "Key"               : Column(value="Key_2", column_name="Key", is_pk=True, column_type="String"),
                    "PK"                : Column(value="True", column_name="PK", is_pk=False, column_type="Boolean"),
                    "Domain"            : Column(value="", column_name="Domain", is_pk=False, column_type="String")
                })
                , 3: Row(row_number=3, columns={
                    "Table Name"        : Column(value="M_New_Table_2", column_name="Table Name", is_pk=True, column_type="String"),
                    "Key"               : Column(value="Key_1", column_name="Key", is_pk=True, column_type="String"),
                    "PK"                : Column(value="False", column_name="PK", is_pk=False, column_type="Boolean"),
                    "Domain"            : Column(value="", column_name="Domain", is_pk=False, column_type="String")
                })
                })]
table_Var = [Table(schema_name="dbo", table_name="VariableColumnDefinition", rows={1: Row(row_number=1, columns={
                    "Table Name"        : Column(value="M_New_Table_1", column_name="Table Name", is_pk=True, column_type="String"),
                    "Variabile"         : Column(value="Vaiable_1", column_name="Variabile", is_pk=True, column_type="String"),
                    "Type"              : Column(value="INTEGER", column_name="Type", is_pk=False, column_type="String"),
                    "Precision"         : Column(value="0", column_name="Precision", is_pk=False, column_type="Integer"),
                    "Scale"             : Column(value="0", column_name="Scale", is_pk=False, column_type="Integer"),
                    "Lenght"            : Column(value="0", column_name="Lenght", is_pk=False, column_type="Integer")
                })
                , 2: Row(row_number=2, columns={
                    "Table Name"        : Column(value="M_New_Table_1", column_name="Table Name", is_pk=True, column_type="String"),
                    "Variabile"         : Column(value="Vaiable_2", column_name="Variabile", is_pk=True, column_type="String"),
                    "Type"              : Column(value="NVARCHAR", column_name="Type", is_pk=False, column_type="String"),
                    "Precision"         : Column(value="False", column_name="Precision", is_pk=False, column_type="Integer"),
                    "Scale"             : Column(value="False", column_name="Scale", is_pk=False, column_type="Integer"),
                    "Lenght"            : Column(value="40", column_name="Lenght", is_pk=False, column_type="Integer")
                })
                , 3: Row(row_number=3, columns={
                    "Table Name"        : Column(value="M_New_Table_1", column_name="Table Name", is_pk=True, column_type="String"),
                    "Variabile"         : Column(value="Vaiable_3", column_name="Variabile", is_pk=True, column_type="String"),
                    "Type"              : Column(value="DECIMAL", column_name="Type", is_pk=False, column_type="String"),
                    "Precision"         : Column(value="8", column_name="Precision", is_pk=False, column_type="Integer"),
                    "Scale"             : Column(value="2", column_name="Scale", is_pk=False, column_type="Integer"),
                    "Lenght"            : Column(value="0", column_name="Lenght", is_pk=False, column_type="Integer")
                })

                
                , 5: Row(row_number=5, columns={
                    "Table Name"        : Column(value="M_New_Table_2", column_name="Table Name", is_pk=True, column_type="String"),
                    "Variabile"         : Column(value="Vaiable_5", column_name="Variabile", is_pk=True, column_type="String"),
                    "Type"              : Column(value="NVARCHAR", column_name="Type", is_pk=False, column_type="String"),
                    "Precision"         : Column(value="0", column_name="Precision", is_pk=False, column_type="Integer"),
                    "Scale"             : Column(value="0", column_name="Scale", is_pk=False, column_type="Integer"),
                    "Lenght"            : Column(value="512", column_name="Lenght", is_pk=False, column_type="Integer")
                })
                , 6: Row(row_number=6, columns={
                    "Table Name"        : Column(value="M_New_Table_2", column_name="Table Name", is_pk=True, column_type="String"),
                    "Variabile"         : Column(value="Vaiable_6", column_name="Variabile", is_pk=True, column_type="String"),
                    "Type"              : Column(value="NVARCHAR", column_name="Type", is_pk=False, column_type="String"),
                    "Precision"         : Column(value="0", column_name="Precision", is_pk=False, column_type="Integer"),
                    "Scale"             : Column(value="0", column_name="Scale", is_pk=False, column_type="Integer"),
                    "Lenght"            : Column(value="256", column_name="Lenght", is_pk=False, column_type="Integer")
                })
                , 7: Row(row_number=7, columns={
                    "Table Name"        : Column(value="M_New_Table_2", column_name="Table Name", is_pk=True, column_type="String"),
                    "Variabile"         : Column(value="Vaiable_7", column_name="Variabile", is_pk=True, column_type="String"),
                    "Type"              : Column(value="NVARCHAR", column_name="Type", is_pk=False, column_type="String"),
                    "Precision"         : Column(value="0", column_name="Precision", is_pk=False, column_type="Integer"),
                    "Scale"             : Column(value="0", column_name="Scale", is_pk=False, column_type="Integer"),
                    "Lenght"            : Column(value="40", column_name="Lenght", is_pk=False, column_type="Integer")
                })
                })]

tables = table_def + table_Key + table_Var
dd_data_stored = ModelConfiguration(Name="Test Config", Tables=tables)

def create_new_feature(DDModel: ModelConfiguration) -> Table:
    return Table(schema_name="dbo", table_name="NewFeature")

get_DD_ModelConfiguration_Structure

create_new_feature(dd_data_stored)