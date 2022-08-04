# Copyright (c) 2021 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
#
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk, Inc.

import sgtk
from sgtk.platform.qt import QtGui

sg_qwidgets = sgtk.platform.import_framework("tk-framework-qtwidgets", "sg_qwidgets")
sg_qicons = sgtk.platform.import_framework("tk-framework-qtwidgets", "sg_qicons")


class SGQWidgetsDemo(QtGui.QWidget):
    """
    A demonstration of the ShotGrid widget wrapper classes.
    """

    def __init__(self, parent=None):
        """
        Initialize the demo widget.
        """

        super(SGQWidgetsDemo, self).__init__(parent)

        self._example_qss = "<br/>".join(
            [
                "SGQToolButton",
                "{",
                "border: none;",
                "outline: none;",
                "padding: 4px;",
                "}",
                "<br/>",
                "SGQToolButton:checked,",
                "SGQToolButton:hover",
                "{",
                "\tbackground-color: palette(light);",
                "\tborder-radius: 4px;",
                "}",
                "<br/>",
                "SGQToolButton:hover",
                "{",
                "\tcolor: rgba(255, 255, 255, 1);",
                "}",
                "<br/>",
                "SGQLabel",
                "{",
                "\tcolor: yellowgreen;",
                "}",
                "<br/>",
                "SGQLabel:hover",
                "{",
                "\tcolor: red;",
                "}",
                "<br/>",
                "SGQCheckBox",
                "{",
                "\tcolor: orange;",
                "}",
                "<br/>",
                "SGQPushButton:hover",
                "{",
                "\tcolor: blue;",
                "}",
            ]
        )

        # Build and layout the UI.
        self._populate_ui()

    def _populate_ui(self):
        """
        Build the UI.
        """

        # Help info message
        info = QtGui.QLabel(
            "Edit the qss style sheet below and click 'Apply Style' to apply the style to the widgets below."
        )

        # Text edit to modify the qss style
        self._qss_text_edit = QtGui.QTextEdit()
        self._qss_text_edit.setHtml(self._example_qss)
        qss_reload_button = sg_qwidgets.SGQPushButton("Apply Style")
        qss_reload_button.clicked.connect(self._reload_qss_style)

        # Example widgets
        label = sg_qwidgets.SGQLabel("SGQLabel widget")
        checkbox = sg_qwidgets.SGQCheckBox("SGQCheckBox widget")
        push_button = sg_qwidgets.SGQPushButton("SGQPushButton widget")
        tool_button = sg_qwidgets.SGQToolButton(self, sg_qicons.SGQIcon.info())

        # Widgets layout
        hlayout = QtGui.QHBoxLayout()
        hlayout.addWidget(label)
        hlayout.addWidget(checkbox)
        hlayout.addWidget(push_button)
        hlayout.addWidget(tool_button)

        # Widget container
        widgets = QtGui.QWidget(self)
        widgets.setLayout(hlayout)

        # The main demo layout
        vlayout = QtGui.QVBoxLayout()
        vlayout.addWidget(info)
        vlayout.addWidget(self._qss_text_edit)
        vlayout.addWidget(qss_reload_button)
        vlayout.addWidget(widgets)

        self.setLayout(vlayout)

    def _reload_qss_style(self):
        """
        Reload the qss style with the data from the qss text edit.
        """

        self.setStyleSheet(self._qss_text_edit.toPlainText())
