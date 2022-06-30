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

message_box = sgtk.platform.import_framework("tk-framework-qtwidgets", "message_box")
MessageBox = message_box.MessageBox


class MessageBoxDemo(QtGui.QWidget):
    """
    A demonstration of the MessageBox class.
    """

    def __init__(self, parent=None):
        """
        Initialize the demo widget.
        """

        super(MessageBoxDemo, self).__init__(parent)

        self._always_show_details = False
        self._show_remember_checkbox = True

        # Build and layout the UI.
        self._populate_ui()

    def _populate_ui(self):
        """
        Build the UI.
        """

        show_msg_box = QtGui.QPushButton("Click to show MessageBox")
        show_msg_box.clicked.connect(self._show_message_box)

        show_details_always = QtGui.QCheckBox("Always Show Details")
        show_details_always.clicked.connect(self._set_always_show_details)

        show_remember_checkbox = QtGui.QCheckBox("Hide Remember Checkbox")
        show_remember_checkbox.clicked.connect(self._set_show_remember_checkbox)

        show_details_text_label = QtGui.QLabel(
            "Customize the 'Show Details...' Button Text:"
        )
        show_details_text_label.setToolTip("Leave blank to use default")
        self._show_details_text = QtGui.QLineEdit()
        show_details_text_layout = QtGui.QHBoxLayout()
        show_details_text_layout.addWidget(show_details_text_label)
        show_details_text_layout.addWidget(self._show_details_text)

        hide_details_text_label = QtGui.QLabel(
            "Customize the 'Hide Details...' Button Text:"
        )
        hide_details_text_label.setToolTip("Leave blank to use default")
        self._hide_details_text = QtGui.QLineEdit()
        hide_details_text_layout = QtGui.QHBoxLayout()
        hide_details_text_layout.addWidget(hide_details_text_label)
        hide_details_text_layout.addWidget(self._hide_details_text)

        checkbox_options = QtGui.QHBoxLayout()
        checkbox_options.addWidget(show_details_always)
        checkbox_options.addWidget(show_remember_checkbox)
        checkbox_options.addStretch()

        toolbar_layout = QtGui.QVBoxLayout()
        toolbar_layout.addLayout(checkbox_options)
        toolbar_layout.addLayout(show_details_text_layout)
        toolbar_layout.addLayout(hide_details_text_layout)

        self._msg_box_result = QtGui.QLabel()
        self._msg_box_result.setToolTip(
            "This is the button role of the button that was clicked to close the dialog."
        )
        self._button_clicked_result = QtGui.QLabel()
        self._msg_box_result.setToolTip(
            "This is the button that was clicked to close the dialog."
        )
        self._remember_value = QtGui.QLabel()
        self._msg_box_result.setToolTip(
            "This is the value of the 'remember' checkbox on closing the dialog."
        )

        footer_layout = QtGui.QVBoxLayout()
        footer_layout.addWidget(self._msg_box_result)
        footer_layout.addWidget(self._button_clicked_result)
        footer_layout.addWidget(self._remember_value)

        # The main demo layout
        vlayout = QtGui.QVBoxLayout()
        vlayout.addLayout(toolbar_layout)
        vlayout.addStretch()
        vlayout.addWidget(show_msg_box)
        vlayout.addStretch()
        vlayout.addLayout(footer_layout)

        self.setLayout(vlayout)

    def _show_message_box(self):
        """
        """

        msg_box = MessageBox(self)
        msg_box.setWindowTitle("MessageBox Demo")

        msg_box.set_text("This is the message box text.")
        msg_box.set_detailed_text("This is the message box detailed text.")

        msg_box.add_button("First Button", MessageBox.ACCEPT_ROLE)
        msg_box.add_button("Second Button", MessageBox.REJECT_ROLE)
        default_button = msg_box.add_button("Last Button", MessageBox.APPLY_ROLE)
        msg_box.set_default_button(default_button)

        msg_box.show_remember_checkbox(self._show_remember_checkbox)
        msg_box.set_always_show_details(self._always_show_details)

        if self._show_details_text.text():
            msg_box.set_show_details_text(self._show_details_text.text())

        if self._hide_details_text.text():
            msg_box.set_hide_details_text(self._hide_details_text.text())

        msg_box.exec_()

        self._msg_box_result.setText("Message Result: {}".format(msg_box.result()))
        self._button_clicked_result.setText(
            "Button Clicked: {}".format(
                msg_box.button_clicked.text()
                if msg_box.button_clicked
                else "No button clicked"
            )
        )
        self._remember_value.setText(
            "Remember Checkbox Value: {}".format(msg_box.get_remember_value())
        )

    def _set_always_show_details(self, checked=False):
        """
        """

        self._always_show_details = not self._always_show_details

    def _set_show_remember_checkbox(self, checked=False):
        """
        """

        self._show_remember_checkbox = not self._show_remember_checkbox
