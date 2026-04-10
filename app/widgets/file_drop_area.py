from PySide6.QtWidgets import QLabel


class FileDropArea(QLabel):

    def __init__(self):
        super().__init__("Drop XLSX file here")
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.parent().load_file(file_path)