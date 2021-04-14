# Copyright (c) 2021 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
#
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk, Inc.

import sgtk
from sgtk.platform.qt import QtCore, QtGui

from .mock_view_config_hook import MockViewConfigHook

# import the delegates module from qtwidgets framework
delegates = sgtk.platform.import_framework("tk-framework-qtwidgets", "delegates")
shotgun_model = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "shotgun_model"
)
ShotgunModel = shotgun_model.ShotgunModel


class BasicShotgunModel(ShotgunModel, delegates.ViewItemRolesMixin):
    """
    A subclass of the ShotgunModel to handle basic Shotgun data.
    """

    # Custom user roles are key to using the ViewItemDelegate with the data model. The delegates.ViewItemRolesMixin
    # class will take care of defining a role for each role that the ViewItemDelegate exposes to allow for data
    # and/or style customization.
    #
    # Here we will just define a base role, which is the offset to our model's custom roles. Add 100 to the first
    # available custom user role, to allow the base ShotgunModel to use (it shouldn't use more than 100, but if it
    # did, we would need to bump this number up.. or ideally the ShotgunModel would tell us what is the last role
    # it uses).
    #
    # We will also define the next available role, to pass to the ViewItemRolesMixin class to start adding new roles,
    # without overwriting any roles in use. Any new custom roles specific to this model should be added before the
    # 'NEXT_AVAILABLE_ROLE' (e.g. the NEXT_AVAILABLE_ROLE shoudl always be the last role in the enum list).
    _BASE_ROLE = QtCore.Qt.UserRole + 100
    (
        NEXT_AVAILABLE_ROLE,  # Keep track of the next available custome role. Insert new roles above.
    ) = range(_BASE_ROLE, _BASE_ROLE + 1)

    def __init__(
        self, entity_type, filters, fields, sort_field, bg_task_manager, parent
    ):
        """
        BasicShotgunModel constructor.

        :param entity_type: The entity type that should be loaded into this model.
        :param parent: QT parent object
        :param bg_task_manager: The background task manager to handle loading data.
        """

        # Initialize the base class
        ShotgunModel.__init__(
            self,
            parent,
            download_thumbs=True,
            bg_load_thumbs=True,
            bg_task_manager=bg_task_manager,
        )

        # Shotgun data query fields
        self._entity_type = entity_type
        self._fields = fields
        self._filters = filters
        self._sort_field = sort_field
        # UI fields
        self._is_loading = False
        self._show_separator = False

        # Initialize the model data roles that the ViewITemDelegate will use to determine how to render
        # items in the model
        self.NEXT_AVAILABLE_ROLE = self.initialize_roles(self.NEXT_AVAILABLE_ROLE)

        # Create a mapping of model data roles to the method that will be called to retrieve the data
        # for the item. Notice these roles do not appear in this model class, that's because they are
        # of the roles that the ViewItemMixinClass created on calling 'initialize_roles'.
        #
        # These role methods must accept a single parameters: (1) a QStandardItem. See the
        # ViewItemRolesMixin method 'set_data_for_role' for more details # on how the role methods
        # will be called.
        self.role_methods = {
            self.VIEW_ITEM_THUMBNAIL_ROLE: MockViewConfigHook._get_item_thumbnail,
            self.VIEW_ITEM_HEADER_ROLE: MockViewConfigHook._get_item_header,
            self.VIEW_ITEM_SUBTITLE_ROLE: MockViewConfigHook._get_item_subtitle,
            self.VIEW_ITEM_TEXT_ROLE: MockViewConfigHook._get_item_text,
            self.VIEW_ITEM_SHORT_TEXT_ROLE: MockViewConfigHook._get_item_short_text,
            self.VIEW_ITEM_LOADING_ROLE: lambda item: self._is_loading,
            self.VIEW_ITEM_SEPARATOR_ROLE: lambda item: self._show_separator,
        }

    @classmethod
    def create_task_model(cls, task_manager, parent):
        """
        Factory (and mostly a convenience) method to create a Shotgun model with Task data.
        """

        app = sgtk.platform.current_bundle()

        entity_type = "Task"
        sort_field = "updated_at"
        fields = [
            "id",
            "type",
            "name",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
            "task_assignees",
            "sg_status_list",
            "description",
            "project",
            "code",
            "content",
            "entity",
        ]
        filters = [["sg_status_list", "is_not", "fin"]]
        if app.context.user:
            filters.append(["task_assignees", "in", [app.context.user]])

        return BasicShotgunModel(
            entity_type, filters, fields, sort_field, task_manager, parent
        )

    def load_data(self):
        """
        The standard method to call the base ShotgunModel '_load_data' method to retrieve the model data.
        """

        hierarchy = [self._sort_field]

        ShotgunModel._load_data(
            self,
            self._entity_type,
            self._filters,
            hierarchy,
            self._fields,
            [{"field_name": self._sort_field, "direction": "desc"}],
            limit=50,
        )

        self._refresh_data()

    def _populate_item(self, item, sg_data):
        """
        Whenever an item is constructed, this methods is called. It allows subclasses to intercept
        the construction of a QStandardItem and add additional metadata or make other changes
        that may be useful. Nothing needs to be returned.

        :param item: QStandardItem that is about to be added to the model. This has been primed
                     with the standard settings that the ShotgunModel handles.
        :param sg_data: Shotgun data dictionary that was received from Shotgun given the fields
                        and other settings specified in load_data()
        """

        # For model that subclass the QStandardItemModel class (e.g. use QStandardItem objects), use
        # the convenience method 'set_data_for_role' to set the method for each role defined in
        # 'self.role_methods' -- which in turn will call the role method when item data for that
        # role is request (e.g. item.data(ROLE) will call the method defined for ROLE).
        self.set_data_for_role_methods(item)

        item.setData(self.VIEW_ITEM_LOADING_ROLE, False)
        item.setData(self.VIEW_ITEM_SEPARATOR_ROLE, False)

    def toggle_data(self, index, role):
        """
        Toggle the loading or separator data. These will alter how the model item is displayed.
        """

        if role == self.VIEW_ITEM_LOADING_ROLE:
            self._is_loading = not self._is_loading

        elif role == self.VIEW_ITEM_SEPARATOR_ROLE:
            self._show_separator = not self._show_separator
