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
from sgtk.platform.qt import QtGui

# import the global_search_widget module from the qtwidgets framework
shotgun_search_widget = sgtk.platform.import_framework(
    "tk-framework-qtwidgets", "shotgun_search_widget")

# import the task manager from shotgunutils framework
task_manager = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "task_manager")


class HierarchicalSearchWidgetDemo(QtGui.QWidget):
    """
    Demonstrates the use of the the GlobalSearchWidget class available in the
    tk-frameworks-qtwidgets framework.
    """

    def __init__(self, parent=None):
        """
        Initialize the demo widget.
        """

        # call the base class init
        super(HierarchicalSearchWidgetDemo, self).__init__(parent)

        # create a bg task manager for pulling data from SG
        self._bg_task_manager = task_manager.BackgroundTaskManager(self)

        # create the widget
        self._search_widget = shotgun_search_widget.HierarchicalSearchWidget(self)

        # give the search widget a handle on the task manager
        self._search_widget.set_bg_task_manager(self._bg_task_manager)

        checkbox = QtGui.QCheckBox("Search in current project only")
        checkbox.setChecked(True)
        checkbox.toggled.connect(self._on_checkbox_clicked)

        # display some instructions
        info_lbl = QtGui.QLabel(
            "Click in the widget and type to search for Shotgun entities. You "
            "will need to type at least 3 characters before the search begins."
        )

        # create a label to show when an entity is activated
        self._activated_label = QtGui.QLabel()
        self._activated_label.setWordWrap(True)
        self._activated_label.setStyleSheet(
            """
            QLabel {
                color: #18A7E3;
            }
            """
        )

        # lay out the UI
        layout = QtGui.QVBoxLayout(self)
        layout.setSpacing(16)
        layout.addStretch()
        layout.addWidget(info_lbl)
        layout.addWidget(checkbox)
        layout.addWidget(self._search_widget)
        layout.addWidget(self._activated_label)
        layout.addStretch()

        # connect the entity activated singal
        self._search_widget.node_activated.connect(self._on_node_activated)

    def destroy(self):
        """
        Clean up the object when deleted.
        """
        self._bg_task_manager.shut_down()

    def _on_node_activated(self, entity_type, entity_id, name, path_label, incremental_path):
        """
        Handle node activated.
        """
        print entity_type, entity_id, name, path_label, incremental_path
        if entity_type and entity_id:
            self._activated_label.setText(
                "<strong>%s</strong> '%s' with id <tt>%s</tt> at '%s' activated" % (
                    entity_type, name, entity_id, path_label)
            )
        else:
            self._activated_label.setText(
                "<strong>Folder</strong> '%s' activated" % (name,)
            )

    def _on_checkbox_clicked(self, is_checked):
        """
        Toggles the search from site level to project level searches.
        """
        if is_checked:
            self._search_widget.set_search_root(sgtk.platform.current_bundle().context.project)
        else:
            self._search_widget.set_search_root(None)
