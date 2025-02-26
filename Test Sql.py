import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
from Utils import (
        Table1ColumnType, DataType, get_DD_ModelConfiguration_Structure, DD_MODEL_FILE, generate_insert_sql,
        Table, Row, Column, ModelConfiguration, Value
    )

def add_underscore(name: str) -> str:
    if name is None:
        return ""
    return name.replace(' ', '_')

def get_physical_name(table_name: str, is_entity: bool, is_view: bool) -> str:
    prefix = "E" if is_entity else "M"
    if is_view:
        prefix = "V" if is_entity else "VC"
    return f"{prefix}_{add_underscore(table_name)}"

def determine_field_type(variableCol: Dict[str, Column]) -> str:
    if variableCol["IsVariable"].get_value() == "True":
        return "variable"
    elif variableCol["PK"].get_value() == "True":
        return "pk"
    else:
        return "entity"  
            
def add_ddfeature_row(DDTable: Table, AliasName: str):
    DDTable.add_row(columns={
        "FeatureKey":                       Column(value="@FeatureKey", column_name="FeatureKey", is_pk=True, column_type="Integer", is_identity=True),
        "FeatureID":                        Column(value="F001", column_name="FeatureID", is_pk=False, column_type="String"),
        "FeatureName":                      Column(value="New Feature", column_name="FeatureName", is_pk=False, column_type="String"),
        "BusinessDescription":              Column(value="Description of the new feature made using the IFG", column_name="BusinessDescription", is_pk=False, column_type="String"),
        "FeatureStatus":                    Column(value=None, column_name="FeatureStatus", is_pk=False, column_type="Integer"),
        "CurrentAliasID":                   Column(value=AliasName, column_name="CurrentAliasID", is_pk=False, column_type="String"),
        "IncludeSYParam":                   Column(value=None, column_name="IncludeSYParam", is_pk=False, column_type="Integer"),
        "DeployAllModel":                   Column(value=None, column_name="DeployAllModel", is_pk=False, column_type="Integer"),
        "SyncCustomOnDeploy":               Column(value=None, column_name="SyncCustomOnDeploy", is_pk=False, column_type="Integer"),
        "PreScript":                        Column(value=None, column_name="PreScript", is_pk=False, column_type="String"),
        "PostScript":                       Column(value=None, column_name="PostScript", is_pk=False, column_type="String"),
        "PurgeDeletedObjects":              Column(value=None, column_name="PurgeDeletedObjects", is_pk=False, column_type="Integer"),
        "IncludeConditionalFormatting":     Column(value=None, column_name="IncludeConditionalFormatting", is_pk=False, column_type="Integer"),
        "IncludeAlias":                     Column(value=None, column_name="IncludeAlias", is_pk=False, column_type="Integer"),
        "IncludeApplicationLayoutTables":   Column(value=None, column_name="IncludeApplicationLayoutTables", is_pk=False, column_type="Integer"),
        "IncludeWritebackTables":           Column(value=None, column_name="IncludeWritebackTables", is_pk=False, column_type="Integer"),
        "IncludeInfoPointTables":           Column(value=None, column_name="IncludeInfoPointTables", is_pk=False, column_type="Integer")
    })

def add_ddVariables(DDModel_To_Update: ModelConfiguration, DataTUse: ModelConfiguration, table_name: str):
    tab = DataTUse.get_Table(table_name="VariableDefinition")
    sequence_no = 1
    for row in tab.get_rows().values():
        columns = row.get_columns()
        if columns["IsVariable"].get_value() == "True":
            variableCol = row.get_columns()
            DDModel_To_Update.add_row_to_table(table_name=table_name, columns={
                    "FeatureKey":                   Column(value="@FeatureKey", column_name="FeatureKey", is_pk=True, column_type="Integer"),
                    "VariableKey":                  Column(value=f"@VariableKey{sequence_no}", column_name="VariableKey", is_pk=True, column_type="Integer", is_identity=True),
                    "VariableID":                   Column(value=add_underscore(variableCol["Variabile"].get_value()), column_name="VariableID", is_pk=False, column_type="String"),
                    "PhysicalName":                 Column(value=add_underscore(variableCol["Variabile"].get_value()), column_name="PhysicalName", is_pk=False, column_type="String"),
                    "DisplayName":                  Column(value=variableCol["Variabile"].get_value(), column_name="DisplayName", is_pk=False, column_type="String"),
                    "DataType":                     Column(value=DataType.get_variable_DSType(variableCol["Type"].get_value()).value, column_name="DataType", is_pk=False, column_type="Integer"),
                    "Length":                       Column(value=variableCol["Length"].get_value(), column_name="Length", is_pk=False, column_type="Integer"),
                    "Precision":                    Column(value=variableCol["Precision"].get_value(), column_name="Precision", is_pk=False, column_type="Integer"),
                    "Scale":                        Column(value=variableCol["Scale"].get_value(), column_name="Scale", is_pk=False, column_type="Integer"),
                    "Aggregation":                  Column(value=DataType.get_variable_Aggregation(variableCol["Type"].get_value()), column_name="Aggregation", is_pk=False, column_type="String"),
                    "WritebackType":                Column(value="STANDARD", column_name="WritebackType", is_pk=False, column_type="String"),
                    "Allocation":                   Column(value=DataType.get_variable_Allocation(variableCol["Type"].get_value()), column_name="Allocation", is_pk=False, column_type="String"),
                    "Grouping":                     Column(value="NEW VARIABLES", column_name="Grouping", is_pk=False, column_type="String"),
                    "CRUDStatus":                   Column(value="c", column_name="CRUDStatus", is_pk=False, column_type="String")
                })
        sequence_no += 1

def add_ddmodeltable(DDModel_To_Update: ModelConfiguration, DataTUse: ModelConfiguration, table_name: str):
    tab = DataTUse.get_Table(table_name="TableDefinition")
    sequence_no = 1
    for row in tab.get_rows().values():
        variableCol = row.get_columns()
        DDModel_To_Update.add_row_to_table(table_name=table_name, columns={
                "FeatureKey":                  Column(value="@FeatureKey",                                                          column_name="FeatureKey",       is_pk=True,     column_type="Integer"),
                "ModelTableKey":               Column(value=f"@ModelTableKey{sequence_no}",                                         column_name="ModelTableKey",    is_pk=True,     column_type="Integer",  is_identity=True),
                "ModelID":                     Column(value=add_underscore(variableCol["Table Name"].get_value()),                  column_name="ModelID",          is_pk=False,    column_type="String"),
                "DisplayName":                 Column(value=variableCol["Table Name"].get_value(),                                  column_name="DisplayName",      is_pk=False,    column_type="String"),
                "PhysicalName":                Column(value=add_underscore(get_physical_name(variableCol["Table Name"].get_value(), 
                                                                                             variableCol["Entity"].get_value() == "True", 
                                                                                             variableCol["View"].get_value() == "True")),
                                                                                                                                    column_name="PhysicalName",     is_pk=False,    column_type="String"),
                "Managed":                     Column(value=0 if variableCol["View"].get_value() == "True" else 1,                  column_name="Managed",          is_pk=False,    column_type="Integer"),
                "ModelType":                   Column(value="ENTITY" if variableCol["Entity"].get_value() == "True" else "DATASET", column_name="ModelType",        is_pk=False,    column_type="String"),
                "AliasSpecific":               Column(value=1 if variableCol["Alias Specific"].get_value() == "True" else 0,        column_name="AliasSpecific",    is_pk=False,    column_type="Integer"),
                "CRUDStatus":                  Column(value="c",                                                                    column_name="CRUDStatus",       is_pk=False,    column_type="String")
            })
        sequence_no += 1

def add_DDModelTableColumn(DDModel_To_Update: ModelConfiguration, DataTUse: ModelConfiguration, table_name: str):
    DDModelTable_actual = DDModel_To_Update.get_Table(table_name="DDModelTable")
    if DDModelTable_actual.get_rows() == {}:
        raise KeyError("Table DDModelTable is empty")
        
    ModelTableKey_sequence_pk = {key: 1 for idx, key in enumerate(DDModelTable_actual.get_column_values(column_name="ModelTableKey"))}

    tab = DataTUse.get_Table(table_name="VariableDefinition")
    ModelTableColumnKey_sequence_no = 1
    for row in tab.get_rows().values():
        columns = row.get_columns()
        Table_Model_info = DDModelTable_actual.filter_rows_by_condition(where_column_name="DisplayName", condition_value=columns["Table Name"].get_value())[0].get_columns()
        Table_ModelId = Table_Model_info["ModelID"].get_value()
        Table_ModelTableKey = Table_Model_info["ModelTableKey"].get_value()

        columns = row.get_columns()
        variableCol = row.get_columns()
        field_type = determine_field_type(variableCol)
        sequence_value = 0 if field_type != "pk" else ModelTableKey_sequence_pk[Table_ModelTableKey]

        reference_model_id = None
        if variableCol["IsVariable"].get_value() == "True":
            dd_variable_table = DDModel_To_Update.get_Table(table_name="DDVariable")
            for dd_variable_row in dd_variable_table.get_rows().values():
                if dd_variable_row.get_columns()["DisplayName"].get_value() == variableCol["Variabile"].get_value():
                    reference_model_id = dd_variable_row.get_columns()["VariableID"].get_value()
                    break
        else:
            reference_model_id = Table_ModelId

        Unique_Column_Id = f"{Table_ModelId}"
        if field_type != "pk":
            Unique_Column_Id += f"_{reference_model_id}{"_Key" if field_type == 'entity' else ""}"

        DDModel_To_Update.add_row_to_table(table_name=table_name, columns={
                "FeatureKey":                  Column(value="@FeatureKey", column_name="FeatureKey", is_pk=True, column_type="Integer"),
                "ModelTableKey":               Column(value=Table_ModelTableKey, column_name="ModelTableKey", is_pk=True, column_type="Integer"),
                "ModelTableColumnKey":         Column(value=f"@ModelTableColumnKey{ModelTableColumnKey_sequence_no}", column_name="ModelTableColumnKey", is_pk=True, column_type="Integer", is_identity=True),
                "FieldName":                   Column(value=add_underscore(variableCol["Variabile"].get_value()), column_name="FieldName", is_pk=False, column_type="String"),
                "FieldType":                   Column(value=field_type, column_name="FieldType", is_pk=False, column_type="String"),
                "ReferenceModelID":            Column(value=reference_model_id, column_name="ReferenceModelID", is_pk=False, column_type="String"),
                "SequenceNo":                  Column(value=sequence_value, column_name="SequenceNo", is_pk=False, column_type="Integer"),
                # "DefaultValue":                Column(value=None, column_name="DefaultValue", is_pk=False, column_type="String"),
                # "OldFieldName":                Column(value=None, column_name="OldFieldName", is_pk=False, column_type="String"),
                "UniqueColumnId":              Column(value=Unique_Column_Id, column_name="UniqueColumnId", is_pk=False, column_type="String"),
                "Cardinality":                 Column(value="Many" if field_type != "pk" else None, column_name="Cardinality", is_pk=False, column_type="String"),
                "CRUDStatus":                  Column(value="c", column_name="CRUDStatus", is_pk=False, column_type="String"),
                "AutoFilter":                  Column(value=0, column_name="AutoFilter", is_pk=False, column_type="Integer"),
                "AutoFilterSequence":          Column(value=0, column_name="AutoFilterSequence", is_pk=False, column_type="Integer"),
                "NamedFilter":                 Column(value=0, column_name="NamedFilter", is_pk=False, column_type="Integer")
            })
        ModelTableColumnKey_sequence_no += 1
        if field_type == "pk":
            ModelTableKey_sequence_pk[Table_ModelTableKey] += 1

    tab = DDModel_To_Update.get_Table(table_name="DDModelTable")
    if tab.get_rows() != {}:
        for row in tab.filter_rows_by_condition(where_column_name="ModelType", condition_value="ENTITY"):
            columns = row.get_columns()
            table_ModelTableKey = columns["ModelTableKey"].get_value()
            table_ModelID = columns["ModelID"].get_value()
            for field in ["Description", "ExternalId", "Id", "Name"]:
                DDModel_To_Update.add_row_to_table(table_name=table_name, columns={
                        "FeatureKey":                  Column(value="@FeatureKey", column_name="FeatureKey", is_pk=True, column_type="Integer"),
                        "ModelTableKey":               Column(value=table_ModelTableKey, column_name="ModelTableKey", is_pk=True, column_type="Integer"),
                        "ModelTableColumnKey":         Column(value=f"@ModelTableColumnKey{ModelTableColumnKey_sequence_no}", column_name="ModelTableColumnKey", is_pk=True, column_type="Integer", is_identity=True),
                        "FieldName":                   Column(value=f"E_{table_ModelID}_{field}", column_name="FieldName", is_pk=False, column_type="String"),
                        "FieldType":                   Column(value="variable", column_name="FieldType", is_pk=False, column_type="String"),
                        "ReferenceModelID":            Column(value=field, column_name="ReferenceModelID", is_pk=False, column_type="String"),
                        "SequenceNo":                  Column(value=0, column_name="SequenceNo", is_pk=False, column_type="Integer"),
                        "UniqueColumnId":              Column(value=f"{table_ModelID}_{field}", column_name="UniqueColumnId", is_pk=False, column_type="String"),
                        "Cardinality":                 Column(value="Many", column_name="Cardinality", is_pk=False, column_type="String"),
                        "CRUDStatus":                  Column(value="c", column_name="CRUDStatus", is_pk=False, column_type="String"),
                        "AutoFilter":                  Column(value=0, column_name="AutoFilter", is_pk=False, column_type="Integer"),
                        "AutoFilterSequence":          Column(value=0, column_name="AutoFilterSequence", is_pk=False, column_type="Integer"),
                        "NamedFilter":                 Column(value=0, column_name="NamedFilter", is_pk=False, column_type="Integer")
                    })
                ModelTableColumnKey_sequence_no += 1

def create_new_entry(DDModel_source: ModelConfiguration, DDModel_To_Update: ModelConfiguration, table_name: str, DataTUse: Optional[ModelConfiguration] = None):
    DDTable_source = DDModel_source.get_Table(table_name=table_name)
    DDTable: Table

    if not DDModel_To_Update.table_exists(table_name=table_name):
        DDTable = Table(schema_name=DDTable_source.get_schema_name(), table_name=DDTable_source.get_table_name(), rows={})
    else:
        DDTable = DDModel_To_Update.get_Table(table_name=table_name)

    rows = DDTable_source.get_rows()
    if 1 not in rows:
        raise KeyError(f"Row with key 1 does not exist in {table_name}")

    if table_name == "DDFeature":
        add_ddfeature_row(DDTable, AliasName)
    elif table_name == "DDVariable" and DataTUse:
        add_ddVariables(DDModel_To_Update, DataTUse, table_name)
    elif table_name == "DDModelTable" and DataTUse:
        add_ddmodeltable(DDModel_To_Update, DataTUse, table_name)
    elif table_name == "DDModelTableColumn" and DataTUse:   
        add_DDModelTableColumn(DDModel_To_Update, DataTUse, table_name)

def generate_sql_Feature_creation(DD_Model_source: ModelConfiguration, DD_Model: ModelConfiguration, dd_data_stored: ModelConfiguration) -> str:
    create_new_entry(DDModel_source=DD_Model_source, DDModel_To_Update=DD_Model, table_name="DDFeature")
    create_new_entry(DDModel_source=DD_Model_source, DDModel_To_Update=DD_Model, table_name="DDVariable", DataTUse=dd_data_stored)
    create_new_entry(DDModel_source=DD_Model_source, DDModel_To_Update=DD_Model, table_name="DDModelTable", DataTUse=dd_data_stored)
    create_new_entry(DDModel_source=DD_Model_source, DDModel_To_Update=DD_Model, table_name="DDModelTableColumn", DataTUse=dd_data_stored)

    sql_statement_DDFeature = generate_insert_sql(DD_Model.get_Table_filtered(table_name="DDFeature", FilterColumn="FeatureKey", FilterValue=None, Operator="!="))
    sql_statement_DDVariables = generate_insert_sql(DD_Model.get_Table_filtered(table_name="DDVariable", FilterColumn="FeatureKey", FilterValue=None, Operator="!="))
    sql_statement_DDModelTable = generate_insert_sql(DD_Model.get_Table_filtered(table_name="DDModelTable", FilterColumn="FeatureKey", FilterValue=None, Operator="!="))
    sql_statement_DDModelTableColumn = generate_insert_sql(DD_Model.get_Table_filtered(table_name="DDModelTableColumn", FilterColumn="FeatureKey", FilterValue=None, Operator="!="))
    
    return sql_statement_DDFeature + "\n" + sql_statement_DDVariables + "\n" + sql_statement_DDModelTable + "\n" + sql_statement_DDModelTableColumn

table_def = [Table(schema_name="dbo", table_name="TableDefinition", rows={1: Row(row_number=1, columns={
                    "Table Name"        : Column(value="New Table 1", column_name="Table Name", is_pk=True, column_type="String"),
                    "Entity"            : Column(value="True", column_name="Entity", is_pk=False, column_type="Boolean"),
                    "Domain"            : Column(value="False", column_name="Domain", is_pk=False, column_type="Boolean"),
                    "View"              : Column(value="False", column_name="View", is_pk=False, column_type="Boolean"),
                    "Alias Specific"    : Column(value="False", column_name="Alias Specific", is_pk=False, column_type="Boolean")
                })

                , 2: Row(row_number=2, columns={
                    "Table Name"        : Column(value="New Table 2", column_name="Table Name", is_pk=True, column_type="String"),
                    "Entity"            : Column(value="True", column_name="Entity", is_pk=False, column_type="Boolean"),
                    "Domain"            : Column(value="False", column_name="Domain", is_pk=False, column_type="Boolean"),
                    "View"              : Column(value="False", column_name="View", is_pk=False, column_type="Boolean"),
                    "Alias Specific"    : Column(value="False", column_name="Alias Specific", is_pk=False, column_type="Boolean")
                })
                })]
table_Var = [Table(schema_name="dbo", table_name="VariableDefinition", rows={
                # Keys
                  1: Row(row_number=1, columns={
                    "Table Name"        : Column(value="New Table 1", column_name="Table Name", is_pk=True, column_type="String"),
                    "Variabile"         : Column(value="Key_1", column_name="Variabile", is_pk=True, column_type="String"),
                    "IsVariable"        : Column(value="False", column_name="IsVariable", is_pk=False, column_type="Boolean"),

                    "PK"                : Column(value="True", column_name="PK", is_pk=False, column_type="Boolean"),
                    "Domain"            : Column(value="", column_name="Domain", is_pk=False, column_type="String"),

                    "Type"              : Column(value=None, column_name="Type", is_pk=False, column_type="String"),
                    "Precision"         : Column(value=None, column_name="Precision", is_pk=False, column_type="Integer"),
                    "Scale"             : Column(value=None, column_name="Scale", is_pk=False, column_type="Integer"),
                    "Length"            : Column(value=None, column_name="Length", is_pk=False, column_type="Integer")
                })


                , 2: Row(row_number=2, columns={
                    "Table Name"        : Column(value="New Table 2", column_name="Table Name", is_pk=True, column_type="String"),
                    "Variabile"         : Column(value="Key_2", column_name="Variabile", is_pk=True, column_type="String"),
                    "IsVariable"        : Column(value="False", column_name="IsVariable", is_pk=False, column_type="Boolean"),

                    "PK"                : Column(value="True", column_name="PK", is_pk=False, column_type="Boolean"),
                    "Domain"            : Column(value="", column_name="Domain", is_pk=False, column_type="String"),

                    "Type"              : Column(value=None, column_name="Type", is_pk=False, column_type="String"),
                    "Precision"         : Column(value=None, column_name="Precision", is_pk=False, column_type="Integer"),
                    "Scale"             : Column(value=None, column_name="Scale", is_pk=False, column_type="Integer"),
                    "Length"            : Column(value=None, column_name="Length", is_pk=False, column_type="Integer")
                })
                , 3: Row(row_number=3, columns={
                    "Table Name"        : Column(value="New Table 2", column_name="Table Name", is_pk=True, column_type="String"),
                    "Variabile"         : Column(value="Key_1", column_name="Variabile", is_pk=True, column_type="String"),
                    "IsVariable"        : Column(value="False", column_name="IsVariable", is_pk=False, column_type="Boolean"),

                    "PK"                : Column(value="False", column_name="PK", is_pk=False, column_type="Boolean"),
                    "Domain"            : Column(value="", column_name="Domain", is_pk=False, column_type="String"),

                    "Type"              : Column(value=None, column_name="Type", is_pk=False, column_type="String"),
                    "Precision"         : Column(value=None, column_name="Precision", is_pk=False, column_type="Integer"),
                    "Scale"             : Column(value=None, column_name="Scale", is_pk=False, column_type="Integer"),
                    "Length"            : Column(value=None, column_name="Length", is_pk=False, column_type="Integer")
                })

                # Vaiables
                , 4: Row(row_number=4, columns={
                    "Table Name"        : Column(value="New Table 1", column_name="Table Name", is_pk=True, column_type="String"),
                    "Variabile"         : Column(value="Vaiable 1", column_name="Variabile", is_pk=True, column_type="String"),
                    "IsVariable"        : Column(value="True", column_name="IsVariable", is_pk=False, column_type="Boolean"),

                    "Type"              : Column(value="INTEGER", column_name="Type", is_pk=False, column_type="String"),
                    "Precision"         : Column(value="0", column_name="Precision", is_pk=False, column_type="Integer"),
                    "Scale"             : Column(value="0", column_name="Scale", is_pk=False, column_type="Integer"),
                    "Length"            : Column(value="0", column_name="Length", is_pk=False, column_type="Integer"),

                    "PK"                : Column(value=None, column_name="PK", is_pk=False, column_type="Boolean"),
                    "Domain"            : Column(value=None, column_name="Domain", is_pk=False, column_type="String")
                })
                , 5: Row(row_number=5, columns={
                    "Table Name"        : Column(value="New Table 1", column_name="Table Name", is_pk=True, column_type="String"),
                    "Variabile"         : Column(value="Vaiable 2", column_name="Variabile", is_pk=True, column_type="String"),
                    "IsVariable"        : Column(value="True", column_name="IsVariable", is_pk=False, column_type="Boolean"),

                    "Type"              : Column(value="NVARCHAR", column_name="Type", is_pk=False, column_type="String"),
                    "Precision"         : Column(value="0", column_name="Precision", is_pk=False, column_type="Integer"),
                    "Scale"             : Column(value="0", column_name="Scale", is_pk=False, column_type="Integer"),
                    "Length"            : Column(value="40", column_name="Length", is_pk=False, column_type="Integer"),

                    "PK"                : Column(value=None, column_name="PK", is_pk=False, column_type="Boolean"),
                    "Domain"            : Column(value=None, column_name="Domain", is_pk=False, column_type="String")
                })
                , 6: Row(row_number=6, columns={
                    "Table Name"        : Column(value="New Table 1", column_name="Table Name", is_pk=True, column_type="String"),
                    "Variabile"         : Column(value="Vaiable 3", column_name="Variabile", is_pk=True, column_type="String"),
                    "IsVariable"        : Column(value="True", column_name="IsVariable", is_pk=False, column_type="Boolean"),

                    "Type"              : Column(value="DECIMAL", column_name="Type", is_pk=False, column_type="String"),
                    "Precision"         : Column(value="8", column_name="Precision", is_pk=False, column_type="Integer"),
                    "Scale"             : Column(value="2", column_name="Scale", is_pk=False, column_type="Integer"),
                    "Length"            : Column(value="0", column_name="Length", is_pk=False, column_type="Integer"),

                    "PK"                : Column(value=None, column_name="PK", is_pk=False, column_type="Boolean"),
                    "Domain"            : Column(value=None, column_name="Domain", is_pk=False, column_type="String")
                })

                
                , 7: Row(row_number=7, columns={
                    "Table Name"        : Column(value="New Table 2", column_name="Table Name", is_pk=True, column_type="String"),
                    "Variabile"         : Column(value="Vaiable 5", column_name="Variabile", is_pk=True, column_type="String"),
                    "IsVariable"        : Column(value="True", column_name="IsVariable", is_pk=False, column_type="Boolean"),

                    "Type"              : Column(value="NVARCHAR", column_name="Type", is_pk=False, column_type="String"),
                    "Precision"         : Column(value="0", column_name="Precision", is_pk=False, column_type="Integer"),
                    "Scale"             : Column(value="0", column_name="Scale", is_pk=False, column_type="Integer"),
                    "Length"            : Column(value="512", column_name="Length", is_pk=False, column_type="Integer"),

                    "PK"                : Column(value=None, column_name="PK", is_pk=False, column_type="Boolean"),
                    "Domain"            : Column(value=None, column_name="Domain", is_pk=False, column_type="String")
                })
                , 8: Row(row_number=8, columns={
                    "Table Name"        : Column(value="New Table 2", column_name="Table Name", is_pk=True, column_type="String"),
                    "Variabile"         : Column(value="Vaiable 6", column_name="Variabile", is_pk=True, column_type="String"),
                    "IsVariable"        : Column(value="True", column_name="IsVariable", is_pk=False, column_type="Boolean"),

                    "Type"              : Column(value="NVARCHAR", column_name="Type", is_pk=False, column_type="String"),
                    "Precision"         : Column(value="0", column_name="Precision", is_pk=False, column_type="Integer"),
                    "Scale"             : Column(value="0", column_name="Scale", is_pk=False, column_type="Integer"),
                    "Length"            : Column(value="256", column_name="Length", is_pk=False, column_type="Integer"),

                    "PK"                : Column(value=None, column_name="PK", is_pk=False, column_type="Boolean"),
                    "Domain"            : Column(value=None, column_name="Domain", is_pk=False, column_type="String")
                })
                , 9: Row(row_number=9, columns={
                    "Table Name"        : Column(value="New Table 2", column_name="Table Name", is_pk=True, column_type="String"),
                    "Variabile"         : Column(value="Vaiable 7", column_name="Variabile", is_pk=True, column_type="String"),
                    "IsVariable"        : Column(value="True", column_name="IsVariable", is_pk=False, column_type="Boolean"),

                    "Type"              : Column(value="NVARCHAR", column_name="Type", is_pk=False, column_type="String"),
                    "Precision"         : Column(value="0", column_name="Precision", is_pk=False, column_type="Integer"),
                    "Scale"             : Column(value="0", column_name="Scale", is_pk=False, column_type="Integer"),
                    "Length"            : Column(value="40", column_name="Length", is_pk=False, column_type="Integer"),

                    "PK"                : Column(value=None, column_name="PK", is_pk=False, column_type="Boolean"),
                    "Domain"            : Column(value=None, column_name="Domain", is_pk=False, column_type="String")
                })
                })]

tables = table_def + table_Var
dd_data_stored = ModelConfiguration(Name="Test Config", Tables=tables)
DD_Model_base = get_DD_ModelConfiguration_Structure(DD_MODEL_FILE)

AliasName = "ARoffi"

DD_Tables: List[Table] = []
for table in DD_Model_base.get_Tables():
    new_table = Table(schema_name=table.get_schema_name(), table_name=table.get_table_name(), rows={})
    DD_Tables.append(new_table)

DD_Model = ModelConfiguration(Name="Config to Generate", Tables=DD_Tables)

file_path = "G:\\Git Repository\\InMemory-Feature-Creator\\test generation.sql"

sql_content = generate_sql_Feature_creation(DD_Model_base, DD_Model, dd_data_stored)

if file_path:
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(sql_content)
    print(f"SQL file saved: {file_path}")

