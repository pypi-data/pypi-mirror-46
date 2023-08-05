# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

from qtpy import QtWidgets

from prettyqt import widgets

MODES = dict(maximum=QtWidgets.QLayout.SetMaximumSize,
             fixed=QtWidgets.QLayout.SetFixedSize)


class FormLayout(QtWidgets.QFormLayout):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_mode("maximum")
        self.setVerticalSpacing(8)

    def __getitem__(self, index):
        return self.itemAt(index)

    def __iter__(self):
        return iter(self[i] for i in range(self.count()) if self[i] is not None)

    def __len__(self):
        """needed for PySide2
        """
        return self.rowCount()

    def set_size_mode(self, mode: str):
        if mode not in MODES:
            raise ValueError(f"{mode} not a valid size mode.")
        self.setSizeConstraint(MODES[mode])

    def set_label_widget(self, row: int, widget):
        """set a widget for the label position at given row

        Args:
            row: Row offset
            widget: widget to get added to layout
        """
        if isinstance(widget, str):
            widget = widgets.Label(widget)
        if isinstance(widget, QtWidgets.QLayout):
            self.setLayout(row, self.LabelRole, widget)
        else:
            self.setWidget(row, self.LabelRole, widget)

    def set_field_widget(self, row: int, widget):
        """set a widget for the field position at given row

        Args:
            row: Row offset
            widget: widget / layout to get added to layout
        """
        if isinstance(widget, str):
            widget = widgets.Label(widget)
        if isinstance(widget, QtWidgets.QLayout):
            self.setLayout(row, self.FieldRole, widget)
        else:
            self.setWidget(row, self.FieldRole, widget)

    def set_spanning_widget(self, row: int, widget):
        """set a widget spanning label and field position at given row

        Args:
            row: Row offset
            widget: widget / layout to get added to layout
        """
        if isinstance(widget, str):
            widget = widgets.Label(widget)
        if isinstance(widget, QtWidgets.QLayout):
            self.setLayout(row, self.SpanningRole, widget)
        else:
            self.setWidget(row, self.SpanningRole, widget)

    @classmethod
    def from_dict(cls, dct, parent=None):
        formlayout = FormLayout(parent)
        for i, (k, v) in enumerate(dct.items(), start=1):
            if k is not None:
                formlayout.set_label_widget(i, k)
            if v is not None:
                formlayout.set_field_widget(i, v)
        return formlayout


if __name__ == "__main__":
    app = widgets.Application.create_default_app()
    dct = {"key": widgets.Label("test"),
           None: widgets.Label("test 2")}
    layout = FormLayout.from_dict(dct)
    widget = widgets.Widget()
    widget.setLayout(layout)
    widget.show()
    app.exec_()
