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

from .ui import resources_rc  # noqa

from .basic_list_model import BasicListItemModel
from .basic_shotgun_model import BasicShotgunModel

# import the delegates module from qtwidgets framework
delegates = sgtk.platform.import_framework("tk-framework-qtwidgets", "delegates")
ThumbnailViewItemDelegate = delegates.ThumbnailViewItemDelegate
ViewItemDelegate = delegates.ViewItemDelegate

# import the task_manager and shotgun_model modules from shotgunutils framework
task_manager = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "task_manager"
)

shotgun_globals = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "shotgun_globals"
)


class ViewItemDelegateDemo(QtGui.QWidget):
    """
    A demonstration of the ViewItemDelegate class that can be used along side any view and model, to render
    the model items in the view.

    See how to create and set up the ViewItemDelegaet object in `_create_delegate` method.

    See how to use the ViewItemRolesMixin class to faciliate setting up the model item data roles in
    the basic_shotgun_model.py file.
    """

    def __init__(self, parent=None):
        """
        Initialize the widget.
        """

        super(ViewItemDelegateDemo, self).__init__(parent)

        self._bg_task_manager = task_manager.BackgroundTaskManager(self, True)
        shotgun_globals.register_bg_task_manager(self._bg_task_manager)

        # Create two separate models to demonstrate how each type can be used with the ViewItemDelegate
        #
        # The BasicListItemModel is a QAbstractItemModel (e.g. does not use QStandardItems)
        self._basic_model = BasicListItemModel(self)
        # The BasicShotgunModel is a subclass of the ShotgunModel, whichh is a QStandardItemModel (e.g.
        # uses QStandardItem objects)
        self._shotgun_model = BasicShotgunModel.create_task_model(
            self._bg_task_manager, self
        )

        # Create and a single view to display the both the BasicListModel and BasicShotgunModel data
        self._view = QtGui.QListView(self)
        # Enable mouse tracking for the delegate to receive mouse events
        self._view.setMouseTracking(True)
        # Put the onus on the delegate to determin view item sizes
        self._view.setUniformItemSizes(False)

        # Create four delegates to render the view using the BasicListModel and BasicShotgunModel, and
        # in both List and Thumbnail view modes
        self._list_view_delegate = self._create_delegate(self._view, BasicListItemModel)
        self._thumbnail_view_delegate = self._create_delegate(
            self._view, BasicListItemModel, thumbnail_mode=True
        )
        self._shotgun_list_view_delegate = self._create_delegate(
            self._view, BasicShotgunModel
        )
        self._shotgun_thumbnail_view_delegate = self._create_delegate(
            self._view, BasicShotgunModel, thumbnail_mode=True
        )

        # Add border specifically to shotgun data thumbnail view
        background_pen = QtGui.QPen(QtCore.Qt.black)
        background_pen.setWidthF(0.5)
        self._shotgun_thumbnail_view_delegate.background_pen = background_pen

        # Build and layout the UI.
        self._populate_ui()

    def _create_delegate(self, view, model_class, thumbnail_mode=False):
        """
        Create and return a ViewItemDelegate object. The data roles from the given 'model_class' will
        be used to set up the delegate.
        """

        if thumbnail_mode:
            # Create and set up the delegate to display items in a thumbnail mode
            delegate = ThumbnailViewItemDelegate(view)
            delegate.item_padding = 4

            # Set the model data roles for the delegate to use to render the model items in the view
            delegate.thumbnail_role = model_class.VIEW_ITEM_THUMBNAIL_ROLE
            delegate.short_text_role = model_class.VIEW_ITEM_SHORT_TEXT_ROLE
            delegate.expand_role = model_class.VIEW_ITEM_EXPAND_ROLE

            # Add a menu button action to display an actions menu
            delegate.add_actions(
                [
                    {
                        "icon": QtGui.QIcon(
                            ":/tk_multi_demo_view_item_delegate/down_arrow.png"
                        ),
                        "padding": 2,
                        "callback": self._action_cb,
                    },
                ],
                ViewItemDelegate.TOP_RIGHT,
            )

        else:
            # Create and set up the delegate to display items in a list mode
            delegate = ViewItemDelegate(view)
            delegate.item_padding = ViewItemDelegate.Padding(4, 8, 4, 8)

            # Set the model data roles for the delegate to use to render the model items in the view
            # NOTE that we added these custom model item data roles to both our models. You can use
            # the ViewItemRolesMixin class to facilitate setting these roles up on your model (see
            # the BasicShotgunModel).
            delegate.thumbnail_role = model_class.VIEW_ITEM_THUMBNAIL_ROLE
            delegate.header_role = model_class.VIEW_ITEM_HEADER_ROLE
            delegate.subtitle_role = model_class.VIEW_ITEM_SUBTITLE_ROLE
            delegate.text_role = model_class.VIEW_ITEM_TEXT_ROLE
            delegate.icon_role = model_class.VIEW_ITEM_ICON_ROLE
            delegate.expand_role = model_class.VIEW_ITEM_EXPAND_ROLE
            delegate.loading_role = model_class.VIEW_ITEM_LOADING_ROLE
            delegate.separator_role = model_class.VIEW_ITEM_SEPARATOR_ROLE

            # Add a button action that will display a message box
            delegate.add_actions(
                [{"name": "Menu", "padding": 2, "callback": self._show_menu}],
                ViewItemDelegate.TOP_RIGHT,
            )

        # Add some padding around the item rect
        delegate.thumbnail_padding = 7

        return delegate

    def _populate_ui(self):
        """
        Build the UI.
        """

        # Button options to change the view model data
        self._basic_model_button = QtGui.QPushButton("Basic Model", self)
        self._basic_model_button.setCheckable(True)
        self._basic_model_button.setFlat(True)
        self._basic_model_button.clicked.connect(self._toggle_view_model)
        self._shotgun_model_button = QtGui.QPushButton("ShotGrid Model", self)
        self._shotgun_model_button.setCheckable(True)
        self._shotgun_model_button.setFlat(True)
        self._shotgun_model_button.clicked.connect(self._toggle_view_model)

        # Button options to change the view mode
        self._list_view_button = QtGui.QPushButton("List View", self)
        self._list_view_button.clicked.connect(self._toggle_view_mode)
        self._list_view_button.setCheckable(True)
        self._list_view_button.setFlat(True)
        self._thumbnail_view_button = QtGui.QPushButton("Thumbnail View", self)
        self._thumbnail_view_button.clicked.connect(self._toggle_view_mode)
        self._thumbnail_view_button.setCheckable(True)
        self._thumbnail_view_button.setFlat(True)

        # Create a slider to dynamically change the view item row height
        self._size_slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self._size_slider.setToolTip(
            "Slider will change row height. This is disabled when the expand checkbox is checked."
        )
        self._size_slider.setMinimum(35)
        self._size_slider.setMaximum(300)
        self._size_slider.valueChanged.connect(self._item_size_change)
        self._size_slider.setValue(75)

        # Create a checkbox option to set the view to expand to fit all text
        size_cb = QtGui.QCheckBox("Expand Row to Fit Text", self)
        size_cb.setToolTip(
            "Expand the row height to fit all text. Checking this will disable the slider."
        )
        size_cb.stateChanged.connect(self._expand_row_height_to_text_changed)
        size_cb.setCheckState(QtCore.Qt.Checked)

        # Set up the top toolbar
        top_toolbar = QtGui.QWidget(self)
        top_toolbar_layout = QtGui.QHBoxLayout(self)
        top_toolbar_layout.addWidget(self._basic_model_button)
        top_toolbar_layout.addWidget(self._shotgun_model_button)
        top_toolbar_layout.addStretch()
        top_toolbar_layout.addWidget(self._list_view_button)
        top_toolbar_layout.addWidget(self._thumbnail_view_button)
        top_toolbar.setLayout(top_toolbar_layout)

        # Set up the bottom toolbar
        bottom_toolbar = QtGui.QWidget(self)
        bottom_toolbar_layout = QtGui.QHBoxLayout(self)
        bottom_toolbar_layout.addWidget(size_cb)
        bottom_toolbar_layout.addWidget(self._size_slider)
        bottom_toolbar.setLayout(bottom_toolbar_layout)

        # Finally layout the main widget
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(top_toolbar)
        layout.addWidget(self._view)
        layout.addWidget(bottom_toolbar)
        self.setLayout(layout)

        # Start with the displaying the BasicListModel in List mode
        self._basic_model_button.click()
        self._list_view_button.click()

    def destroy(self):
        """
        Destructor. Clean up.
        """

        shotgun_globals.unregister_bg_task_manager(self._bg_task_manager)

        try:
            # shut down main threadpool
            self._bg_task_manager.shut_down()
        except Exception:
            logger.exception("Error running closeEvent()")


    ######################################################################################################
    # ViewItemDelegate action callbacks. These methods are triggered by the ViewItemDelegaet when an
    # item's action is triggered (e.g. clicked)

    def _show_menu(self, view, index, pos):
        """
        Callback triggered from the ViewItemDelegate when Menu Button action is triggered.

        Create and show the actions menu.
        """

        menu = QtGui.QMenu(self)

        if isinstance(index.model(), BasicListItemModel):
            # NOTE: ShotgunDemoModel is not set up to handle setting loading state and separator data per item,
            # but it could be extended to achieve this functionality

            # Toggle showing loading indicator for this index
            toggle_loading_action = QtGui.QAction("Toggle Loading", self)
            toggle_loading_action.triggered.connect(
                lambda: index.model().toggle_data(
                    index, index.model().VIEW_ITEM_LOADING_ROLE
                )
            )
            # Toggle showing separator for this index
            toggle_separator_action = QtGui.QAction("Toggle Separator", self)
            toggle_separator_action.triggered.connect(
                lambda: index.model().toggle_data(
                    index, index.model().VIEW_ITEM_SEPARATOR_ROLE
                )
            )
            menu.addActions([toggle_loading_action, toggle_separator_action])

        # Non-index specific actions
        # Toggle showing loading indactors for all items
        toggle_all_loading_action = QtGui.QAction("Toggle All Loading", self)
        toggle_all_loading_action.triggered.connect(
            lambda: index.model().toggle_data(
                None, index.model().VIEW_ITEM_LOADING_ROLE
            )
        )
        # Toggle showing separators for all items
        toggle_all_separator_action = QtGui.QAction("Toggle All Separators", self)
        toggle_all_separator_action.triggered.connect(
            lambda: index.model().toggle_data(
                None, index.model().VIEW_ITEM_SEPARATOR_ROLE
            )
        )
        menu.addActions([toggle_all_loading_action, toggle_all_separator_action])

        # Show the menu at the given position relative to the view widget
        menu_pos = view.mapToGlobal(pos)
        menu.exec_(menu_pos)

    def _action_cb(self, view, index, pos):
        """
        Callback triggered from the ViewItemDelegate when the Thumbnail action is triggered.

        Show a message dialog with some information about actions in the ViewItemDelegate.
        """

        QtGui.QMessageBox.information(
            self,
            "Action button callback",
            (
                "Action executed for index({row},{col})!\n\n"
                "Notice that this action button executes a different callback than the List View action menu button. "
                "Each action button can have their own callback method to execute sepcifically for the action and current index."
            ).format(row=index.row(), col=index.column()),
        )

    ######################################################################################################
    # UI/Widget callbacks

    def _expand_row_height_to_text_changed(self, state):
        """
        Callback triggered by the checkbox to signal the ViewItemDelegate to expand each row to fit all
        item text (vertically).
        """

        if state == QtCore.Qt.Checked:
            # Expand item row height to see all text.

            # Disable the size slider to change the row height.
            self._size_slider.setEnabled(False)

            # Set the delegate item height to None to indicate expand to full text. Fix the thumbnail
            # width to ensure text aligns between item rows.
            self._list_view_delegate.item_height = None
            self._list_view_delegate.thumbnail_width = 80
            self._shotgun_list_view_delegate.item_height = None
            self._shotgun_list_view_delegate.thumbnail_width = 80

            self._view.setIconSize(QtCore.QSize())

            # Update the viewport
            self._view.viewport().update()

        elif state == QtCore.Qt.Unchecked:
            # Do not expand row height to full text, let the slider change the height.

            # Enable the size slider to change the row height.
            self._size_slider.setEnabled(True)
            # Call the method to update the item row height from the slider's current value.
            self._item_size_change(self._size_slider.value())

        else:
            raise AssertionError("QCheckBox state '{}' not supported".format(state))

    def _item_size_change(self, value):
        """
        The slide value changed to update the view item size.
        """

        icon_size = QtCore.QSize(value, value)
        self._view.setIconSize(icon_size)
        # Set the thumbnail size for Thumbnail delegates
        self._thumbnail_view_delegate.thumbnail_size = icon_size
        self._shotgun_thumbnail_view_delegate.thumbnail_size = icon_size

        # Set the item height for non-Thumbnail delegates
        self._list_view_delegate.item_height = value
        self._shotgun_list_view_delegate.item_height = value

        # Update the viewport
        self._view.viewport().update()

    def _toggle_view_model(self):
        """
        Set the view model based on the view model button clicked.
        """

        is_list_mode = self._list_view_button.isChecked()

        if self.sender() == self._basic_model_button:
            # BasicListModel

            # Set the model on the view to change the data
            self._view.setModel(self._basic_model)
            self._basic_model_button.setChecked(True)
            self._shotgun_model_button.setChecked(False)

            # Set the delegate corresponding to the current view mode and model
            if is_list_mode:
                self._view.setItemDelegate(self._list_view_delegate)
            else:
                self._view.setItemDelegate(self._thumbnail_view_delegate)

        elif self.sender() == self._shotgun_model_button:
            # BasicShotgunModel

            # Set the model on the view to change the data
            self._view.setModel(self._shotgun_model)
            self._shotgun_model_button.setChecked(True)
            self._basic_model_button.setChecked(False)

            # Set the delegate corresponding to the current view mode and model
            if is_list_mode:
                self._view.setItemDelegate(self._shotgun_list_view_delegate)
            else:
                self._view.setItemDelegate(self._shotgun_thumbnail_view_delegate)

            self._shotgun_model.load_data()

        else:
            raise AssertionError("Unsupported view model option")

    def _toggle_view_mode(self):
        """
        Set the view item delegate based on the view mode button clicked.
        """

        if self.sender() == self._list_view_button:
            # List view

            self._view.setViewMode(QtGui.QListView.ListMode)
            self._list_view_button.setChecked(True)
            self._thumbnail_view_button.setChecked(False)

            # Set the delegate to render the list mode
            if isinstance(self._view.model(), BasicListItemModel):
                self._view.setItemDelegate(self._list_view_delegate)
            elif isinstance(self._view.model(), BasicShotgunModel):
                self._view.setItemDelegate(self._shotgun_list_view_delegate)
            else:
                raise AssertionError("Unsupported model class")

        elif self.sender() == self._thumbnail_view_button:
            # Thumbnail mode

            self._view.setViewMode(QtGui.QListView.IconMode)
            self._thumbnail_view_button.setChecked(True)
            self._list_view_button.setChecked(False)

            # Set the delegate to render the thumbnail mode
            if isinstance(self._view.model(), BasicListItemModel):
                self._view.setItemDelegate(self._thumbnail_view_delegate)
            elif isinstance(self._view.model(), BasicShotgunModel):
                self._view.setItemDelegate(self._shotgun_thumbnail_view_delegate)
            else:
                raise AssertionError("Unsupported model class")

        else:
            raise AssertionError("Unsupported view mode option")
