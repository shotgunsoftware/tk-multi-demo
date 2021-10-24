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

logger = sgtk.platform.get_logger(__name__)

# import the shotgun model module from shotgunutils framework
shotgun_model = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "shotgun_model"
)


class ShotgunEntityModelDemo(QtGui.QWidget):
    """
    Demonstrates the use of the ``ShotgunEntityModle`` to display a hierarchy.
    """

    def __init__(self, parent=None):
        """
        Return the ``QtGui.QWidget`` instance for this demo.
        """
        # import sys
        # sys.path.append(r"/Users/ariel.calzada/Library/Application Support/JetBrains/Toolbox/apps/PyCharm-P/ch-0/212.5284.44/PyCharm.app/Contents/debug-eggs/pydevd-pycharm.egg")
        # import pydevd
        # pydevd.settrace('localhost', port=5490, stdoutToServer=True,
        #                 stderrToServer=True)

        super(ShotgunEntityModelDemo, self).__init__(parent)

        osx_f5_refresh_action = QtGui.QAction("Refresh (F5)", self)
        osx_f5_refresh_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F5))
        osx_f5_refresh_action.triggered.connect(self._refresh_data)
        self.addAction(osx_f5_refresh_action)

        # see if we can determine the current project. if we can, only show the
        # assets for this project.
        self._app = sgtk.platform.current_bundle()
        if self._app.context.project:
            filters = ["project", "is", self._app.context.project]
        else:
            filters = []

        # construct the view and set the model
        self._entity_view = QtGui.QTreeView()
        self._entity_view.setIndentation(16)
        self._entity_view.setUniformRowHeights(True)
        self._entity_view.setSortingEnabled(True)
        self._entity_view.sortByColumn(0, QtCore.Qt.AscendingOrder)

        # construct an entity model then load some data.
        # self._entity_model = shotgun_model.ShotgunEntityModel(
        #     "Asset",  # entity type
        #     [filters],  # filters
        #     ["project.Project.name", "sg_asset_type", "code"],  # hierarchy
        #     ["description", "id", "project", "sg_asset_type"],  # fields
        #     self,
        # )

        fields = [
            "code",
            "sg_status_list",
            "sg_sequence.Sequence.code",
            "tasks",
        ]
        hierarchy = [
            "sg_sequence.Sequence.code",
            "code",
            "tasks"
        ]
        self._entity_model = shotgun_model.ShotgunEntityModel(
            "Shot",  # entity type
            [filters],  # filters
            hierarchy,  # hierarchy
            fields,  # fields
            self,
        )

        # refresh the data to ensure it is up-to-date
        self._entity_model.async_refresh()

        # create a proxy model to sort the model
        self._entity_proxy_model = QtGui.QSortFilterProxyModel(self)
        self._entity_proxy_model.setDynamicSortFilter(True)

        # set the proxy model's source to the entity model
        self._entity_proxy_model.setSourceModel(self._entity_model)

        # set the proxy model as the data source for the view
        self._entity_view.setModel(self._entity_proxy_model)

        info_lbl = QtGui.QLabel(
            "This demo shows how to use the <tt>ShotgunEntityModel</tt> to "
            "display a hierarchy of <b>Asset</b> entities."
        )

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(info_lbl)
        layout.addWidget(self._entity_view)

        timer = QtCore.QTimer(parent)
        timer.timeout.connect(self._refresh_data)
        timer.start(5000)

    def _refresh_data(self):
        logger.debug("=" * 60)
        logger.debug("Refreshing data")
        logger.debug("=" * 60)
        self._entity_model.async_refresh()

    def destroy(self):
        """
        Destroy the model as required by the API.
        """
        try:
            self._entity_model.destroy()
        except Exception as e:
            # log exception
            pass
