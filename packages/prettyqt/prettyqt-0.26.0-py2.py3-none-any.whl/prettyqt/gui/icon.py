# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import pathlib

from qtpy import QtGui, QtCore
import qtawesome as qta

from prettyqt import gui, widgets


class Icon(QtGui.QIcon):

    def __init__(self, icon=None):
        if isinstance(icon, pathlib.Path):
            icon = str(icon)
        super().__init__(icon)

    def __reduce__(self):
        return type(self), (), self.__getstate__()

    def __getstate__(self):
        ba = QtCore.QByteArray()
        stream = QtCore.QDataStream(ba, QtCore.QIODevice.WriteOnly)
        stream << self
        return ba

    def __setstate__(self, ba):
        stream = QtCore.QDataStream(ba, QtCore.QIODevice.ReadOnly)
        stream >> self

    @classmethod
    def for_color(cls, color: str):
        color = gui.Color.from_text(color)
        if color.isValid():
            bitmap = gui.Pixmap(16, 16)
            bitmap.fill(color)
            icon = gui.Icon(bitmap)
        else:
            icon = qta.icon("mdi.card-outline")
        return icon


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    icon = Icon.for_color("green")
