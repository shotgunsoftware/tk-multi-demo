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


class ShotgunHierarchyDemo(QtGui.QFrame):
    """
    Demonstrates the use of the ``ShotgunHierarchyModel`` to display a hierarchy
    as defined by project's tracking settings in Shotgun.
    """

    def __init__(self, parent):
        """
        Return the ``QtGui.QWidget`` instance for this demo.
        """

        super(ShotgunHierarchyDemo, self).__init__(parent)

        doc_lbl = QtGui.QLabel(
            "Browse the hierarchy on the left to find <tt>Version</tt> "
            "entities."
        )

        # import the views module from qtwidgets framework
        views = sgtk.platform.import_framework(
            "tk-framework-qtwidgets", "views")

        # import the shotgun fields module from qtwidgets.
        shotgun_fields = sgtk.platform.import_framework(
            "tk-framework-qtwidgets", "shotgun_fields")


        # the field manager handles retrieving widgets for shotgun field types
        fields_manager = shotgun_fields.ShotgunFieldManager(
            self,
            bg_task_manager=parent.bg_task_manager,
        )

        # construct the view and set the model
        self._hierarchy_view = views.ShotgunHierarchyView(self)

        # this view will display versions for selected entites on the left
        self._version_view = views.ShotgunTableView(fields_manager)

        # the fields manager needs time to initialize itself. once that's done,
        # the widgets can begin to be populated.
        fields_manager.initialized.connect(self._populate_ui)
        fields_manager.initialize()

        # layout the widgets for display
        browse_layout = QtGui.QHBoxLayout()
        browse_layout.addWidget(self._hierarchy_view)
        browse_layout.addWidget(self._version_view)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(doc_lbl)
        layout.addLayout(browse_layout)

    def _populate_ui(self):
        """
        Populate the UI with the data.
        """

        # import the shotgun model module from shotgunutils framework
        shotgun_model = sgtk.platform.import_framework(
            "tk-framework-shotgunutils", "shotgun_model")

        # construct a hierarchy model then load some data.
        # the "/" url means "show the hierarchies for all projects"
        # the "Version.entity" seed means build a hierarchy that leads to
        # entities that are linked via the Version.entity field.
        self._hierarchy_model = shotgun_model.SimpleShotgunHierarchyModel(self)
        self._hierarchy_model.load_data("/", "Version.entity")

        self._hierarchy_view.setModel(self._hierarchy_model)

        selection_model = self._hierarchy_view.selectionModel()
        selection_model.selectionChanged.connect(
            self._on_hierarchy_selection_changed
        )

    def _on_hierarchy_selection_changed(self, selected, deselected):
        """
        Handles selection changes in the hierarchy view.
        """

        # for this demo, we only care about the first item selected
        indexes = selected.indexes()
        if not indexes:
            return

        # get the item directly. Note: if you have a proxy model in between
        # the view and the model, you'll likely need to call `mapToSource`.
        selected_item = self._hierarchy_model.itemFromIndex(indexes[0])

