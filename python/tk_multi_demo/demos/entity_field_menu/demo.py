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

# import the shotgun_menus module from the framework
shotgun_menus = sgtk.platform.import_framework(
    "tk-framework-qtwidgets", "shotgun_menus")

# import the shotgun_fields module from the framework
shotgun_fields = sgtk.platform.import_framework(
    "tk-framework-qtwidgets", "shotgun_fields")


class EntityFieldMenuDemo(QtGui.QWidget):
    """
    Demonstrates the use of the the EntityFieldMenu class available in the
    tk-frameworks-qtwidgets framework.
    """

    def __init__(self, parent):
        """
        Initialize the demo widget.
        """

        # call the base class init
        super(EntityFieldMenuDemo, self).__init__(parent)

        # --- build an entity field menu

        # the fields manager is used to query which fields are supported
        # for display. it can also be used to find out which fields are
        # visible to the user and editable by the user
        fields_manager = shotgun_fields.ShotgunFieldManager(self)
        fields_manager.initialize()

        # build a menu to display Project entity fields
        entity_type = "Project"
        entity_field_menu = shotgun_menus.EntityFieldMenu(
            entity_type,
            self,
            parent.bg_task_manager,
        )

        # ---- define a few simple filter methods for use by the menu

        def field_filter(field):
            # display fields that are displayable by the shotgun field widgets
            return bool(fields_manager.supported_fields(entity_type, [field]))

        def checked_filter(field):
            # none of the fields are checked
            return False

        def disabled_filter(field):
            # none of the fields are disabled
            return False

        # attach our filters
        entity_field_menu.set_field_filter(field_filter)
        entity_field_menu.set_checked_filter(checked_filter)
        entity_field_menu.set_disabled_filter(disabled_filter)

        # a button to trigger the menu
        entity_field_menu_button = QtGui.QPushButton(
            "EntityFieldMenu (%s)" % (entity_type,))
        entity_field_menu_button.setObjectName("entity_field_menu_button")

        # show the menu when the button is clicked
        entity_field_menu_button.clicked.connect(
            lambda: entity_field_menu.exec_(QtGui.QCursor.pos())
        )

        # help label for the UI
        doc = QtGui.QLabel("Click the button to show the menu.")
        doc.setAlignment(QtCore.Qt.AlignCenter)

        # lay out the widgets
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(doc)
        layout.addSpacing(8)
        layout.addWidget(entity_field_menu_button)
        layout.addStretch()

        layout.setAlignment(entity_field_menu_button, QtCore.Qt.AlignCenter)
