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

# import the shotgun model module from shotgunutils framework
shotgun_model = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "shotgun_model"
)
shotgun_model_widgets = sgtk.platform.import_framework("tk-framework-qtwidgets", "models")
HierarchicalFilteringProxyModel = shotgun_model_widgets.HierarchicalFilteringProxyModel

class SGSortFilterProxyModel(HierarchicalFilteringProxyModel):
    """
    A HierarchicalFilteringProxyModel allowing to only show tasks for the current
    user and filter on any column value.
    """

    def __init__(self, *args, **kwargs):
        """
        Instantiate a new :class:`SGSortFilterProxyModel`.
        """
        super(SGSortFilterProxyModel, self).__init__(*args, **kwargs)
        self._my_tasks_only = False
        app = sgtk.platform.current_bundle()
        context = app.context
        self._current_user = context.user
        # Allow matching on all columns
        self.setFilterKeyColumn(-1)

    def invalidate_filter(self):
        """
        Invalidate the current filter which forces it to be re-evaluated.
        """
        self._dirty_all_accepted()  # Needed to not have parents with no child
        self.invalidateFilter()

    def show_my_tasks_only(self, value):
        """
        Control the current user filter mode.
        """
        self._my_tasks_only = value
        self.invalidate_filter()

    def _is_row_accepted(self, src_row, src_parent_idx, parent_accepted):
        """
        Accept or reject the given row, depending on curret filter.

        :param src_row: The row in the source model to filter.
        :param src_parent_idx: The parent QModelIndex instance to filter.
        :param parent_accepted: ``True`` if a parent item has been accepted by the filter.
        :returns: ``True`` if this index should be accepted, otherwise ``False``.
        """
        # Ensure everything is loaded before filtering it
        # TODO: find a better way to handle this since this can cause performance
        # issues on large set of data.
        src_model = self.sourceModel()
        print(self._current_user)
        if self._my_tasks_only:
            # Get the source index for the row:

            src_idx = src_model.index(src_row, 0, src_parent_idx)
            item = src_model.itemFromIndex(src_idx)
            sg_entity = src_model.get_entity(item)
            print(sg_entity)
            if sg_entity:
                for assignee in sg_entity["task_assignees"]:
                    if(
                        assignee["type"] == self._current_user["type"]
                        and assignee["id"] == self._current_user["id"]
                    ):
                        break
                else:
                    # It will be accepted if needed when children are checked
                    return False
            else:
                return False
        if parent_accepted:
            # The parent was accepted, it means a match happened for it, don't
            # try to match anything at this level
            return True

        # Call base implementation
        return QtGui.QSortFilterProxyModel.filterAcceptsRow(
            self,
            src_row,
            src_parent_idx
        )


class ShotgunEntityModelDemo(QtGui.QWidget):
    """
    Demonstrates the use of the ``ShotgunEntityModle`` to display a hierarchy.
    """

    def __init__(self, parent=None):
        """
        Return the ``QtGui.QWidget`` instance for this demo.
        """

        super(ShotgunEntityModelDemo, self).__init__(parent)

        self._show_my_tasks_only = False

        # see if we can determine the current project. if we can, only show
        # Tasks which are attached to a Shot where the Sequence is ip.
        self._app = sgtk.platform.current_bundle()
        if self._app.context.project:
            filters = [
                ["project", "is", self._app.context.project],
                ["entity", "type_is", "Shot"],
                ["entity.Shot.sg_sequence.Sequence.sg_status_list", "is", "ip"],
            ]
        else:
            filters = []

        # construct the view and set the model
        self._entity_view = QtGui.QTreeView()
        self._entity_view.setIndentation(16)
        self._entity_view.setUniformRowHeights(True)
        self._entity_view.setSortingEnabled(True)
        self._entity_view.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self._refresh_action = QtGui.QAction("Refresh...", self._entity_view)
        self._refresh_action.triggered.connect(self._refresh)
        self._entity_view.addAction(self._refresh_action)
        self._entity_view.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        # construct an entity model then load some data.
        self._entity_model = shotgun_model.ShotgunEntityModel(
            entity_type="Task",
            filters=filters,
            hierarchy=[
                "entity.Shot.sg_sequence.Sequence.code",
                "entity.Shot.id",
            ],
            fields=[
                "entity.Shot.code", "entity.Shot.id",
                "description", "sg_status_list", "task_assignees",
                "entity.Shot.sg_sequence", "entity.Shot.sg_sequence.sg_status_list",
            ],
            parent=self,
            bg_load_thumbs=True,
            download_thumbs=True,
        )
        self._entity_model.data_refresh_fail.connect(self._refresh_ended)
        self._entity_model.data_refreshed.connect(self._refresh_ended)

        self._info_lbl = QtGui.QLabel(
            "This demo shows how to use the <tt>ShotgunEntityModel</tt> to "
            "display a hierarchy of <b>Asset</b> entities."
        )

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self._info_lbl)
        layout.addWidget(self._entity_view)

        # refresh the data to ensure it is up-to-date
        self._entity_model.async_refresh()

    def _refresh(self):
        self._info_lbl.setText("Refreshing SG data")
        self._entity_view.setModel(None)
        self._entity_model.async_refresh()

    def _refresh_ended(self):
        self._info_lbl.setText("SG Data refreshed")
        # create a proxy model to sort the model
        self._show_my_tasks_only = not self._show_my_tasks_only
        self._entity_proxy_model = SGSortFilterProxyModel(self)
        self._entity_proxy_model.show_my_tasks_only(self._show_my_tasks_only)
#        self._entity_proxy_model = QtGui.QSortFilterProxyModel(self)
        self._entity_proxy_model.setDynamicSortFilter(True)

        # set the proxy model's source to the entity model
        self._entity_proxy_model.setSourceModel(self._entity_model)

        # set the proxy model as the data source for the view
        self._entity_view.setModel(self._entity_proxy_model)

    def destroy(self):
        """
        Destroy the model as required by the API.
        """
        try:
            self._entity_model.destroy()
        except Exception as e:
            # log exception
            pass
