# Copyright (c) 2020 Autodesk Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk Inc.

import sgtk
from sgtk.platform.qt import QtCore, QtGui
from .ui.shotgun_widget_demo import Ui_ShotgunWidgetDemoUI

# import the shotgun_widget module from the qtwidgets framework
shotgun_widget = sgtk.platform.import_framework(
    "tk-framework-qtwidgets", "shotgun_widget"
)

# import the shotgun_model module from shotgunutils framework
shotgun_model = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "shotgun_model"
)

shotgun_view = sgtk.platform.import_framework("tk-framework-qtwidgets", "views")

# import the shotgun_globals module from shotgunutils framework
shotgun_globals = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "shotgun_globals"
)

task_manager = sgtk.platform.import_framework(
    "tk-framework-shotgunutils", "task_manager"
)

utils = sgtk.platform.import_framework("tk-framework-qtwidgets", "utils")


class ShotgunWidgetDemo(QtGui.QWidget):
    """
    Demonstrates the use of the the ShotgunWidget classes available in the
    tk-frameworks-qtwidgets framework.
    """

    def __init__(self, parent=None):
        """
        Initialize the demo widget.
        """

        # call the base class init
        super(ShotgunWidgetDemo, self).__init__(parent)

        # create a single instance of the task manager that manages all
        # asynchronous work/tasks
        self._bg_task_manager = task_manager.BackgroundTaskManager(self, True)
        shotgun_globals.register_bg_task_manager(self._bg_task_manager)

        # setup the ui
        self.ui = Ui_ShotgunWidgetDemoUI()
        self.ui.setupUi(self)

        # setup the model
        self._sg_model = shotgun_model.SimpleShotgunModel(self, self._bg_task_manager)
        self._sg_delegate = None

        # tell the view to pull data from the model
        self.ui.view.setModel(self._sg_model)

        self.ui.view_mode_switch.clicked.connect(self._switch_view_mode)

        # finally populate the UI with some data
        self.populate_ui()

    def destroy(self):
        """
        Destructor. Ensures that all threads are properly joined before exit.
        """
        self._bg_task_manager.shut_down()

    def populate_ui(self, icon_mode=False):
        """
        Populate the UI with some data.

        :param icon_mode: If True, the view will use the icon mode. If False, it will use the list mode.
        """

        entity_type = "Project"
        fields = ["image"]

        if icon_mode:

            self.ui.view.setViewMode(QtGui.QListView.IconMode)

            # configure the way we want to display the Flow Production Tracking data
            header = "<b>{name}<b>"
            body = "{sg_description}<br> {[Created by: ]created_by.HumanUser.name}"

            # to be sure to return the required fields, collect them from the widget
            fields += utils.resolve_sg_fields(header)
            fields += utils.resolve_sg_fields(body)

            # setup a delegate which will be using the Shotgun Widget to display the information and tell him how we
            # want to setup the data
            self._sg_delegate = FolderItemDelegate(self.ui.view)
            self._sg_delegate.set_formatting(header=header, body=body, thumbnail=True)

        else:

            self.ui.view.setViewMode(QtGui.QListView.ListMode)

            # configure the way we want to display the Shotgun data
            left_corner = "<b>{name}</b>"
            right_corner = "{sg_status}"
            body = "{sg_description}<br> {[Created by: ]created_by.HumanUser.name}"

            # to be sure to return the required fields, collect them from the widget
            fields += utils.resolve_sg_fields(left_corner)
            fields += utils.resolve_sg_fields(right_corner)
            fields += utils.resolve_sg_fields(body)

            # setup a delegate which will be using the Flow Production Tracking Widget
            # to display the information and tell him how we want to setup the data
            self._sg_delegate = ListItemDelegate(self.ui.view)
            self._sg_delegate.set_formatting(
                left_corner=left_corner,
                right_corner=right_corner,
                body=body,
                thumbnail=True,
            )

        # load the data from the model
        self._sg_model.load_data(entity_type=entity_type, fields=fields)

        # hook up delegate renderer with view
        self.ui.view.setItemDelegate(self._sg_delegate)

    def _switch_view_mode(self):
        """
        Triggered when a user clicks on the button to change the view mode.
        """

        view_mode = self.ui.view.viewMode()

        if view_mode == QtGui.QListView.IconMode:
            self.ui.view_mode_switch.setText("Switch to Icon View")
            self.populate_ui(icon_mode=False)
        else:
            self.ui.view_mode_switch.setText("Switch to List View")
            self.populate_ui(icon_mode=True)


class ShotgunWidgetDelegate(shotgun_view.EditSelectedWidgetDelegate):
    """
    Base class for the widget delegate.
    """

    def __init__(self, view):
        """
        Class constructor

        :param view: The parent view for this delegate
        """
        shotgun_view.EditSelectedWidgetDelegate.__init__(self, view)

    def _on_before_selection(self, widget, model_index, style_options):
        """
        Called when the associated widget is selected. This method
        implements all the setting up and initialization of the widget
        that needs to take place prior to a user starting to interact with it.

        :param widget: The widget to operate on (created via _create_widget)
        :param model_index: The model index to operate on
        :param style_options: QT style options
        """
        # do std drawing first
        self._on_before_paint(widget, model_index, style_options)

        # indicate to the widget that it is in a selected state
        widget.set_selected(True)

    def _on_before_paint(self, widget, model_index, style_options):
        """
        Called by the base class when the associated widget should be
        painted in the view. This method should implement setting of all
        static elements (labels, pixmaps etc) but not dynamic ones (e.g. buttons)

        :param widget: The widget to operate on (created via _create_widget)
        :param model_index: The model index to operate on
        :param style_options: QT style options
        """
        icon = shotgun_model.get_sanitized_data(model_index, QtCore.Qt.DecorationRole)
        widget.set_thumbnail(icon)

        # get the shotgun data
        sg_item = shotgun_model.get_sg_data(model_index)

        # fill the content of the widget with the data of the loaded Flow Production Tracking
        # item
        widget.set_text(sg_item)

        # add an action to the widget toolbox to be able to open the Flow Production Tracking
        # Web page of the current item
        sg_url = sgtk.platform.current_bundle().shotgun.base_url
        url = "%s/page/project_overview?project_id=%d" % (sg_url, sg_item["id"])
        fn = lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))
        a = QtGui.QAction("View in Shotgun", None)
        a.triggered[()].connect(fn)

        widget.set_actions([a])


class ListItemDelegate(ShotgunWidgetDelegate):
    """
    The widget delegate used to display the widget as a list view item.
    """

    def __init__(self, view):
        """
        Class constructor

        :param view: The parent view for this delegate
        """
        self._left_corner = None
        self._right_corner = None
        self._body = None
        self._thumbnail = None

        ShotgunWidgetDelegate.__init__(self, view)

    def set_formatting(
        self, left_corner=None, right_corner=None, body=None, thumbnail=True
    ):
        """
        Format the delegate to be able to render the data at the right place

        :param left_corner:  Content to display in the top left area of the item
        :param right_corner: Content to display in the top right area of the item
        :param body:         Content to display in the main area of the item
        :param thumbnail:    If True, the widget will display a thumbnail. If False, no thumbnail will be displayed
        """
        self._left_corner = left_corner
        self._right_corner = right_corner
        self._body = body
        self._thumbnail = thumbnail

    def _create_widget(self, parent):
        """
        Widget factory as required by base class. The base class will call this
        when a widget is needed and then pass this widget in to the various callbacks.

        :param parent: Parent object for the widget
        """
        widget = shotgun_widget.ShotgunListWidget(parent)
        widget.set_formatting(
            top_left=self._left_corner,
            top_right=self._right_corner,
            body=self._body,
            thumbnail=self._thumbnail,
        )
        return widget

    def sizeHint(self, style_options, model_index):
        """
        Specify the size of the item.

        :param style_options: QT style options
        :param model_index: Model item to operate on
        """
        # ask the widget what size it takes
        return shotgun_widget.ShotgunListWidget.calculate_size()


class FolderItemDelegate(ShotgunWidgetDelegate):
    """
    The widget delegate used to display the widget as an icon view item.
    """

    def __init__(self, view):
        """
        Class constructor

        :param view: The parent view for this delegate
        """
        self._header = None
        self._body = None
        self._thumbnail = None

        ShotgunWidgetDelegate.__init__(self, view)

    def set_formatting(self, header=None, body=None, thumbnail=True):
        """
        Format the delegate to be able to render the data at the right place

        :param header:    Content to display in the header area of the item
        :param body:      Content to display in the main area of the item
        :param thumbnail: If True, the widget will display a thumbnail. If False, no thumbnail will be displayed
        """
        self._header = header
        self._body = body
        self._thumbnail = thumbnail

    def _create_widget(self, parent):
        """
        Widget factory as required by base class. The base class will call this
        when a widget is needed and then pass this widget in to the various callbacks.

        :param parent: Parent object for the widget
        """
        widget = shotgun_widget.ShotgunFolderWidget(parent)
        widget.set_formatting(
            header=self._header, body=self._body, thumbnail=self._thumbnail
        )
        widget._ui.thumbnail.setScaledContents(True)
        return widget

    def sizeHint(self, style_options, model_index):
        """
        Specify the size of the item.

        :param style_options: QT style options
        :param model_index: Model item to operate on
        """
        # ask the widget what size it takes
        return shotgun_widget.ShotgunFolderWidget.calculate_size()
