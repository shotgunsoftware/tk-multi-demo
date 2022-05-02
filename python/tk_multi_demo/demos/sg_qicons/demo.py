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

sg_qicons = sgtk.platform.import_framework("tk-framework-qtwidgets", "sg_qicons")
SGQIcon = sg_qicons.SGQIcon


class SGQIconDemo(QtGui.QWidget):
    """
    A demonstration of the SGQIcon class.
    """

    def __init__(self, parent=None):
        """
        Initialize the demo widget.
        """

        super(SGQIconDemo, self).__init__(parent)

        self._icons = [
            {"icon": SGQIcon.ValidationOk,},
            {"icon": SGQIcon.ValidationError,},
            {"icon": SGQIcon.ValidationWarning,},
            {"icon": SGQIcon.RedRefresh,},
            {"icon": SGQIcon.Lock,},
            {"icon": SGQIcon.GreenCheckMark,},
            {"icon": SGQIcon.RedCheckMark,},
            {"icon": SGQIcon.RedBullet,},
            {"icon": SGQIcon.Filter,},
            {"icon": SGQIcon.Info,},
            {"icon": SGQIcon.TreeArrow,},
            {"icon": SGQIcon.ListViewMode,},
            {"icon": SGQIcon.ThumbnailViewMode,},
            {"icon": SGQIcon.GridViewMode,},
            {"icon": SGQIcon.Toggle,},
        ]

        # Build and layout the UI.
        self._populate_ui()

    def _populate_ui(self):
        """
        Build the UI.
        """

        vlayout = QtGui.QVBoxLayout(self)

        info = QtGui.QLabel(
            "Click the icons to toggle between inactive and active states (if available). Hover to see more information about each icon."
        )
        vlayout.addWidget(info)

        hlayout = QtGui.QHBoxLayout(self)

        for icon_data in self._icons:
            # Create a QToolButton to show the icon
            tb = QtGui.QToolButton(self)
            tb.setIcon(icon_data["icon"]())
            tb.setCheckable(True)
            tooltip = "Create using: SGQIcon.{name}())".format(
                name=icon_data["icon"].__name__,
            )
            tb.setToolTip(tooltip)
            hlayout.addWidget(tb)
        hlayout.addStretch()

        icons_widget = QtGui.QWidget(self)
        icons_widget.setLayout(hlayout)

        vlayout.addWidget(icons_widget)
        vlayout.addStretch()

        self.setLayout(vlayout)
