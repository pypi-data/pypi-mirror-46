# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets


class MenuBar(QtWidgets.QMenuBar):

    def __add__(self, other):
        if isinstance(other, QtWidgets.QAction):
            self.add_action(other)
            return self

    def add_action(self, action):
        self.addAction(action)


MenuBar.__bases__[0].__bases__ = (widgets.Widget,)


if __name__ == "__main__":
    app = widgets.app()
    win = QtWidgets.QMainWindow()
    menu_bar = MenuBar()
    win.setMenuBar(menu_bar)
    win.show()
    app.exec_()
