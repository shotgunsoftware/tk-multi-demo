# Copyright (c) 2016 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import sgtk
from sgtk.platform.qt import QtCore, QtGui
from sgtk.util import get_current_user

# import the note_input_widget module from the qtwidgets framework
note_input_widget = sgtk.platform.import_framework(
    "tk-framework-qtwidgets", "note_input_widget")

# import the task manager from shotgunutils framework
task_manager = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "task_manager")


class NoteInputWidgetDemo(QtGui.QWidget):
    """
    Demos the NoteInputWidget from the qtwidgets frameworks.
    """

    def __init__(self, parent=None):
        """
        Initialize the demo widget.
        """

        # call the base class init
        super(NoteInputWidgetDemo, self).__init__(parent)

        # create a background task manager for the widget to use
        self._bg_task_manager = task_manager.BackgroundTaskManager(self)

        self._note_input = note_input_widget.NoteInputWidget(self)
        self._note_input.set_bg_task_manager(self._bg_task_manager)

        engine = sgtk.platform.current_engine()
        user = get_current_user(engine.sgtk)

        if not user:
            raise Exception("Could not determine the current user.")

        self._note_input.set_current_entity(user["type"], user["id"])

        info_lbl = QtGui.QLabel(
            "<strong>LIVE DEMO</strong>: If you click the checkmark to submit "
            "the input, you will attach a new Note to yourself in Shotgun. "
            "Just a heads up in case you want to delete it afterward."
        )
        info_lbl.setWordWrap(True)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(info_lbl)
        layout.addStretch()
        layout.addWidget(self._note_input)
        layout.addStretch()

    def destroy(self):
        """
        Clean up the object when deleted.
        """
        self._bg_task_manager.shut_down()
        self._note_input.destroy()


