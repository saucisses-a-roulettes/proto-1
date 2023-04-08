import sys

from PySide6.QtCore import Qt, QPoint, QPointF
from PySide6.QtGui import QMouseEvent, QPixmap, QPainter, QColor
from PySide6.QtWidgets import QMainWindow, QLabel, QApplication


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self._image = QPixmap("tympan.jpg")

        self._draft_canvas = QPixmap(self._image.size())
        self._draft_canvas.fill(QColor(0, 0, 0, 0))

        self._label = QLabel()
        self.setCentralWidget(self._label)

        self._last_point: QPoint | QPointF | None = None

        self._draw_label()

    def _draw_label(self) -> None:
        new_canvas = QPixmap(self._image.size())
        painter = QPainter(new_canvas)
        painter.drawPixmap(0, 0, self._image)
        painter.drawPixmap(0, 0, self._draft_canvas)
        painter.end()
        self._label.setPixmap(new_canvas)

    def _draw_point(self, point: QPoint | QPointF) -> None:
        if self._last_point is None:
            self._last_point = point
            return

        painter = QPainter(self._draft_canvas)
        painter.drawLine(self._last_point, point)
        painter.end()

        self._last_point = point

        self._draw_label()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            self._draw_point(event.position())

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._last_point = None


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
