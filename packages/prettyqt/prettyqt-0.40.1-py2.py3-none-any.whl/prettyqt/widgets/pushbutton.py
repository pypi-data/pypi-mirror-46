# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import core, widgets


class PushButton(QtWidgets.QPushButton):

    value_changed = core.Signal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toggled.connect(self.value_changed)

    def get_value(self):
        return None

    def set_value(self, value):
        return None


PushButton.__bases__[0].__bases__ = (widgets.AbstractButton,)


if __name__ == "__main__":
    app = widgets.app()
    widget = PushButton("This is a test")
    widget.show()
    app.exec_()
