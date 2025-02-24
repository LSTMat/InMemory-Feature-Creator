import sys
import collections, re, typing, enum
import os
import Utils as DM
import pandas as pd
import xml.etree.ElementTree as ET
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QMenuBar, 
                             QFileDialog, QTableWidget, QTableWidgetItem, QTabWidget, QCheckBox, QComboBox, 
                             QHBoxLayout, QPushButton, QHeaderView, QSpinBox, QDialog, QLabel, QLineEdit)
from PyQt6.QtGui import QAction, QFont, QPalette, QColor
from PyQt6.QtCore import Qt

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
        self.parent().inmemory_data = DM.load_xml_to_config(selected_file, selected_config_path)
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

class CSV_XML_Editor(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing CSV_XML_Editor...")  # Debug log
        self.xml_structure = {}  # Stores the structure of InMemory XML
        self.inmemory_data: DM.InMemoryConfiguration  # Stores data from user-loaded XML
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
        self.table1 = QTableWidget()
        self.style_table(self.table1)
        self.table1.setColumnCount(5)
        self.table1.setRowCount(10)
        self.table1.setHorizontalHeaderLabels(["Table Name", "Entity", "Domain", "View", "Alias Specific"])
        self.initialize_table1()
        self.tabs.addTab(self.table1, "Tabelle")
        
        # Table 2 setup
        print("Initializing Table 2...")  # Debug log
        self.table2 = QTableWidget()
        self.style_table(self.table2)
        self.table2.setColumnCount(5)
        self.table2.setRowCount(10)
        self.table2.setHorizontalHeaderLabels(["Variable Name", "PK", "Table Name", "Allocation", "Domain"])
        self.initialize_table2()
        self.tabs.addTab(self.table2, "Calculation Plan")
        
        layout.addWidget(self.tabs)
        
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
        for row in range(10):
            for col in range(1, 5):
                self.table1.setCellWidget(row, col, self.create_checkbox())
    
    def initialize_table2(self):
        """Initializes checkboxes and dropdowns in table2."""
        print("Populating Table 2...")  # Debug log
        for row in range(10):
            self.table2.setCellWidget(row, 1, self.create_checkbox())
            self.table2.setCellWidget(row, 3, self.create_dropdown(["Replicate", "Proportional"]))
            self.table2.setCellWidget(row, 4, self.create_dropdown(["None"]))

    def style_table(self, table):
        """Applies styling to tables based on system theme."""
        table.setSortingEnabled(True)
        table.setAlternatingRowColors(True)
        if self.is_dark_mode:
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
        load_xml_action = QAction("Load XML", self)
        load_xml_action.triggered.connect(self.show_load_xml_dialog)
        file_menu.addAction(load_xml_action)
    
    def show_load_xml_dialog(self):
        """Opens the Load XML dialog."""
        dialog = LoadXMLDialog(self)
        if dialog.exec():
            print("XML Configuration Loaded")
            self.refresh_dropdowns()
    
    def generate_feature(self, sql_content):
        """Saves the SQL content to a file, prompting the user for a save location."""
        options = QFileDialog.Option.ReadOnly
        file_path, _ = QFileDialog.getSaveFileName(self, "Save SQL File", "", "SQL Files (*.sql)", options=options)
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
        for _ in range(row_count):
            self.table1.insertRow(self.table1.rowCount())
            self.table2.insertRow(self.table2.rowCount())
            row = self.table1.rowCount() - 1
            for col in range(1, 5):
                self.table1.setCellWidget(row, col, self.create_checkbox())
            self.table2.setCellWidget(row, 1, self.create_checkbox())
            self.table2.setCellWidget(row, 3, self.create_dropdown(["Replicate", "Proportional"]))
            self.table2.setCellWidget(row, 4, self.create_dropdown(["None"]))
    
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
    
    def refresh_dropdowns(self):
        """Refreshes all dropdowns in table2."""
        domain_values = self.inmemory_data.get_column_values("DMDomain", "Name")
        dropdown: QComboBox
        for row in range(self.table2.rowCount()):
            dropdown = self.table2.cellWidget(row, 4)
            currentValue = dropdown.currentText()
            if currentValue != "None":
                self.table2.setCellWidget(row, 4, self.create_dropdown(domain_values, addNone = True, currentValue = currentValue))
            else:
                self.table2.setCellWidget(row, 4, self.create_dropdown(domain_values, addNone = True))

    def create_dropdown(self, options: collections.abc.Iterable[typing.Optional[str]], addNone: bool = False, currentValue: str = "None"):
        dropdown = QComboBox()
        if addNone:
            dropdown.addItem("None")

        if len(options) != 0:
            dropdown.addItems(options)
                
        if currentValue != "None":
            dropdown.setCurrentText(currentValue)
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
    
if __name__ == "__main__":
    print("Starting application...")  # Debug log
    app = QApplication(sys.argv)
    window = CSV_XML_Editor()
    window.show()
    sys.exit(app.exec())
