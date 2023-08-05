# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import gui


class TextEdit(QtWidgets.QTextEdit):

    def set_enabled(self):
        self.setEnabled(True)

    def set_disabled(self):
        self.setEnabled(False)

    def set_font(self,
                 font_name: str,
                 font_size: int = -1,
                 weight: int = -1,
                 italic: bool = False):
        font = gui.Font(font_name, font_size, weight, italic)
        self.setFont(font)

    def set_text(self, text: str):
        self.setPlainText(text)

    def append_text(self, text: str):
        self.append(text)

    def text(self) -> str:
        return self.toPlainText()

    def set_read_only(self, value: bool = True):
        self.setReadOnly(value)

    def scroll_to_end(self):
        """scroll to the end of the text
        """
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

    def set_color(self, color):
        self.setStyleSheet(f"background-color: {color};")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = TextEdit("This is a test")
    widget.show()
    app.exec_()
