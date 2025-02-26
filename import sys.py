import sys
import collections, re, typing, enum
import os
import Utils
import pandas as pd
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QMenuBar, QMenu,
                             QFileDialog, QTableWidget, QTableWidgetItem, QTabWidget, QCheckBox, QComboBox, 
                             QHBoxLayout, QPushButton, QHeaderView, QSpinBox, QDialog, QLabel, QLineEdit)
from PyQt6.QtGui import QAction, QFont, QPalette, QColor
from PyQt6.QtCore import Qt

import Utils.TableModel

class LoadXMLDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Load XML Configuration")
        self.setGeometry(200, 200, 500, 200)
        
        layout = QVBoxLayout()
        
        config_layout = QHBoxLayout()
        self.config_label = QLabel("Select Configuration:")
        self.config_dropdown = QComboBox()
        self.refresh_configurations()
        config_layout.addWidget(self.config_label)
        config_layout.addWidget(self.config_dropdown)
        
        file_info_layout = QHBoxLayout()
        self.file_label = QLabel("Select XML File:")
        self.file_name_display = QLabel("No file selected")
        file_info_layout.addWidget(self.file_label)
        file_info_layout.addWidget(self.file_name_display)
        
        file_layout = QHBoxLayout()
        self.file_path_display = QLineEdit()
        self.file_path_display.setReadOnly(True)
        self.file_button = QPushButton("Browse...")
        self.file_button.setFixedWidth(100)
        self.file_button.clicked.connect(self.load_xml_file)
        file_layout.addWidget(self.file_path_display)
        file_layout.addWidget(self.file_button)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.ok_button = QPushButton("OK")
        self.ok_button.setFixedWidth(80)
        self.ok_button.clicked.connect(self.handle_ok)
        self.ok_button.setDisabled(True)
        button_layout.addWidget(self.ok_button)
        
        layout.addLayout(config_layout)
        layout.addLayout(file_info_layout)
        layout.addLayout(file_layout)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def handle_ok(self):
        selected_config_name = self.config_dropdown.currentText()
        selected_config_path = self.config_paths.get(selected_config_name, "")
        selected_file = self.file_path_display.text()
        print(f"Selected Configuration Path: {selected_config_path}, Selected File: {selected_file}")
        CSV_XML_Editor.dm_inmemory_data = Utils.load_xml_to_config(selected_file, selected_config_path)
        self.accept()

    def refresh_configurations(self):
        """Refresh the dropdown list with configurations from the 'XML' folder."""
        self.config_dropdown.clear()
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "XML")
        if os.path.exists(config_path):
            configs = [f for f in os.listdir(config_path) if f.endswith(".xml")]
            self.config_dropdown.addItems(configs)
            self.config_paths = {config: os.path.join(config_path, config) for config in configs}
        else:
            self.config_dropdown.addItem("No configurations found")
            self.config_paths = {}
    
    def load_xml_file(self):
        """Opens file dialog to select an XML file and displays the full path and file name."""
        options = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Open XML File", "", "XML Files (*.xml)", options=options)
        if file_path:
            self.file_path_display.setText(file_path)
            self.file_name_display.setText(os.path.basename(file_path))
            self.ok_button.setDisabled(True) if not self.config_dropdown.currentText() else self.ok_button.setDisabled(False)

class Table3Dialog(QDialog):

    T3CN = Utils.Table3ColumnName
    T3CO = Utils.Table3ColumnOrder

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Variables")
        self.setGeometry(600, 300, 1200, 500)
        T3CN = Utils.Table3ColumnName
        
        layout = QVBoxLayout()
        
        self.table3 = QTableWidget()
        self.table3.setColumnCount(8)
        self.table3.setRowCount(1)
        self.table3.setHorizontalHeaderLabels([T3CN.COLUMN_VARIABLE_NAME.value
                                                , T3CN.COLUMN_IS_PK.value
                                                , T3CN.COLUMN_IS_DOMAIN.value
                                                , T3CN.COLUMN_IS_VARIABLE.value
                                                , T3CN.COLUMN_VARIABLE_TYPE.value
                                                , T3CN.COLUMN_VARIABLE_PRECISION.value
                                                , T3CN.COLUMN_VARIABLE_SCALE.value
                                                , T3CN.COLUMN_VARIABLE_LENGHT.value])
        self.initialize_table3()
        self.table3.cellChanged.connect(self.on_table3_cell_changed)
        CSV_XML_Editor.style_table(self, self.table3)
        
        layout.addWidget(self.table3)
        self.setLayout(layout)

        # Row count selector
        self.row_count_spinner = QSpinBox()
        self.row_count_spinner.setMinimum(1)
        self.row_count_spinner.setMaximum(100)
        self.row_count_spinner.setValue(1)
        layout.addWidget(self.row_count_spinner, alignment=Qt.AlignmentFlag.AlignCenter)

        # Button to add new rows
        self.add_row_btn = QPushButton("Add Rows")
        self.add_row_btn.setFixedSize(220, 45)
        self.add_row_btn.setStyleSheet(self.get_button_style())
        self.add_row_btn.setFont(QFont("Arial", 11, QFont.Weight.Medium))
        self.add_row_btn.clicked.connect(self.add_rows)
        layout.addWidget(self.add_row_btn, alignment=Qt.AlignmentFlag.AlignCenter)



    def initialize_table3(self):
        """Initializes checkboxes and dropdowns in table3."""
        print("Populating Table 3...")  # Debug log
        VT = Utils.VariableType

        TableID: str = CSV_XML_Editor.dm_inmemory_data.get_column_values_filtered(table_name=Utils.IMConfigurationTable.MODELTABLE.value, column_name=Utils.IMConfigurationModelTable.MODELID.value, FilterColumn = Utils.IMConfigurationModelTable.PHYSICALNAME.value, FilterValue = CSV_XML_Editor.TableValue)
        
        VariableList: List[str] = []

        if len(TableID) > 0:
            VariableList = CSV_XML_Editor.dm_inmemory_data.get_column_values_filtered(table_name=Utils.IMConfigurationTable.MODELTABLECOLUMN.value, column_name=Utils.IMConfigurationModelTableColumn.FIELDNAME.value, FilterColumn = Utils.IMConfigurationModelTableColumn.MODELID.value, FilterValue = TableID[0])

        if len(VariableList) > 0:
            for i in range(len(VariableList)):
                if i > 0:
                    self.table3.insertRow(self.table3.rowCount())
                self.table3.setItem(i, self.T3CO.COLUMN_VARIABLE_NAME.value - 1, QTableWidgetItem(VariableList[i]))
                self.table3.setCellWidget(i, self.T3CO.COLUMN_IS_PK.value - 1, CSV_XML_Editor.create_checkbox(self))
                self.table3.setCellWidget(i, self.T3CO.COLUMN_IS_DOMAIN.value - 1, CSV_XML_Editor.create_checkbox(self))
                self.table3.setCellWidget(i, self.T3CO.COLUMN_IS_VARIABLE.value - 1, CSV_XML_Editor.create_checkbox(self))
                self.table3.setCellWidget(i, self.T3CO.COLUMN_VARIABLE_TYPE.value - 1, CSV_XML_Editor.create_dropdown(self, [VT.INTEGER.value, VT.DECIMAL.value, VT.NVARCHAR.value, VT.DATE.value, VT.DATETIME.value]))
                CSV_XML_Editor.dm_User_Input.get_Table(Utils.TabName.TAB3.value).add_row(columns={
                    self.T3CN.COLUMN_TABLE_NAME.value           : Utils.Column(value=VariableList[i]   , name=self.T3CN.COLUMN_TABLE_NAME.value         , is_pk=True    , column_type="String"),
                    self.T3CN.COLUMN_VARIABLE_NAME.value        : Utils.Column(value=""                , name=self.T3CN.COLUMN_VARIABLE_NAME.value      , is_pk=True    , column_type="String"),
                    self.T3CN.COLUMN_IS_PK.value                : Utils.Column(value="False"           , name=self.T3CN.COLUMN_IS_PK.value              , is_pk=False   , column_type="Boolean"),
                    self.T3CN.COLUMN_IS_DOMAIN.value            : Utils.Column(value="False"           , name=self.T3CN.COLUMN_IS_DOMAIN.value          , is_pk=False   , column_type="Boolean"),
                    self.T3CN.COLUMN_IS_VARIABLE.value          : Utils.Column(value="False"           , name=self.T3CN.COLUMN_IS_VARIABLE.value        , is_pk=False   , column_type="Boolean"),
                    self.T3CN.COLUMN_VARIABLE_TYPE.value        : Utils.Column(value=None              , name=self.T3CN.COLUMN_VARIABLE_TYPE.value      , is_pk=False   , column_type="Integer"),
                    self.T3CN.COLUMN_VARIABLE_PRECISION.value   : Utils.Column(value=None              , name=self.T3CN.COLUMN_VARIABLE_PRECISION.value , is_pk=False   , column_type="Integer"),
                    self.T3CN.COLUMN_VARIABLE_SCALE.value       : Utils.Column(value=None              , name=self.T3CN.COLUMN_VARIABLE_SCALE.value     , is_pk=False   , column_type="Integer"),
                    self.T3CN.COLUMN_VARIABLE_LENGHT.value      : Utils.Column(value=None              , name=self.T3CN.COLUMN_VARIABLE_LENGHT.value    , is_pk=False   , column_type="Integer"),
                })
        else:
            CSV_XML_Editor.dm_User_Input.get_Table(Utils.TabName.TAB3.value).add_row(columns={
                self.T3CN.COLUMN_TABLE_NAME.value           : Utils.Column(value=""                , name=self.T3CN.COLUMN_TABLE_NAME.value         , is_pk=True    , column_type="String"),
                self.T3CN.COLUMN_VARIABLE_NAME.value        : Utils.Column(value=""                , name=self.T3CN.COLUMN_VARIABLE_NAME.value      , is_pk=True    , column_type="String"),
                self.T3CN.COLUMN_IS_PK.value                : Utils.Column(value="False"           , name=self.T3CN.COLUMN_IS_PK.value              , is_pk=False   , column_type="Boolean"),
                self.T3CN.COLUMN_IS_DOMAIN.value            : Utils.Column(value="False"           , name=self.T3CN.COLUMN_IS_DOMAIN.value          , is_pk=False   , column_type="Boolean"),
                self.T3CN.COLUMN_IS_VARIABLE.value          : Utils.Column(value="False"           , name=self.T3CN.COLUMN_IS_VARIABLE.value        , is_pk=False   , column_type="Boolean"),
                self.T3CN.COLUMN_VARIABLE_TYPE.value        : Utils.Column(value=None              , name=self.T3CN.COLUMN_VARIABLE_TYPE.value      , is_pk=False   , column_type="Integer"),
                self.T3CN.COLUMN_VARIABLE_PRECISION.value   : Utils.Column(value=None              , name=self.T3CN.COLUMN_VARIABLE_PRECISION.value , is_pk=False   , column_type="Integer"),
                self.T3CN.COLUMN_VARIABLE_SCALE.value       : Utils.Column(value=None              , name=self.T3CN.COLUMN_VARIABLE_SCALE.value     , is_pk=False   , column_type="Integer"),
                self.T3CN.COLUMN_VARIABLE_LENGHT.value      : Utils.Column(value=None              , name=self.T3CN.COLUMN_VARIABLE_LENGHT.value    , is_pk=False   , column_type="Integer"),
            })
            self.table3.setCellWidget(0, Utils.Table3ColumnOrder.COLUMN_IS_PK.value - 1, CSV_XML_Editor.create_checkbox(self))
            self.table3.setCellWidget(0, Utils.Table3ColumnOrder.COLUMN_IS_DOMAIN.value - 1, CSV_XML_Editor.create_checkbox(self))
            self.table3.setCellWidget(0, Utils.Table3ColumnOrder.COLUMN_IS_VARIABLE.value - 1, CSV_XML_Editor.create_checkbox(self))
            self.table3.setCellWidget(0, Utils.Table3ColumnOrder.COLUMN_VARIABLE_TYPE.value - 1, CSV_XML_Editor.create_dropdown(self, [VT.INTEGER.value, VT.DECIMAL.value, VT.NVARCHAR.value, VT.DATE.value, VT.DATETIME.value]))

    def add_rows(self):
        """Adds a specified number of rows to both tables."""
        print("Adding new rows...")  # Debug log
        row_count = self.row_count_spinner.value()
        VT = Utils.VariableType
        for _ in range(row_count):
            self.table3.insertRow(self.table3.rowCount())
            row = self.table3.rowCount() - 1
            CSV_XML_Editor.dm_User_Input.get_Table(Utils.TabName.TAB3.value).add_row(columns={
                self.T3CN.COLUMN_TABLE_NAME.value           : Utils.Column(value=""                , name=self.T3CN.COLUMN_TABLE_NAME.value         , is_pk=True    , column_type="String"),
                self.T3CN.COLUMN_VARIABLE_NAME.value        : Utils.Column(value=""                , name=self.T3CN.COLUMN_VARIABLE_NAME.value      , is_pk=True    , column_type="String"),
                self.T3CN.COLUMN_IS_PK.value                : Utils.Column(value="False"           , name=self.T3CN.COLUMN_IS_PK.value              , is_pk=False   , column_type="Boolean"),
                self.T3CN.COLUMN_IS_DOMAIN.value            : Utils.Column(value="False"           , name=self.T3CN.COLUMN_IS_DOMAIN.value          , is_pk=False   , column_type="Boolean"),
                self.T3CN.COLUMN_IS_VARIABLE.value          : Utils.Column(value="False"           , name=self.T3CN.COLUMN_IS_VARIABLE.value        , is_pk=False   , column_type="Boolean"),
                self.T3CN.COLUMN_VARIABLE_TYPE.value        : Utils.Column(value=None              , name=self.T3CN.COLUMN_VARIABLE_TYPE.value      , is_pk=False   , column_type="Integer"),
                self.T3CN.COLUMN_VARIABLE_PRECISION.value   : Utils.Column(value=None              , name=self.T3CN.COLUMN_VARIABLE_PRECISION.value , is_pk=False   , column_type="Integer"),
                self.T3CN.COLUMN_VARIABLE_SCALE.value       : Utils.Column(value=None              , name=self.T3CN.COLUMN_VARIABLE_SCALE.value     , is_pk=False   , column_type="Integer"),
                self.T3CN.COLUMN_VARIABLE_LENGHT.value      : Utils.Column(value=None              , name=self.T3CN.COLUMN_VARIABLE_LENGHT.value    , is_pk=False   , column_type="Integer"),
            })
            self.table3.setCellWidget(row, Utils.Table3ColumnOrder.COLUMN_IS_PK.value - 1, CSV_XML_Editor.create_checkbox(self))
            self.table3.setCellWidget(row, Utils.Table3ColumnOrder.COLUMN_IS_DOMAIN.value - 1, CSV_XML_Editor.create_checkbox(self))
            self.table3.setCellWidget(row, Utils.Table3ColumnOrder.COLUMN_IS_VARIABLE.value - 1, CSV_XML_Editor.create_checkbox(self))
            self.table3.setCellWidget(row, Utils.Table3ColumnOrder.COLUMN_VARIABLE_TYPE.value - 1, CSV_XML_Editor.create_dropdown(self, [VT.INTEGER.value, VT.DECIMAL.value, VT.NVARCHAR.value, VT.DATE.value, VT.DATETIME.value]))

    def on_table3_cell_changed(self, row : int, column):
        """Slot to handle cell changes in table3."""
        print(f"Cell changed at row {row}, column {column}")  # Debug log

        column_label = self.table3.horizontalHeaderItem(column).text()
        CSV_XML_Editor.dm_User_Input.set_column_value_by_row_number(Utils.TabName.TAB3.value, row, column_label, self.table3.item(row, column).text())
    
    def get_button_style(self):
        """Returns the appropriate button style based on system theme."""
        if CSV_XML_Editor.check_dark_mode(self):
            return "background-color: #1E1E1E; color: white; font-size: 14px; border-radius: 5px; padding: 8px;"
        else:
            return "background-color: #34495E; color: white; font-size: 14px; border-radius: 5px; padding: 8px;"
        
    def check_dark_mode(self):
        """Checks if the system is in dark mode."""
        palette = QApplication.instance().palette()
        return palette.color(QPalette.ColorRole.Window).lightness() < 128

class CSV_XML_Editor(QMainWindow):

    T1CN = Utils.Table1ColumnName
    T1CO = Utils.Table1ColumnOrder
    T2CN = Utils.Table2ColumnName
    T2CO = Utils.Table2ColumnOrder

    TableValue: str = ""

    dm_User_Input = Utils.ModelConfiguration("User", [])  # Stores data from user input
    dm_inmemory_data: Utils.ModelConfiguration = None  # Stores data from user-loaded XML
    dd_inmemory_data = Utils.get_DD_ModelConfiguration_Structure("E:/Python Projects/InMemory-Feature-Creator/TestFiles/DD Model only necessary.xml") # Stores data from DD XML

    def __init__(self):
        super().__init__()
        print("Initializing CSV_XML_Editor...")  # Debug log
        self.xml_structure = {}  # Stores the structure of InMemory XML
        self.updating_dropdown = False  # Flag to prevent infinite loop
        self.initUI()
    
    def initUI(self):
        """Initializes the main UI components of the application."""
        print("Setting up UI...")  # Debug log
        self.setWindowTitle("InMemory Auto Generate Feature")
        self.setGeometry(100, 100, 900, 700)
        self.create_menu()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        
        self.is_dark_mode = self.check_dark_mode()
        print(f"Dark mode detected: {self.is_dark_mode}")  # Debug log
        
        # Button to generate features
        self.generate_feature_btn = QPushButton("Generate Feature")
        self.generate_feature_btn.setFixedSize(220, 45)
        self.generate_feature_btn.setStyleSheet(self.get_button_style())
        self.generate_feature_btn.setFont(QFont("Arial", 11, QFont.Weight.Medium))
        self.generate_feature_btn.clicked.connect(self.generate_feature)
        layout.addWidget(self.generate_feature_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.tabs = QTabWidget()
        
        # Table 1 setup
        print("Initializing Table 1...")  # Debug log
        self.dm_User_Input.add_table(Utils.Table(schema_name="User", table_name="Tabelle", rows={}))
        self.table1 = QTableWidget()
        self.style_table(self.table1)
        self.table1.setColumnCount(5)
        self.table1.setRowCount(1)
        self.table1.setHorizontalHeaderLabels([self.T1CN.COLUMN_TABLE_NAME.value, self.T1CN.COLUMN_IS_ENTITY.value, self.T1CN.COLUMN_IS_DOMAIN.value, self.T1CN.COLUMN_IS_VIEW.value, self.T1CN.COLUMN_IS_ALIAS_SPECIFIC.value])
        self.initialize_table1()
        self.table1.cellChanged.connect(self.on_table1_cell_changed)
        self.table1.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table1.customContextMenuRequested.connect(self.show_table1_context_menu)
        self.tabs.addTab(self.table1, "Tabelle")
        
        # Table 2 setup
        print("Initializing Table 2...")  # Debug log
        self.dm_User_Input.add_table(Utils.Table(schema_name="User", table_name="Calculation Plan", rows={}))
        self.table2 = QTableWidget()
        self.style_table(self.table2)
        self.table2.setColumnCount(5)
        self.table2.setRowCount(1)
        self.table2.setHorizontalHeaderLabels([self.T2CN.COLUMN_VARIABLE_NAME.value, self.T2CN.COLUMN_PK.value, self.T2CN.COLUMN_TABLE_NAME.value, self.T2CN.COLUMN_ALLOCATION.value, self.T2CN.COLUMN_DOMAIN.value])
        self.initialize_table2()
        self.table2.cellChanged.connect(self.on_table2_cell_changed)
        self.tabs.addTab(self.table2, "Calculation Plan")
        
        layout.addWidget(self.tabs)

        # Table 3 setup
        self.dm_User_Input.add_table(Utils.Table(schema_name="User", table_name="Variabili", rows={}))
        
        # Row count selector
        self.row_count_spinner = QSpinBox()
        self.row_count_spinner.setMinimum(1)
        self.row_count_spinner.setMaximum(100)
        self.row_count_spinner.setValue(1)
        layout.addWidget(self.row_count_spinner, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Button to add new rows
        self.add_row_btn = QPushButton("Add Rows")
        self.add_row_btn.setFixedSize(220, 45)
        self.add_row_btn.setStyleSheet(self.get_button_style())
        self.add_row_btn.setFont(QFont("Arial", 11, QFont.Weight.Medium))
        self.add_row_btn.clicked.connect(self.add_rows)
        layout.addWidget(self.add_row_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.central_widget.setLayout(layout)

    def initialize_table1(self):
        """Initializes checkboxes for specific columns in table1."""
        print("Populating Table 1...")  # Debug log
        self.dm_User_Input.get_Table(Utils.TabName.TAB1.value).add_row(columns={
            self.T1CN.COLUMN_TABLE_NAME.value        : Utils.Column(value=""                , name=self.T1CN.COLUMN_TABLE_NAME.value         , is_pk=True    , column_type="String"),
            self.T1CN.COLUMN_IS_ENTITY.value         : Utils.Column(value="False"           , name=self.T1CN.COLUMN_IS_ENTITY.value          , is_pk=False   , column_type="Boolean"),
            self.T1CN.COLUMN_IS_DOMAIN.value         : Utils.Column(value="False"           , name=self.T1CN.COLUMN_IS_DOMAIN.value          , is_pk=False   , column_type="Boolean"),
            self.T1CN.COLUMN_IS_VIEW.value           : Utils.Column(value="False"           , name=self.T1CN.COLUMN_IS_VIEW.value            , is_pk=False   , column_type="Boolean"),
            self.T1CN.COLUMN_IS_ALIAS_SPECIFIC.value : Utils.Column(value="False"           , name=self.T1CN.COLUMN_IS_ALIAS_SPECIFIC.value  , is_pk=False   , column_type="Boolean")
        })
        self.table1.setCellWidget(0, Utils.Table1ColumnOrder.COLUMN_IS_ENTITY.value - 1, self.create_checkbox())
        self.table1.setCellWidget(0, Utils.Table1ColumnOrder.COLUMN_IS_DOMAIN.value - 1, self.create_checkbox())
        self.table1.setCellWidget(0, Utils.Table1ColumnOrder.COLUMN_IS_VIEW.value - 1, self.create_checkbox())
        self.table1.setCellWidget(0, Utils.Table1ColumnOrder.COLUMN_IS_ALIAS_SPECIFIC.value - 1, self.create_checkbox())
                
    
    def initialize_table2(self):
        """Initializes checkboxes and dropdowns in table2."""
        print("Populating Table 2...")  # Debug log
        self.dm_User_Input.get_Table(Utils.TabName.TAB2.value).add_row(columns={
            self.T2CN.COLUMN_VARIABLE_NAME.value        : Utils.Column(value=""         , name=self.T2CN.COLUMN_VARIABLE_NAME.value   , is_pk=True    , column_type="String"),
            self.T2CN.COLUMN_PK.value                   : Utils.Column(value="False"    , name=self.T2CN.COLUMN_PK.value              , is_pk=False   , column_type="Boolean"),
            self.T2CN.COLUMN_TABLE_NAME.value           : Utils.Column(value=""         , name=self.T2CN.COLUMN_TABLE_NAME.value      , is_pk=False   , column_type="String"),
            self.T2CN.COLUMN_ALLOCATION.value           : Utils.Column(value=""         , name=self.T2CN.COLUMN_ALLOCATION.value      , is_pk=False   , column_type="String"),
            self.T2CN.COLUMN_DOMAIN.value               : Utils.Column(value=""         , name=self.T2CN.COLUMN_DOMAIN.value          , is_pk=False   , column_type="String")
        })
        self.table2.setCellWidget(0, Utils.Table2ColumnOrder.COLUMN_PK.value - 1, self.create_checkbox())
        self.table2.setCellWidget(0, Utils.Table2ColumnOrder.COLUMN_ALLOCATION.value - 1, self.create_dropdown(["Replicate", "Proportional"]))
        self.table2.setCellWidget(0, Utils.Table2ColumnOrder.COLUMN_DOMAIN.value - 1, self.create_dropdown([""]))

    def on_table1_cell_changed(self, row : int, column):
        """Slot to handle cell changes in table2."""
        print(f"Cell changed at row {row}, column {column}")  # Debug log

        column_label = self.table1.horizontalHeaderItem(column).text()
        self.dm_User_Input.set_column_value_by_row_number(Utils.TabName.TAB1.value, row, column_label, self.table1.item(row, column).text())
        #if column_label == Utils.Table2ColumnName.COLUMN_TABLE_NAME.value:
        #    item = self.table2.item(row, column)
        #    filter_value = item.text()
        #    #print(f"Filter value: {filter_value}")  # Debug log
        #    self.refresh_dropdowns(EntityID=Utils.IMConfigurationTableDomain.ENTITYID.value, FilterValue=filter_value)

    def on_table2_cell_changed(self, row, column):
        """Slot to handle cell changes in table2."""
        print(f"Cell changed at row {row}, column {column}")  # Debug log

        column_label = self.table2.horizontalHeaderItem(column).text()
        self.dm_User_Input.set_column_value_by_row_number(Utils.TabName.TAB2.value, row, column_label, self.table2.item(row, column).text())
        if column_label == Utils.Table2ColumnName.COLUMN_TABLE_NAME.value:
            item = self.table2.item(row, column)
            filter_value = item.text()
            self.refresh_dropdowns(EntityID=Utils.IMConfigurationDomain.ENTITYID.value, FilterValue=filter_value)

    def style_table(self, table):
        """Applies styling to tables based on system theme."""
        table.setSortingEnabled(True)
        table.setAlternatingRowColors(True)
        if self.check_dark_mode():
            table.setStyleSheet("background-color: #1E1E1E; color: white; border: 1px solid #555;")
            table.horizontalHeader().setStyleSheet("background-color: #333; color: white; font-size: 13px;")
        else:
            table.setStyleSheet("background-color: #ECF0F1; border: 1px solid #BDC3C7;")
            table.horizontalHeader().setStyleSheet("background-color: #34495E; color: white; font-size: 13px;")
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)
    
    def create_menu(self):
        """Creates the application menu."""
        print("Creating menu...")  # Debug log
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        load_xml_action = QAction("Load System Configuration", self)
        load_xml_action.triggered.connect(self.show_load_xml_dialog)
        file_menu.addAction(load_xml_action)
    
    def show_load_xml_dialog(self):
        """Opens the Load XML dialog."""
        dialog = LoadXMLDialog(self)
        if dialog.exec():
            print("XML Configuration Loaded")
    
    def generate_feature(self):
        """Saves the SQL content to a file, prompting the user for a save location."""
        options = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getSaveFileName(self, "Save SQL File", "", "SQL Files (*.sql)", options=options)
        sql_content = Utils.generate_insert_sql(self.dm_inmemory_data.get_Table("DMDomain"))
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(sql_content)
            print(f"SQL file saved: {file_path}")
        """Placeholder for the feature generation logic."""
        print("Feature generation executed.")
    
    def add_rows(self):
        """Adds a specified number of rows to both tables."""
        print("Adding new rows...")  # Debug log
        row_count = self.row_count_spinner.value()
        current_tab_index = self.tabs.currentIndex()
        if current_tab_index == 0:  # Table 1 is active
            for _ in range(row_count):
                self.table1.insertRow(self.table1.rowCount())
                row = self.table1.rowCount() - 1

                self.dm_User_Input.get_Table(Utils.TabName.TAB1.value).add_row(columns={
                    self.T1CN.COLUMN_TABLE_NAME.value        : Utils.Column(value=""                , name=self.T1CN.COLUMN_TABLE_NAME.value         , is_pk=True    , column_type="String"),
                    self.T1CN.COLUMN_IS_ENTITY.value         : Utils.Column(value="False"           , name=self.T1CN.COLUMN_IS_ENTITY.value          , is_pk=False   , column_type="Boolean"),
                    self.T1CN.COLUMN_IS_DOMAIN.value         : Utils.Column(value="False"           , name=self.T1CN.COLUMN_IS_DOMAIN.value          , is_pk=False   , column_type="Boolean"),
                    self.T1CN.COLUMN_IS_VIEW.value           : Utils.Column(value="False"           , name=self.T1CN.COLUMN_IS_VIEW.value            , is_pk=False   , column_type="Boolean"),
                    self.T1CN.COLUMN_IS_ALIAS_SPECIFIC.value : Utils.Column(value="False"           , name=self.T1CN.COLUMN_IS_ALIAS_SPECIFIC.value  , is_pk=False   , column_type="Boolean")
                })

                self.table1.setCellWidget(row, Utils.Table1ColumnOrder.COLUMN_IS_ENTITY.value - 1, self.create_checkbox())
                self.table1.setCellWidget(row, Utils.Table1ColumnOrder.COLUMN_IS_DOMAIN.value - 1, self.create_checkbox())
                self.table1.setCellWidget(row, Utils.Table1ColumnOrder.COLUMN_IS_VIEW.value - 1, self.create_checkbox())
                self.table1.setCellWidget(row, Utils.Table1ColumnOrder.COLUMN_IS_ALIAS_SPECIFIC.value - 1, self.create_checkbox())
        elif current_tab_index == 1:  # Table 2 is active
            for _ in range(row_count):
                self.table2.insertRow(self.table2.rowCount())
                row = self.table2.rowCount() - 1

                self.dm_User_Input.get_Table(Utils.TabName.TAB2.value).add_row(columns={
                    self.T2CN.COLUMN_VARIABLE_NAME.value        : Utils.Column(value=""         , name=self.T2CN.COLUMN_VARIABLE_NAME.value   , is_pk=True    , column_type="String"),
                    self.T2CN.COLUMN_PK.value                   : Utils.Column(value="False"    , name=self.T2CN.COLUMN_PK.value              , is_pk=False   , column_type="Boolean"),
                    self.T2CN.COLUMN_TABLE_NAME.value           : Utils.Column(value=""         , name=self.T2CN.COLUMN_TABLE_NAME.value      , is_pk=False   , column_type="String"),
                    self.T2CN.COLUMN_ALLOCATION.value           : Utils.Column(value=""         , name=self.T2CN.COLUMN_ALLOCATION.value      , is_pk=False   , column_type="String"),
                    self.T2CN.COLUMN_DOMAIN.value               : Utils.Column(value=""         , name=self.T2CN.COLUMN_DOMAIN.value          , is_pk=False   , column_type="String")
                })

                self.table2.setCellWidget(row, Utils.Table2ColumnOrder.COLUMN_PK.value - 1, self.create_checkbox())
                self.table2.setCellWidget(row, Utils.Table2ColumnOrder.COLUMN_ALLOCATION.value - 1, self.create_dropdown(["Replicate", "Proportional"]))
                self.table2.setCellWidget(row, Utils.Table2ColumnOrder.COLUMN_DOMAIN.value - 1, self.create_dropdown([""]))
    
    def create_checkbox(self):
        checkbox = QCheckBox()
        checkbox.setStyleSheet(
            "QCheckBox::indicator { width: 20px; height: 20px; border-radius: 3px; border: 2px solid #777; background: white; }"
            "QCheckBox::indicator:checked { background-color: #28a745; border: 2px solid #28a745; }"
            "QCheckBox::indicator:unchecked { background-color: white; border: 2px solid #777; }"
            "QCheckBox { spacing: 0px; }"
        )
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addWidget(checkbox)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        return widget
    
    def refresh_dropdowns(self, EntityID : str = "", FilterValue : str = ""):
        """Refreshes all dropdowns in table2."""
        if self.dm_inmemory_data is None:
            return
        
        domain_values = self.dm_inmemory_data.get_column_values_filtered(table_name=Utils.IMConfigurationTable.DOMAIN.value, column_name=Utils.IMConfigurationDomain.NAME.value, FilterColumn = EntityID, FilterValue = FilterValue)
        dropdown: QComboBox

        for row in range(self.table2.rowCount()):
            dropdown = self.table2.cellWidget(row, Utils.Table2ColumnOrder.COLUMN_DOMAIN.value - 1)
            currentValue = dropdown.currentText()
            if FilterValue != "" or FilterValue is None:
                self.table2.setCellWidget(row, Utils.Table2ColumnOrder.COLUMN_DOMAIN.value - 1, self.create_dropdown(domain_values, addNone=True, currentValue=currentValue))
            else:
                self.table2.setCellWidget(row, Utils.Table2ColumnOrder.COLUMN_DOMAIN.value - 1, self.create_dropdown(domain_values, addNone=True))

    def create_dropdown(self, options: collections.abc.Iterable[typing.Optional[str]], addNone: bool = False, currentValue: str = ""):
        dropdown = QComboBox()

        if addNone:
            dropdown.addItem("")

        if isinstance(options, str):
            options = [options]

        if len(options) != 0:
            dropdown.addItems(options)

        if currentValue != "":
            dropdown.setCurrentText(currentValue)
        else:
            dropdown.setCurrentText("")
        return dropdown
        

    def get_button_style(self):
        """Returns the appropriate button style based on system theme."""
        if self.is_dark_mode:
            return "background-color: #1E1E1E; color: white; font-size: 14px; border-radius: 5px; padding: 8px;"
        else:
            return "background-color: #34495E; color: white; font-size: 14px; border-radius: 5px; padding: 8px;"
    
    def check_dark_mode(self):
        """Checks if the system is in dark mode."""
        palette = QApplication.instance().palette()
        return palette.color(QPalette.ColorRole.Window).lightness() < 128
    
    def show_table1_context_menu(self, position):
        """Shows the context menu for Table 1."""
        menu = QMenu()

        row = self.table1.currentRow()
        if self.table1.item(row, self.T1CO.COLUMN_TABLE_NAME.value-1) is not None:
            CSV_XML_Editor.TableValue = self.table1.item(row, self.T1CO.COLUMN_TABLE_NAME.value-1).text()
        else:
            CSV_XML_Editor.TableValue = ""

        open_dialog_action = QAction("Open Variable Tab", self)
        open_dialog_action.triggered.connect(self.open_table3_dialog)
        menu.addAction(open_dialog_action)
        menu.exec(self.table1.viewport().mapToGlobal(position))

    def open_table3_dialog(self):
        print("Opening Table 3 dialog...")  # Debug log
        dialog = Table3Dialog(self)
        dialog.exec()
    
if __name__ == "__main__":
    print("Starting application...")  # Debug log
    app = QApplication(sys.argv)
    window = CSV_XML_Editor()
    window.show()
    sys.exit(app.exec())
