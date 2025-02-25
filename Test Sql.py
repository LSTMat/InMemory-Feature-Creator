import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
from Utils.InMemoryConfiguration import load_xml_to_config
from Utils.SQLGenerator import generate_insert_sql
from Utils.TableModel import ModelConfiguration, Table, Row, Column, Value

table_def = [Table("dbo", "TableDefinition", {1: Row(1, {
                    "Table Name"        : Column("M_New_Table_1", "Table Name", True, "String"),
                    "Entity"            : Column("True", "Entity", False, "Boolean"),
                    "Domain"            : Column("False", "Domain", False, "Boolean"),
                    "View"              : Column("False", "View", False, "Boolean"),
                    "Alias Specific"    : Column("False", "Alias Specific", False, "Boolean")
                })

                , 2: Row(2, {
                    "Table Name"        : Column("M_New_Table_2", "Table Name", True, "String"),
                    "Entity"            : Column("True", "Entity", False, "Boolean"),
                    "Domain"            : Column("False", "Domain", False, "Boolean"),
                    "View"              : Column("False", "View", False, "Boolean"),
                    "Alias Specific"    : Column("False", "Alias Specific", False, "Boolean")
                })
                # , 3: Row(3, {
                #     "Table Name"        : Column("M_New_Table_3", "Table Name", True, "String"),
                #     "Entity"            : Column("True", "Entity", False, "Boolean"),
                #     "Domain"            : Column("True", "Domain", False, "Boolean"),
                #     "View"              : Column("False", "View", False, "Boolean"),
                #     "Alias Specific"    : Column("False", "Alias Specific", False, "Boolean")
                # })
                # , 4: Row(4, {
                #     "Table Name"        : Column("M_New_Table_4", "Table Name", True, "String"),
                #     "Entity"            : Column("False", "Entity", False, "Boolean"),
                #     "Domain"            : Column("False", "Domain", False, "Boolean"),
                #     "View"              : Column("True", "View", False, "Boolean"),
                #     "Alias Specific"    : Column("False", "Alias Specific", False, "Boolean")
                # })
                # , 5: Row(5, {
                #     "Table Name"        : Column("M_New_Table_5", "Table Name", True, "String"),
                #     "Entity"            : Column("False", "Entity", False, "Boolean"),
                #     "Domain"            : Column("False", "Domain", False, "Boolean"),
                #     "View"              : Column("True", "View", False, "Boolean"),
                #     "Alias Specific"    : Column("True", "Alias Specific", False, "Boolean")
                # })
                })]
table_Key = [Table("dbo", "KeyColumnDefinition", {1: Row(1, {
                    "Table Name"        : Column("M_New_Table_1", "Table Name", True, "String"),
                    "Key"               : Column("Key_1", "Key", True, "String"),
                    "PK"                : Column("True", "PK", False, "Boolean"),
                    "Domain"            : Column("", "Domain", False, "String")
                })


                , 2: Row(2, {
                    "Table Name"        : Column("M_New_Table_2", "Table Name", True, "String"),
                    "Key"               : Column("Key_2", "Key", True, "String"),
                    "PK"                : Column("True", "PK", False, "Boolean"),
                    "Domain"            : Column("", "Domain", False, "String")
                })
                , 3: Row(3, {
                    "Table Name"        : Column("M_New_Table_2", "Table Name", True, "String"),
                    "Key"               : Column("Key_1", "Key", True, "String"),
                    "PK"                : Column("False", "PK", False, "Boolean"),
                    "Domain"            : Column("", "Domain", False, "String")
                })
                })]
table_Var = [Table("dbo", "VariableColumnDefinition", {1: Row(1, {
                    "Table Name"        : Column("M_New_Table_1", "Table Name", True, "String"),
                    "Variabile"         : Column("Vaiable_1", "Variabile", True, "String"),
                    "Type"              : Column("INTEGER", "Type", False, "String"),
                    "Precision"         : Column("0", "Precision", False, "Integer"),
                    "Scale"             : Column("0", "Scale", False, "Integer"),
                    "Lenght"            : Column("0", "Lenght", False, "Integer")
                })
                , 2: Row(2, {
                    "Table Name"        : Column("M_New_Table_1", "Table Name", True, "String"),
                    "Variabile"         : Column("Vaiable_2", "Variabile", True, "String"),
                    "Type"              : Column("NVARCHAR", "Type", False, "String"),
                    "Precision"         : Column("False", "Precision", False, "Integer"),
                    "Scale"             : Column("False", "Scale", False, "Integer"),
                    "Lenght"            : Column("40", "Lenght", False, "Integer")
                })
                , 3: Row(3, {
                    "Table Name"        : Column("M_New_Table_1", "Table Name", True, "String"),
                    "Variabile"         : Column("Vaiable_3", "Variabile", True, "String"),
                    "Type"              : Column("DECIMAL", "Type", False, "String"),
                    "Precision"         : Column("8", "Precision", False, "Integer"),
                    "Scale"             : Column("2", "Scale", False, "Integer"),
                    "Lenght"            : Column("0", "Lenght", False, "Integer")
                })

                
                , 5: Row(5, {
                    "Table Name"        : Column("M_New_Table_2", "Table Name", True, "String"),
                    "Variabile"         : Column("Vaiable_5", "Variabile", True, "String"),
                    "Type"              : Column("NVARCHAR", "Type", False, "String"),
                    "Precision"         : Column("0", "Precision", False, "Integer"),
                    "Scale"             : Column("0", "Scale", False, "Integer"),
                    "Lenght"            : Column("512", "Lenght", False, "Integer")
                })
                , 6: Row(6, {
                    "Table Name"        : Column("M_New_Table_2", "Table Name", True, "String"),
                    "Variabile"         : Column("Vaiable_6", "Variabile", True, "String"),
                    "Type"              : Column("NVARCHAR", "Type", False, "String"),
                    "Precision"         : Column("0", "Precision", False, "Integer"),
                    "Scale"             : Column("0", "Scale", False, "Integer"),
                    "Lenght"            : Column("256", "Lenght", False, "Integer")
                })
                , 7: Row(7, {
                    "Table Name"        : Column("M_New_Table_2", "Table Name", True, "String"),
                    "Variabile"         : Column("Vaiable_7", "Variabile", True, "String"),
                    "Type"              : Column("NVARCHAR", "Type", False, "String"),
                    "Precision"         : Column("0", "Precision", False, "Integer"),
                    "Scale"             : Column("0", "Scale", False, "Integer"),
                    "Lenght"            : Column("40", "Lenght", False, "Integer")
                })
                })]

tables = table_def + table_Key + table_Var
dd_data_stored = ModelConfiguration(Name="Test Config", Tables=tables)

a = 1
# sql_script = generate_insert_sql(table)
# print(sql_script)

# feature_finder = FeatureKeyFinder(data_store)
# sql_generator = SQLGenerator(mapping, feature_finder)

# # Generate SQL for a sample row
# data_to_insert = {"AlgorithmConfigurationID": "ALG001", "DisplayName": "Test Algorithm"}
# sql_query = sql_generator.generate_insert_sql("DDAlgorithmConfiguration", data_to_insert)
# print(sql_query)
