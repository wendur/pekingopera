import sys
from PekingOpera import *

from PyQt5.QtCore import Qt, QRect, QRectF
from PyQt5.QtGui import QColor, QPainter, QBrush, QFont, QTextOption
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget

# Класс отрисовки
class PyQtGame(QWidget):
    def __init__(self):
        super(PyQtGame, self).__init__()
        self.game = PekingOpera(7, 9, 10) # создание экземпляра игры
        self.colors = {
            1: QColor(0xFF0000),
            2: QColor(0xFFFF00),
            3: QColor(0x00FF00),
            4: QColor(0x00FFFF),
            5: QColor(0xFF00FF)
        }
        self.initUI() # инициализация игры

    def initUI(self):
        self.setFixedSize(740, 420)
        self.centerWindow()
        self.setWindowTitle("PEKINGOPERA")
        self.show()

    def centerWindow(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, e):
        self.last_point = e.pos()

    # обработка нажатий кнопки мыши
    def mouseReleaseEvent(self, e):
        self.restart_rect = QRect(530, 160, 180, 40)
        if self.restart_rect.contains(e.pos().x(), e.pos().y()) \
                and self.restart_rect.contains(self.last_point.x(), self.last_point.y()):
            self.game.reset_game()
            self.update()

        self.field = QRect(20, 20, 476, 374)
        if self.field.contains(e.pos().x(), e.pos().y()) \
                and self.field.contains(self.last_point.x(), self.last_point.y()):
            self.game.add_cell(int((self.last_point.y() - 25) / 52), int((self.last_point.x() - 25) / 52))
            self.update()

    # отрисовка элементов, рисуется через QtPainter
    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)

        painter.setBrush(QBrush(QColor(0xFFFFFF)))
        painter.drawRect(self.rect())

        painter.setBrush(QBrush(QColor(0x999999)))
        painter.drawRoundedRect(QRect(20, 20, 476, 374), 10, 10)

        painter.setBrush(QBrush(QColor(0x999999)))
        painter.drawRoundedRect(QRect(520, 20, 200, 374), 10, 10)

        painter.setFont(QFont("Franklin Gothic Medium", 18))
        painter.setPen(QColor(0xFFFFFF))
        painter.drawText(QRectF(QRect(530, 25, 180, 25)), "SCORE", QTextOption(Qt.AlignHCenter))
        painter.setPen(Qt.NoPen)

        painter.setBrush(QBrush(QColor(0x000000)))

        painter.setPen(QColor(0xFFFFFF))
        painter.drawText(QRectF(QRect(540, 55, 160, 25)), "BEST:", QTextOption(Qt.AlignLeft | Qt.AlignVCenter))
        painter.drawText(QRectF(QRect(540, 55, 160, 25)), str(self.game.best_score),
                         QTextOption(Qt.AlignRight| Qt.AlignVCenter))
        painter.setPen(Qt.NoPen)

        painter.setPen(QColor(0xFFFFFF))
        painter.drawText(QRectF(QRect(540, 85, 160, 25)), "CUR:", QTextOption(Qt.AlignLeft | Qt.AlignVCenter))
        painter.drawText(QRectF(QRect(540, 85, 160, 25)), str(self.game.score),
                         QTextOption(Qt.AlignRight | Qt.AlignVCenter))
        painter.setPen(Qt.NoPen)

        painter.setFont(QFont("Franklin Gothic Medium", 14))
        painter.setPen(QColor(0xFFFFFF))
        painter.drawText(QRectF(QRect(540, 125, 160, 25)), "MOVES LEFT:", QTextOption(Qt.AlignLeft))
        painter.drawText(QRectF(QRect(540, 125, 160, 25)), str(self.game.moves_left),
                         QTextOption(Qt.AlignRight))
        painter.setPen(Qt.NoPen)

        painter.setBrush(QBrush(QColor(0x787878)))
        painter.drawRoundedRect(QRect(530, 160, 180, 40), 6, 6)
        painter.setFont(QFont("Franklin Gothic Medium", 18))
        painter.setPen(QColor(0xFFFFFF))
        painter.drawText(QRectF(QRect(540, 165, 160, 40)), "RESTART", QTextOption(Qt.AlignHCenter))
        painter.setPen(Qt.NoPen)

        self.drawRectangles(painter)

        if not self.game.playing:
            painter.setBrush(QBrush(QColor(80, 80, 80, 150)))
            painter.drawRoundedRect(QRect(20, 20, 476, 374), 10, 10)

            painter.setFont(QFont("Franklin Gothic Medium", 35))
            painter.setPen(QColor(0xffffff))
            painter.drawText(QRectF(QRect(20, 20, 476, 374)), "MOVES OVER", QTextOption(Qt.AlignHCenter | Qt.AlignVCenter))
            painter.setPen(Qt.NoPen)

    # отрисовка ячеек
    def drawRectangles(self, painter):
        for i in range(self.game.row):
            for j in range(self.game.col):
                painter.setBrush(QColor(0, 0, 0))
                painter.drawRoundedRect(QRect(25 + j * 52, 25 + i * 52, 50, 50), 8, 8)

                painter.setBrush(self.colors[self.game.field[i][j]])
                painter.drawRoundedRect(QRect(27 + j * 52, 27 + i * 52, 46, 46), 8, 8)

                painter.setBrush(Qt.NoBrush)
                painter.setPen(Qt.NoPen)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = PyQtGame()
    sys.exit(app.exec_())
