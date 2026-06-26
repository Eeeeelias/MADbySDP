import shutil

import pandas as pd
import traceback
from PySide6.QtWidgets import (
    QMainWindow,
    QTableWidgetItem,
    QFileDialog,
)
from PySide6.QtCore import Qt

from app.ui_mainwindow import Ui_MainWindow
from core.validator import validate_dataframe
from core.processor import run_processing


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.file_path = None
        self.df = None
        self.xct_gen = None
        self.missing_cols = []
        self.excel_sheet = ""
        self.available_sheets = None

        self.setAcceptDrops(True)

        self.ui.option_sheet.currentIndexChanged.connect(self.sheet_change_event)

        self.ui.xct_gen_1.toggled.connect(self.set_processing)
        self.ui.xct_gen_2.toggled.connect(self.set_processing)

        self.ui.process_button.clicked.connect(self.process_file)
        self.ui.clear_button.clicked.connect(self.clear_file)

    # -----------------------------
    # Drag and drop support
    # -----------------------------

    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):

        file_path = event.mimeData().urls()[0].toLocalFile()

        if file_path.endswith(".xlsx"):
            self.load_file(file_path)

    def set_processing(self):
        if self.df is None:

            self.ui.process_button.setEnabled(False)
            self.ui.status_label.setText("Status: Waiting for file")
            return

        # terrible pattern but I'm setting the global xct_gen param here, sorry
        self.xct_gen = self.get_selected_xct_gen()
        self.missing_cols = validate_dataframe(self.df, self.xct_gen)

        if self.missing_cols:
            self.ui.process_button.setEnabled(False)

            self.ui.status_label.setText(
                f"Status: ⚠ Missing params: {', '.join(self.missing_cols)}"
            )
            return

        self.ui.process_button.setEnabled(True)

        self.ui.status_label.setText("Status: Ready to process")

    # -----------------------------
    # Load XLSX
    # -----------------------------

    def load_file(self, file_path, sheet_name=None):

        try:
            if sheet_name is None:
                self.df = pd.read_excel(file_path)
            else:
                self.df = pd.read_excel(file_path, sheet_name=sheet_name)
            self.file_path = file_path

            self.populate_table()

            if sheet_name is None:
                self.populate_sheets()

            self.set_processing()

            self.ui.clear_button.setEnabled(True)

            self.setAcceptDrops(False)
            self.ui.drop_label.setText("Clear current file to drop new file")

        except Exception as e:

            self.ui.status_label.setText(
                f"Error loading file: {str(e)}"
            )

            self.ui.process_button.setEnabled(False)

    # -----------------------------
    # Populate preview table
    # -----------------------------

    def populate_table(self):

        df = self.df

        self.ui.table.setRowCount(len(df.index))
        self.ui.table.setColumnCount(len(df.columns))

        self.ui.table.setHorizontalHeaderLabels(df.columns)

        preview_rows = min(len(df.index), 1000)

        for row in range(preview_rows):

            for col in range(len(df.columns)):

                value = str(df.iloc[row, col])

                self.ui.table.setItem(
                    row,
                    col,
                    QTableWidgetItem(value),
                )

    #-----------------------------
    # Handle sheets sheets
    #-----------------------------
    def populate_sheets(self):
        with pd.ExcelFile(self.file_path, engine='openpyxl') as xls:
            self.available_sheets = xls.sheet_names
        self.ui.option_sheet.addItems(self.available_sheets)

    def sheet_change_event(self):
        self.excel_sheet = self.ui.option_sheet.currentText()
        self.load_file(self.file_path, self.excel_sheet)

    #-----------------------------
    # Processing XCT Generation
    #-----------------------------

    def get_selected_xct_gen(self):
        if self.ui.xct_gen_1.isChecked():
            return 1

        if self.ui.xct_gen_2.isChecked():
            return 2

        return 0

    #-----------------------------
    # Processing Conformal options
    #-----------------------------

    def get_selected_conformal_highlights(self):
        highlighted = []
        if self.ui.conformal_85.isChecked():
            highlighted.append("85th")

        if self.ui.conformal_95.isChecked():
            highlighted.append("95th")

        return highlighted

    # -----------------------------
    # Processing model
    # -----------------------------

    def get_selected_model(self):

        if self.ui.option_balanced.isChecked():
            return "balanced"

        if self.ui.option_unbalanced.isChecked():
            return "unbalanced"

        return "balanced"

    # -----------------------------
    # Run processing
    # -----------------------------

    def process_file(self):

        if self.df is None:

            self.ui.status_label.setText(
                "Load a file first"
            )

            return

        model = self.get_selected_model()

        conformal_highlights = self.get_selected_conformal_highlights()

        output_file_path = self.file_path[:-5] + "_processed.xlsx"

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save processed file",
            output_file_path,
            "Excel Files (*.xlsx)",
        )

        if not save_path:
            return
        
        print("Running this")
        
        shutil.copy(self.file_path, save_path)

        try:

            run_processing(dataframe=self.df, model_type=model, xct_gen=self.xct_gen, conformal=conformal_highlights, 
                           output_path=save_path, sheet_name=self.excel_sheet)

            self.ui.status_label.setText(
                "Processing complete"
            )

        except Exception as e:

            print(traceback.format_exc())

            self.ui.status_label.setText(
                f"Processing failed: {str(e)}"
            )

    # -----------------------------
    # Reset everything
    # -----------------------------

    def clear_file(self):
        self.file_path = None
        self.df = None
        self.xct_gen = None
        self.missing_cols = []
        self.available_sheets = None

        # reset table
        self.ui.table.clear()
        self.ui.table.setRowCount(0)
        self.ui.table.setColumnCount(0)

        # reset all buttons
        self.ui.option_sheet.clear()
        self.ui.conformal_95.setChecked(False)
        self.ui.conformal_85.setChecked(True)
        self.ui.option_balanced.setChecked(True)
        self.ui.option_unbalanced.setChecked(False)
        self.ui.xct_gen_1.setChecked(False)
        self.ui.xct_gen_2.setChecked(False)

        # reset status
        self.ui.status_label.setText("Status: No file loaded")
        self.ui.drop_label.setText("Drop XLSX file here")

        self.setAcceptDrops(True)