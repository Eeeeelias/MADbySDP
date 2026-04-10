from PySide6.QtWidgets import QApplication
from app.window import MainWindow

app = QApplication([])
window = MainWindow()
window.show()
app.exec()