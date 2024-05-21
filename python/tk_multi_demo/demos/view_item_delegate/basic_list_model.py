# Copyright (c) 2021 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
#
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk, Inc.

from sgtk.platform.qt import QtCore, QtGui


class BasicListItemModel(QtCore.QAbstractListModel):
    """
    A subclass of the Qt QAbstractListModel (does not use QStandardItem objects). A very basic model
    with some hard coded data to highlight the capabilties of the ViewItemDelegate.
    """

    # The model roles for the delegate to use. The ViewItemRolesMixin class may be used for convenience
    # in creating these roles on the model (see the BasicShotgunModel class).
    (
        VIEW_ITEM_THUMBNAIL_ROLE,
        VIEW_ITEM_HEADER_ROLE,
        VIEW_ITEM_SUBTITLE_ROLE,
        VIEW_ITEM_TEXT_ROLE,
        VIEW_ITEM_SHORT_TEXT_ROLE,
        VIEW_ITEM_ICON_ROLE,
        VIEW_ITEM_EXPAND_ROLE,
        VIEW_ITEM_WIDTH_ROLE,  # Item width int
        VIEW_ITEM_HEIGHT_ROLE,  # Item height int
        VIEW_ITEM_LOADING_ROLE,  # Item loading state flag
        VIEW_ITEM_SEPARATOR_ROLE,  # Item has separator flag
        BUTTON_STATE_ROLE,
    ) = range(QtCore.Qt.UserRole, QtCore.Qt.UserRole + 12)

    def __init__(self, *args, **kwargs):
        """
        BasicListItemModel constructor.
        """

        super(BasicListItemModel, self).__init__(*args, **kwargs)

        # The underlying data structure. Just hard code some data to display.
        # The data structure is stored as a list, where each item in the list represents
        # an item (index) in the model. Each item is itself a list of values, where the
        # value at index i in the list may be referred to as the "column" i value.
        self._data = [
            # Item/Index 0
            [
                ":/tk_multi_demo_view_item_delegate/project_1.png",  # Column 0, thumbnail data
                "Title",  # Column 1, header text
                "Subtitle",  # Column 2, subttile text
                "This is some longer text.<br/>With multiple lines.<br/>The end.",  # Column 3, long text
                "Short txt<br/>for condensed views",  # Column 4, short text
                None,  # Column 5, icon data
                None,  # Column 6, expand state
                None,  # Column 7, width hint
                None,  # Column 8, height hint
                False,  # Column 9, loading state
                False,  # Column 10, has separator
                QtCore.Qt.Unchecked,  # Column 11, checkstate
                True,  # Column 11, button state where True is enabled and False is disabled
            ],
            # Item/Index 1
            [
                ":/tk_multi_demo_view_item_delegate/project_2.png",
                "<b><span style='font-size:14px'>HTML Formatting</span></b>",
                "<i>Italic Subtitle</i>",
                "<br/>".join(
                    [
                        "<span style='color:#18A7E3'>NOTICE</span> the icon in top-left thumbnail corner",
                        "Different icons can be shown over the thumbnail in any corner",
                        "Oh, and did you notice the HTML formatted <span style='color:#18A7E3'>text</span>?",
                        "The end.",
                    ]
                ),
                "<b>Short txt</b><br/><i>Item 2</i>",
                {
                    "top-left": QtGui.QPixmap(
                        ":/tk_multi_demo_view_item_delegate/project_1.png"
                    )
                },
                None,
                None,
                None,
                False,
                False,
                QtCore.Qt.Unchecked,
                True,
            ],
            # Item/Index 2
            [
                ":/tk_multi_demo_view_item_delegate/project_1.png",
                "<u><span style='font-size:14px'>Eliding and Clipping Text</span></u>",
                "<span style='color:rgba(240,240,240,60)'>Faded Subtitle</span>",
                "<br/>".join(
                    [
                        "This is a really really really really really really really really really really really realy realy long line that should be elided",
                        "(Did you notice my copy paste typo from above?)"
                        "A tooltip will display with the full text when any text is elided",
                        "<i>Note that eliding and clipping text are different</i>",
                        "<b>Eliding</b> text happens when a single line is too long (horizontally)",
                        "<b>Clipping</b> text happens when the number of text lines is too long (vertically)",
                        "An expand/collapse button is show when text is clipped",
                        "Check <span style='color:#18A7E3'>Auto Expand</span> option to ensure the row height fits all text",
                        "Uncheck Auto Expand option and move the slider to change the row height",
                        "The end.",
                    ]
                ),
                "<span style='color:#18A7E3'>Short txt</span><br/><span style='color:rgba(240,240,240,60)'>Item 3</span>",
                None,
                None,
                None,
                None,
                False,
                False,
                QtCore.Qt.Unchecked,
                True,
            ],
        ]

    def rowCount(self, parent=QtCore.QModelIndex()):
        """
        Override the base method.

        Returns the number of rows in the model.
        """

        return len(self._data)

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        """
        Override the base method.

        Set the data for the index and role.
        """

        if not index.isValid():
            return

        data_changed = False

        # Check if the role is "editable"
        if role in (
            self.VIEW_ITEM_EXPAND_ROLE,
            self.VIEW_ITEM_LOADING_ROLE,
            self.VIEW_ITEM_SEPARATOR_ROLE,
        ):
            if index.row() < 0 or index.row() >= len(self._data):
                return None

            row_value = self._data[index.row()]
            column = self.get_role_column(role)

            if 0 <= column < len(row_value):
                row_value[column] = value
                data_changed = True

        if data_changed:
            # Something changed, emit the sigal
            try:
                self.dataChanged.emit(index, index, [role])
            except TypeError:
                # Pyside version compaitbility
                self.dataChanged.emit(index, index)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """
        Override the base method.

        Return the data for the index and role.
        """

        if not index.isValid():
            return None

        # Roles that do not depend on the index
        if role == QtCore.Qt.BackgroundRole:
            return QtGui.QApplication.palette().midlight()

        # Ensure the index is valid with the internal model data
        if index.row() < 0 or index.row() >= len(self._data):
            return None

        # Get the model data for this index
        row_value = self._data[index.row()]

        # Get the column associated with this role to index into the data for this row.
        column = self.get_role_column(role)

        if column < 0:
            # Role is not set to a specific column, just return the data is is.
            return row_value

        if column >= len(row_value):
            # Invalid column
            return None

        # Get the speciifc data value for this role
        value = row_value[column]

        # Perform any extra logic based on the role
        if role == self.VIEW_ITEM_THUMBNAIL_ROLE:
            return QtGui.QPixmap(value)

        return value

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
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
        column = self.get_role_column(role)

        if column < 0:
            return

        if column >= len(row_value):
            return None

        # Get the speciifc data value for this role
        row_value[column] = value

        self.dataChanged.emit(index, index, [role])

    def get_role_column(self, role):
        """
        Return the index into the data structure for this role (e.g. the data for an item
        is represented as an array, this index returned will be used to index into the
        data array to get the value for this role).
        """

        # Might have been nicer to use a dictionary to map the role to the column index,
        # but this is more verbose for demonstration purposes.
        if role == self.VIEW_ITEM_THUMBNAIL_ROLE:
            return 0

        if role == self.VIEW_ITEM_HEADER_ROLE:
            return 1

        if role == self.VIEW_ITEM_SUBTITLE_ROLE:
            return 2

        if role == self.VIEW_ITEM_TEXT_ROLE:
            return 3

        if role == self.VIEW_ITEM_SHORT_TEXT_ROLE:
            return 4

        if role == self.VIEW_ITEM_ICON_ROLE:
            return 5

        if role == self.VIEW_ITEM_EXPAND_ROLE:
            return 6

        if role == self.VIEW_ITEM_WIDTH_ROLE:
            return 7

        if role == self.VIEW_ITEM_HEIGHT_ROLE:
            return 8

        if role == self.VIEW_ITEM_LOADING_ROLE:
            return 9

        if role == self.VIEW_ITEM_SEPARATOR_ROLE:
            return 10

        if role == QtCore.Qt.CheckStateRole:
            return 11

        if role == self.BUTTON_STATE_ROLE:
            return 12

        # Unsupported role
        return -1

    def toggle_data(self, index, role):
        """
        Toggle the data for the index and role (e.g. for loading and separator roles,
        this will toggle the boolean value).
        """

        indexes = []
        if index is None:
            # No index specified, toggle all indices in the model
            for row in range(self.rowCount()):
                indexes.append(self.createIndex(row, 0, None))
        else:
            indexes.append(index)

        for i in indexes:
            if not i.isValid():
                return

            if role in (self.VIEW_ITEM_LOADING_ROLE, self.VIEW_ITEM_SEPARATOR_ROLE):
                if i.row() < 0 or i.row() >= len(self._data):
                    return None

                row_value = self._data[i.row()]
                column = self.get_role_column(role)

                if 0 <= column < len(row_value):
                    cur_value = row_value[column]

                self.setData(i, not cur_value, role)
