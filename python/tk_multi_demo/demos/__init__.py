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
from elided_label import ElidedLabelDemo
from entity_field_menu import EntityFieldMenuDemo
from field_widget_delegate import FieldWidgetDelegateDemo
from field_widgets_form import FieldWidgetsFormDemo
from help import HelpDemo
from overlay import OverlayDemo
from shotgun_menu import ShotgunMenuDemo
from shotgun_hierarchy import ShotgunHierarchyDemo
from shotgun_globals import ShotgunGlobalsDemo

# the default demo to display when the app starts up.
DEMO_DEFAULT = HelpDemo

# this list defines the hierarchy of items that show up in the list of demos to
# display. each string starts a new grouping of demos. demo classes can show up
# in multiple groups. only one instance of a demo will be created however.
DEMOS_LIST = [
    "Widget Demos",
        ElidedLabelDemo,
        EntityFieldMenuDemo,
        FieldWidgetDelegateDemo,
        FieldWidgetsFormDemo,
        ShotgunHierarchyDemo,
        OverlayDemo,
        ShotgunMenuDemo,
    "Utils Demo",
        ShotgunGlobalsDemo,
    "Model Demos",
        ShotgunHierarchyDemo,
        FieldWidgetDelegateDemo,

    "Help Demos",
        HelpDemo,
]

