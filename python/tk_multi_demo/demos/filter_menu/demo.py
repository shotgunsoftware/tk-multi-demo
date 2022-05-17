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
from sgtk.platform.qt import QtCore, QtGui

from .ui import resources_rc

task_manager = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "task_manager"
)

shotgun_model = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "shotgun_model"
)

shotgun_globals = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "shotgun_globals"
)

shotgun_fields = sgtk.platform.import_framework(
    "tk-framework-qtwidgets", "shotgun_fields"
)

filtering = sgtk.platform.import_framework("tk-framework-qtwidgets", "filtering")
FilterMenu = filtering.FilterMenu
ShotgunFilterMenu = filtering.ShotgunFilterMenu
FilterMenuButton = filtering.FilterMenuButton
FilterItemProxyModel = filtering.FilterItemProxyModel
FilterItemTreeProxyModel = filtering.FilterItemTreeProxyModel


class FilterMenuDemo(QtGui.QWidget):
    """
    A demonstration of how the FilterMenu class works, and how to set it up with both ShotGrid
    models and plain Qt models.
    """

    def __init__(self, parent=None):
        """
        Initialize the demo widget.
        """

        super(FilterMenuDemo, self).__init__(parent)

        # Set up the SG source/proxy models and menu.
        self._bg_task_manager = task_manager.BackgroundTaskManager(self, True)
        self._sg_source_model = shotgun_model.SimpleShotgunModel(
            self, self._bg_task_manager
        )
        self._sg_proxy_model = FilterItemTreeProxyModel()
        self._sg_proxy_model.setSourceModel(self._sg_source_model)

        # Create a 'ShotGrid' specific filter menu since we are using a 'ShotGrid' model.
        self._sg_filter_menu = ShotgunFilterMenu(self)

        # Before initializing the menu, set the filter/proxy model on the menu.
        self._sg_filter_menu.set_filter_model(self._sg_proxy_model)

        # Default filter fields to show on open (these default fields can be saved/restored using
        # QSettings).
        self._sg_filter_menu.set_visible_fields(
            ["Project.name", "Project.end_date", "Project.created_by"]
        )

        # Now the menu is ready to be initialized.
        self._sg_filter_menu.initialize_menu()

        # Set up a basic model with predefined data to demonstrate how the filter menu can be used
        # with non-SG data. The filter menu set up is the same, except that the non SG specific
        # menu class is used, and a non-SG model is being used.
        basic_model_data = [
            ["one"],
            ["two"],
            ["three"],
            [
                {
                    "Field Name 1": "field name 1 value 1",
                    "Field Name 2": "field name 2 value 1",
                    "Field Name 3": "field name 3 value 1",
                }
            ],
            [
                {
                    "Field Name 1": "field name 1 value 2",
                    "Field Name 2": "field name 2 value 2",
                    "Field Name 3": "field name 3 value 2",
                }
            ],
            [
                {
                    "Number Field": 1,
                    "Bool Field": True,
                }
            ],
            [
                {
                    "Number Field": 2,
                    "Bool Field": False,
                }
            ],
            [
                {
                    "Number Field": 2,
                    "Bool Field": True,
                }
            ],
        ]
        self._basic_source_model = BasicModel()
        self._basic_source_model.set_internal_data(basic_model_data)
        self._basic_proxy_model = FilterItemProxyModel()
        self._basic_proxy_model.setSourceModel(self._basic_source_model)
        self._basic_filter_menu = FilterMenu(self)
        # Set the model item data roles used to extract the model data for filtering.
        self._basic_filter_menu.set_filter_roles([BasicModel.FILTER_DATA_ROLE])
        self._basic_filter_menu.set_filter_model(self._basic_proxy_model)
        self._basic_filter_menu.set_visible_fields(
            ["{role}.None".format(role=BasicModel.FILTER_DATA_ROLE)]
        )
        self._basic_filter_menu.initialize_menu()

        # Initialize the view to display the SG model data to filter on.
        self._view = QtGui.QTableView(self)
        self._view.horizontalHeader().setStretchLastSection(True)
        self._view.setModel(self._sg_proxy_model)

        # Initialize the filter button to display the SG filter menu.
        self._filter_menu_btn = FilterMenuButton(self)
        self._filter_menu_btn.setMenu(self._sg_filter_menu)

        # Set up a combobox for the user to toggle the SG entity data to filter on.
        # A list of entity type examples to filter on. User may also type in other entity types
        # that do not appear in this list.
        self._entity_types = ["Project", "Task", "HumanUser", "Asset", "Version"]
        self._entity_type_combo_box = QtGui.QComboBox(self)
        self._entity_type_combo_box.addItems(self._entity_types)
        self._entity_type_combo_box.setEditable(True)
        self._entity_type_combo_box.setCurrentIndex(0)
        self._entity_type_combo_box.currentIndexChanged.connect(
            self._entity_type_changed
        )

        # Create and initialize the fields manager, which is used to get the entity fields used
        # for filtering.
        self._fields_manager = shotgun_fields.ShotgunFieldManager(
            self, self._bg_task_manager
        )
        self._fields_manager.initialized.connect(self._update_ui)

        # Build the UI before initializing the fields manager so that the UI is ready once the
        # fields manager is initialized.
        self._populate_ui()
        self._fields_manager.initialize()

    def destroy(self):
        """
        Destructor. Clean up.
        """

        self._bg_task_manager.shut_down()

    def _populate_ui(self):
        """
        Build the UI. Should be called once on initialization.
        """

        model_check_box = QtGui.QCheckBox("Filter on SG Entity:", self)
        model_check_box.setToolTip(
            "Check to populate the view with ShotGrid entity data. Uncheck to populate with plain basic data."
        )
        model_check_box.setChecked(True)
        model_check_box.stateChanged.connect(self._set_model)

        top_toolbar = QtGui.QWidget(self)
        top_toolbar_layout = QtGui.QHBoxLayout(top_toolbar)
        top_toolbar_layout.addWidget(model_check_box)
        top_toolbar_layout.addWidget(self._entity_type_combo_box)
        top_toolbar_layout.addStretch()
        top_toolbar_layout.addWidget(self._filter_menu_btn)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(top_toolbar)
        layout.addWidget(self._view)
        self.setLayout(layout)

    def _update_ui(self):
        """
        Slot triggered when the fields manager is initialized. Call the `_entity_type_changed` slot to
        initialize the menu with the current entity type.
        """

        self._entity_type_changed(self._entity_type_combo_box.currentIndex())

    def _entity_type_changed(self, entity_index):
        """
        Update the UI based on the current SG entity type. Nothing to do if the model is set to the
        basic model data.
        """

        entity_type = self._entity_types[entity_index]

        # Clear the menu of the previous entity filter items.
        self._sg_filter_menu.clear_menu()

        # Get a list of fields for the entity type
        fields = shotgun_globals.get_entity_fields(entity_type)
        fields = self._fields_manager.supported_fields(entity_type, fields)

        # Load the data for the new entity type. The 'data_refreshed' signal from the SG model will
        # trigger the menu to update based on the new data.
        self._sg_source_model.load_data(
            entity_type,
            fields=fields,
            columns=fields,
            limit=20,
        )

    def _set_model(self, state):
        """
        Slot triggered on the model checkbox state changed.

        If the `_model_check_box` is checked, set up the filter menu to use SG Entity data.

        If the `_model_check_box` is unchecked, set up the filter menu to use the predefined
        basic model data.

        :param state: The checkbox state when triggered.
        :type state: int
        """

        if state == QtCore.Qt.Checked:
            self._filter_menu_btn.setMenu(self._sg_filter_menu)
            self._filter_menu_btn.update_button_checked()

            self._view.setModel(self._sg_proxy_model)
            self._entity_type_combo_box.setEnabled(True)

        else:
            self._filter_menu_btn.setMenu(self._basic_filter_menu)
            self._filter_menu_btn.update_button_checked()

            self._view.setModel(self._basic_proxy_model)
            self._entity_type_combo_box.setEnabled(False)


class BasicModel(QtCore.QAbstractListModel):
    """
    A subclass of the Qt QAbstractListModel. A very basic model to use for demonstrating other components.
    """

    # Custom role used to return data used for filtering.
    FILTER_DATA_ROLE = QtCore.Qt.UserRole

    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """

        super(BasicModel, self).__init__(*args, **kwargs)

        self._data = []

    def set_internal_data(self, data):
        """
        Set the model's internal data.
        """

        self._data = data

    def rowCount(self, parent=QtCore.QModelIndex()):
        """
        Override the base method.

        Returns the number of rows in the model.
        """

        if parent.isValid():
            return 0

        return len(self._data)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """
        Override the base method.

        Return the data for the index and role.
        """

        if not index.isValid():
            return None

        # Ensure the index is valid with the internal model data
        if index.row() < 0 or index.row() >= len(self._data):
            return None

        # Get the model data for this index
        row_value = self._data[index.row()]

        # Get the column associated with this role to index into the data for this row.
        column = index.column()

        if column < 0 or column >= len(row_value):
            # Role not mapped to a column or invalid column
            return None

        raw_data = row_value[column]

        if role == self.FILTER_DATA_ROLE:
            return raw_data

        if role == QtCore.Qt.DisplayRole:
            if isinstance(raw_data, dict):
                return ", ".join(("{}: {}".format(k, v) for k, v in raw_data.items()))

            if isinstance(raw_data, list):
                return ", ".join(raw_data)

            return row_value[column]
