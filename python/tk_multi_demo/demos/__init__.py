# Copyright (c) 2016 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

# import the demos to display here. They won't be added to the menu until
# they're included in the DEMO_LIST below.
from activity_stream_widget import ActivityStreamWidgetDemo
from elided_label import ElidedLabelDemo
from engine_show_busy import EngineShowBusyDemo
from entity_field_menu import EntityFieldMenuDemo
from field_widget_delegate import FieldWidgetDelegateDemo
from field_widgets_form import FieldWidgetsFormDemo
from help import HelpDemo
from help_screen_popup import HelpScreenPopupDemo
from note_input_widget import NoteInputWidgetDemo
from overlay import OverlayDemo
from screen_capture_widget import ScreenCaptureWidgetDemo
from shotgun_menu import ShotgunMenuDemo
from shotgun_hierarchy import ShotgunHierarchyDemo
from shotgun_globals import ShotgunGlobalsDemo

# the default demo to display when the app starts up.
DEMO_DEFAULT = HelpDemo

# this list defines the hierarchy of items that show up in the list of demos to
# display. each string starts a new grouping of demos. demo classes can show up
# in multiple groups. only one instance of a demo will be created however.
DEMOS_LIST = [
    "Qt Widgets Framework",
        ActivityStreamWidgetDemo,
        ElidedLabelDemo,
        # TODO: global search completer & widget
        HelpScreenPopupDemo,
        # TODO: model related classes
        # TODO: Navigation widgets
        NoteInputWidgetDemo,
        OverlayDemo,
        # TODO: Playback label widget
        ScreenCaptureWidgetDemo,
        FieldWidgetDelegateDemo,
        FieldWidgetsFormDemo,
        # TODO: more field widget demos
        EntityFieldMenuDemo,
        ShotgunMenuDemo,
        # TODO: spinner widget
        # TODO: view related classes
    "Shotgun Utils Framework",
        # TODO: SG model
        ShotgunHierarchyDemo,
        # TODO: data retriever
        # TODO: bg task manager
        # TODO: settings
        ShotgunGlobalsDemo,
    "Toolkit Core",
        EngineShowBusyDemo,
    "Other",
        HelpDemo,
]

