from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QRadioButton,
    QGroupBox, QCheckBox,
)


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        MainWindow.setWindowTitle("Automatic Motion Grading")
        MainWindow.resize(900, 600)

        self.central_widget = QWidget()
        MainWindow.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Drag-and-drop label
        self.drop_label = QLabel("Drop XLSX file here")
        self.drop_label.setStyleSheet(
            "border: 2px dashed gray; padding: 20px;"
        )
        self.drop_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.drop_label)

        # Preview table
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # select model
        self.options_group = QGroupBox("Model Choice")
        self.options_layout = QHBoxLayout()

        self.option_balanced = QRadioButton("balanced")
        self.option_unbalanced = QRadioButton("unbalanced")

        self.option_balanced.setChecked(True)

        self.options_layout.addWidget(self.option_balanced)
        self.options_layout.addWidget(self.option_unbalanced)

        self.options_group.setLayout(self.options_layout)

        # select xct gen
        self.xct_group = QGroupBox("XCT Generation")
        self.xct_layout = QHBoxLayout()

        self.xct_gen_1 = QRadioButton("XCT 1")
        self.xct_gen_2 = QRadioButton("XCT 2")

        self.xct_layout.addWidget(self.xct_gen_1)
        self.xct_layout.addWidget(self.xct_gen_2)

        self.xct_group.setLayout(self.xct_layout)

        # select conformal highlights

        self.conformal_group = QGroupBox("Conformal Highlighting")
        self.conformal_layout = QHBoxLayout()

        self.conformal_85 = QCheckBox("85th percentile")
        self.conformal_95 = QCheckBox("95th percentile")

        self.conformal_layout.addWidget(self.conformal_85)
        self.conformal_layout.addWidget(self.conformal_95)

        self.conformal_85.setChecked(True)

        self.conformal_group.setLayout(self.conformal_layout)

        self.option_row = QHBoxLayout()

        self.option_row.addWidget(self.xct_group)
        self.option_row.addWidget(self.options_group)
        self.option_row.addWidget(self.conformal_group)
        self.layout.addLayout(self.option_row)

        self.bottom_row = QHBoxLayout()

        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.setEnabled(False)
        self.clear_button.setMinimumHeight(55)

        # Process button
        self.process_button = QPushButton("Grade File")
        self.process_button.setEnabled(False)
        self.process_button.setMinimumHeight(55)

        self.bottom_row.addWidget(self.clear_button)
        self.bottom_row.addWidget(self.process_button)

        self.layout.addLayout(self.bottom_row)

        # Status label
        self.status_label = QLabel("Status: waiting for file")
        self.layout.addWidget(self.status_label)