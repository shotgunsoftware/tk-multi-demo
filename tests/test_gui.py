# Copyright (c) 2019 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import pytest
import subprocess
import time
import os
import sys
import sgtk
from tk_toolchain.authentication import get_toolkit_user

try:
    from MA.UI import topwindows
    from MA.UI import first
except ImportError:
    pytestmark = pytest.mark.skip()


@pytest.fixture(scope="session")
def context():
    # Get credentials from TK_TOOLCHAIN
    sg = get_toolkit_user().create_sg_connection()

    # Get the Demo Animation project id
    filters = [["name", "is", "Demo: Animation"]]
    project = sg.find_one("Project", filters)

    return project


# This fixture will launch tk-run-app on first usage
# and will remain valid until the test run ends.
@pytest.fixture(scope="session")
def host_application(context):
    """
    Launch the host application for the Toolkit application.

    TODO: This can probably be refactored, as it is not
    likely to change between apps, except for the context.
    One way to pass in a context would be to have the repo being
    tested to define a fixture named context and this fixture
    would consume it.
    """
    process = subprocess.Popen(
        [
            "python",
            "-m",
            "tk_toolchain.cmd_line_tools.tk_run_app",
            # Allows the test for this application to be invoked from
            # another repository, namely the tk-framework-widget repo,
            # by specifying that the repo detection should start
            # at the specified location.
            "--location",
            os.path.dirname(__file__),
            "--context-entity-type",
            context["type"],
            "--context-entity-id",
            str(context["id"]),
        ]
    )
    try:
        yield
    finally:
        # We're done. Grab all the output from the process
        # and print it so that is there was an error
        # we'll know about it.
        stdout, stderr = process.communicate()
        sys.stdout.write(stdout or "")
        sys.stderr.write(stderr or "")
        process.poll()
        # If returncode is not set, then the process
        # was hung and we need to kill it
        if process.returncode is None:
            process.kill()
        else:
            assert process.returncode == 0


@pytest.fixture(scope="session")
def app_dialog(host_application):
    """
    Retrieve the application dialog and return the AppDialogAppWrapper.
    """
    before = time.time()
    while before + 30 > time.time():
        if sgtk.util.is_windows():
            app_dialog = AppDialogAppWrapper(topwindows)
        else:
            app_dialog = AppDialogAppWrapper(topwindows["python"])

        if app_dialog.exists():
            yield app_dialog
            app_dialog.close()
            return
    else:
        raise RuntimeError("Timeout waiting for the app dialog to launch.")


class AppDialogAppWrapper(object):
    """
    Wrapper around the app dialog.
    """

    def __init__(self, parent):
        """
        :param root:
        """
        self.root = parent[
            "Flow Production Tracking: Flow Production Tracking Toolkit Demos"
        ].get()

    def exists(self):
        """
        ``True`` if the widget was found, ``False`` otherwise.
        """
        return self.root.exists()

    def open_demo_pane(self, name):
        self.root["Demo Tree View"][name].get().mouseClick()

    def close(self):
        self.root.buttons["Close"].get().mouseClick()


def test_activity_stream(app_dialog):
    # Validate that Demo app is on the welcome page
    assert app_dialog.root.captions[
        "Help With this App"
    ].exists(), "Not on the Demos app Welcome Page"

    # Click on the Activity Stream widget
    app_dialog.open_demo_pane("Activity Stream")
    assert app_dialog.root.captions[
        "Activity Stream"
    ].exists(), "Not on the Activity Stream widget"

    # Wait until note creation field is showing up.
    while app_dialog.root.captions["Loading PTR Data..."].exists():
        time.sleep(1)

    # Click to create a new note
    app_dialog.root.captions["Click to create a new note..."].get().mouseClick()

    # Validate that all buttons are available
    assert app_dialog.root.buttons[
        "Cancel"
    ].exists(), "Cancel buttons is not showing up"
    assert app_dialog.root.buttons[
        "Attach Files"
    ].exists(), "Attach Screenshot buttons is not showing up"
    assert app_dialog.root.buttons[
        "Take Screenshot"
    ].exists(), "Take Screenshot buttons is not showing up"
    assert app_dialog.root.buttons[
        "Create Note"
    ].exists(), "Create Note buttons is not showing up"

    # Add a note
    app_dialog.root.textfields.typeIn("New Note")
    app_dialog.root.buttons["Create Note"].get().mouseClick()
    app_dialog.root.waitIdle(), 30
    app_dialog.root.captions["New Note"].get().waitExist(), 30

    # Validate the Note gets created
    assert app_dialog.root.captions["New Note"].exists(), "New note wasn't created"
    assert app_dialog.root.captions[
        "Reply to this Note"
    ].exists(), "New note wasn't created"

    # Scroll down in the activity stream
    activityScrollBar = first(app_dialog.root.scrollbars[1])
    width, height = activityScrollBar.size
    app_dialog.root.scrollbars[1]["Position"].get().mouseSlide()
    activityScrollBar.mouseDrag(width * 0, height * 1)
    assert app_dialog.root.buttons[
        "Click here to see the Activity stream in Flow Production Tracking."
    ].exists(), "Hyperlink to see the Activity Stream in PTR is missing"


def test_context_selector(app_dialog):
    # Click on the Context Selector widget
    app_dialog.open_demo_pane("Context Selector Widget")
    assert app_dialog.root.captions[
        "Context Selector Widget"
    ].exists(), "Not on the Context Selector Widget"

    # Validate that all selectors are available
    assert app_dialog.root.captions["Task:*"].exists(), "Task: is not available"
    assert app_dialog.root.captions[
        "*The task that the selected item will be associated with the PTR entity being acted upon.*"
    ].exists(), "Task field is not available"
    assert app_dialog.root.checkboxes[
        "*Toggle this button to allow searching for a Task to associate with the selected item*"
    ].exists(), "Task search is not available"
    assert app_dialog.root.captions["Link:*"].exists(), "Link: is not available"
    assert app_dialog.root.captions["*Demo: Animation"].exists(), "Link field isn't set"
    assert app_dialog.root.checkboxes[
        "*Toggle this button to allow searching for an entity to link to the selected item.*"
    ].exists(), "Link search is not available"
    app_dialog.root.checkboxes["Click to Toggle Editing"].get().mouseClick()
    assert app_dialog.root.captions[
        "Editing is now disabled."
    ].exists(), "Toggle to disable context switch doesn't work."
    app_dialog.root.checkboxes["Click to Toggle Editing"].get().mouseClick()
    assert app_dialog.root.captions[
        "Editing is now enabled."
    ].exists(), "Toggle to disable context switch doesn't work."

    # Change Context
    app_dialog.root.checkboxes[
        "*Toggle this button to allow searching for a Task to associate with the selected item*"
    ].get().mouseClick()
    app_dialog.root.textfields.typeIn("Art")
    topwindows.listitems["Art"].get().mouseClick()
    app_dialog.root.captions["*Art"].get().waitExist(), 30

    # Validate context Changed successfully
    assert app_dialog.root.captions["*Art"].exists(), "Task field didn't update"
    assert app_dialog.root.captions["*Acorn"].exists(), "Link field didn't update"
    assert app_dialog.root.captions[
        "Context set to: Art, Asset Acorn"
    ].exists(), "Context wasn't set correctly"


def test_auto_elide_label(app_dialog):
    # Click on the Context Selector widget
    app_dialog.open_demo_pane("Auto-Elide Label")
    assert app_dialog.root.captions[
        "Auto-Elide Label"
    ].exists(), "Not on the Auto-Elide Label Widget"

    # Validate default lable value
    assert app_dialog.root.captions[
        "Lorem ipsum dolor sit amet, consectetur adipiscing el..."
    ].exists(), "Default Auto-Elide text value is good"

    # Slide to the left side to remove the text and validate
    labelIndicator = first(app_dialog.root.buttons["Page left"])
    width, height = labelIndicator.size
    app_dialog.root.indicators.Position[1].mouseSlide()
    labelIndicator.mouseDrag(width * 0, height * 0)
    assert app_dialog.root.captions[""].exists(), "Empty Auto-Elide text value is good"

    # Slide to the right side to show all the text and validate
    labelIndicator = first(app_dialog.root.buttons["Page right"])
    width, height = labelIndicator.size
    app_dialog.root.indicators.Position[1].mouseSlide()
    labelIndicator.mouseDrag(width * 1, height * 0)
    assert app_dialog.root.captions[
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque non posuere lorem. Donec non lobortis mauris...."
    ].exists(), "Full Auto-Elide text value is good"


def test_global_search(app_dialog):
    # Click on the Global Search widget
    app_dialog.open_demo_pane("Global Search")
    assert app_dialog.root.captions[
        "Global Search"
    ].exists(), "Not on the Global Search Widget"

    # Search for a specific entity
    app_dialog.root.textfields.typeIn("Art")
    topwindows.listitems["Art"].get().mouseClick()

    # Validate search complete successfully
    assert app_dialog.root.captions[
        "Task 'Art' with id * activated"
    ].exists(), "Global search is not working"


def test_help_screen(app_dialog):
    # Click on the Help Screen Popup widget
    app_dialog.open_demo_pane("Help Screen Popup")
    assert app_dialog.root.captions[
        "Help Screen Popup"
    ].exists(), "Not on the Help Screen Popup Widget"

    # Click on the show_help_screen button
    app_dialog.root.buttons["show_help_screen()"].get().mouseClick()

    # Validate Show Help Screen
    assert app_dialog.root.dialogs[
        "Toolkit Help"
    ].exists(), "Show Help Screen is not showing up"
    assert (
        app_dialog.root.dialogs["Toolkit Help"]
        .buttons["Jump to Documentation"]
        .exists()
    ), "Jump to Documentation button is not available"
    assert (
        app_dialog.root.dialogs["Toolkit Help"].buttons["Close"].exists()
    ), "Close button is not available"

    # Click on Scroll to the next slide until you reach the last slide
    for _i in range(0, 3):
        # Make sure Scroll to the next slide button is available
        assert (
            app_dialog.root.dialogs["Toolkit Help"]
            .buttons["Scroll to the next slide"]
            .exists()
        ), "Scroll to the next slide button is not available"
        # Click on Scroll to the next slide button
        app_dialog.root.dialogs["Toolkit Help"].buttons[
            "Scroll to the next slide"
        ].get().mouseClick()

    # Validate Show Help Screen last slide
    assert app_dialog.root.dialogs[
        "Toolkit Help"
    ].exists(), "Show Help Screen is not showing up"
    assert (
        app_dialog.root.dialogs["Toolkit Help"]
        .buttons["Jump to Documentation"]
        .exists()
    ), "Jump to Documentation button is not available"
    assert (
        app_dialog.root.dialogs["Toolkit Help"].buttons["Close"].exists()
    ), "Close button is not available"
    assert (
        app_dialog.root.dialogs["Toolkit Help"]
        .buttons["Scroll to the previous slide"]
        .exists()
    ), "Scroll to the previous slide button is not available"
    assert (
        app_dialog.root.dialogs["Toolkit Help"]
        .buttons["Scroll to the next slide"]
        .exists()
        is False
    ), "Scroll to the next slide button is still available"

    # Close Show Help Screen
    app_dialog.root.dialogs["Toolkit Help"].buttons["Close"].get().mouseClick()


def test_navigation(app_dialog):
    # Click on the Navigation widget
    app_dialog.open_demo_pane("Navigation")
    assert app_dialog.root.captions[
        "Navigation"
    ].exists(), "Not on the Navigation widget"
    assert app_dialog.root.captions[
        "Select items in the tree view to the left to see the NavigationWidget and BreadcrumbWidget above update. Then use the navigation widgets themselves to traverse the selection history in the tree view. Clicking the Home button in the NavigationWidget will clear selection."
    ].exists(), "Widget's description is missing"

    # Navigate in Demo: Animation project
    app_dialog.root.outlineitems["Demo: Animation"].waitExist(), 30
    app_dialog.root.outlineitems["Demo: Animation"].get().mouseDoubleClick()

    # Validate Breadcrumb widget and that Assets and Shots entities are showing up
    assert app_dialog.root.captions[
        "Project Demo: Animation"
    ].exists(), "Breadcrumb widget is not set correctly"
    app_dialog.root.outlineitems["Assets"].waitExist(), 30
    assert app_dialog.root.outlineitems[
        "Assets"
    ].exists(), "Assets entity is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Shots"
    ].exists(), "Shots entity is not in the navigation widget"

    # Navigate in Assets entity
    app_dialog.root.outlineitems["Assets"].get().mouseDoubleClick()

    # Validate Breadcrumb widget and Assets Types
    assert app_dialog.root.captions[
        "Project Demo: Animation * Assets"
    ].exists(), "Breadcrumb widget is not set correctly"
    app_dialog.root.outlineitems["Character"].waitExist(), 30
    assert app_dialog.root.outlineitems[
        "Character"
    ].exists(), "Asset type Character is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Environment"
    ].exists(), "Asset type Environment is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Matte Painting"
    ].exists(), "Asset type Matte Painting is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Prop"
    ].exists(), "Asset type Prop is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Vehicle"
    ].exists(), "Asset type Vehicle is not in the navigation widget"

    # Navigate in Asset type Character
    app_dialog.root.outlineitems["Character"].get().mouseDoubleClick()

    # Validate Breadcrumb widget and Asset Type Characters
    assert app_dialog.root.captions[
        "Project Demo: Animation * Assets * Character"
    ].exists(), "Breadcrumb widget is not set correctly"
    app_dialog.root.outlineitems["Alice"].waitExist(), 30
    assert app_dialog.root.outlineitems[
        "Alice"
    ].exists(), "Character Alice is not in the navigation widget"

    # Select asset Alice
    app_dialog.root.outlineitems["Alice"].get().mouseClick()

    # Validate Breadcrumb widget
    assert app_dialog.root.captions[
        "Project Demo: Animation * Assets * Character * Asset Alice"
    ].exists(), "Breadcrumb widget is not set correctly"

    # Click on the back navigation button until back to the project context
    for _i in range(0, 3):
        # Click on the back navigation button
        app_dialog.root.buttons["nav_prev_btn"].mouseClick()

    # Validate Breadcrumb widget is only showing the project context
    assert app_dialog.root.captions[
        "Project Demo: Animation"
    ].exists(), "Breadcrumb widget is not set correctly"

    # Click on the forward navigation button until back to the asset hamster context
    for _i in range(0, 3):
        # Click on the back navigation button
        app_dialog.root.buttons["nav_next_btn"].mouseClick()

    # Validate Breadcrumb widget is only showing the entire context
    assert app_dialog.root.captions[
        "Project Demo: Animation * Assets * Character * Asset Alice"
    ].exists(), "Breadcrumb widget is not set correctly"

    # Click on the home button and validate breadcrumb is empty
    app_dialog.root.buttons["nav_home_btn"].mouseClick()
    assert app_dialog.root.outlineitems[
        ""
    ].exists(), "Breadcrumb should be empty after clicking on the home button"


def test_note_editor(app_dialog):
    # Click on the Note Editor widget
    app_dialog.open_demo_pane("Note Editor")
    assert app_dialog.root.captions[
        "Note Editor"
    ].exists(), "Not on the Note Editor widget"

    # Click to create a new note
    if app_dialog.root.captions["Click to create a new note..."].exists():
        app_dialog.root.captions["Click to create a new note..."].get().mouseClick()

    # Validate that all buttons are available
    assert app_dialog.root.buttons[
        "Cancel"
    ].exists(), "Cancel buttons is not showing up"
    assert app_dialog.root.buttons[
        "Attach Files"
    ].exists(), "Attach Screenshot buttons is not showing up"
    assert app_dialog.root.buttons[
        "Take Screenshot"
    ].exists(), "Take Screenshot buttons is not showing up"
    assert app_dialog.root.buttons[
        "Create Note"
    ].exists(), "Create Note buttons is not showing up"

    # Validate that the File browser is showing up after clicking on the Files to attach button then close it
    app_dialog.root.buttons["Attach Files"].get().mouseClick()
    app_dialog.root.dialogs["Select files to attach."].waitExist(), 30
    app_dialog.root.dialogs["Select files to attach."].buttons[
        "Close"
    ].get().mouseClick()

    # Validate that all buttons are available
    assert app_dialog.root.buttons["Cancel"].exists(), "Cancel button is not showing up"
    assert app_dialog.root.buttons[
        "add_button"
    ].exists(), "Add attachments button is not showing up"
    assert app_dialog.root.buttons[
        "remove_button"
    ].exists(), "Remove attachments button is not showing up"
    assert app_dialog.root.buttons[
        "Create Note"
    ].exists(), "Create Note button is not showing up"
    app_dialog.root.buttons["Cancel"].get().mouseClick()

    # Take a screenshot
    app_dialog.root.buttons["Take Screenshot"].get().mouseClick()
    MyOGL = first(app_dialog.root)
    width, height = MyOGL.size
    MyOGL.mouseSlide(width * 0, height * 0)
    MyOGL.mouseDrag(width * 1, height * 1)

    # Add a note
    app_dialog.root.textfields.typeIn("New Note")
    app_dialog.root.buttons["Create Note"].get().mouseClick()
    app_dialog.root.captions["Click to create a new note..."].waitExist(), 30


def test_overlay(app_dialog):
    # Click on the Overlay widget
    app_dialog.open_demo_pane("Overlay")
    assert app_dialog.root.captions["Overlay"].exists(), "Not on the Overlay widget"

    # Validate "When the overlay widget is hidden, you should be able to click this button" button
    app_dialog.root.buttons[
        "When the overlay widget is hidden, you should be able to click this button."
    ].get().mouseClick()
    assert app_dialog.root.captions[
        "*This is a label widget with an OverlayWidget parented to it. When shown,*"
    ].exists(), "Message isn't showing up in the overlay dialog"

    # Type in text dialog
    app_dialog.root.textfields.typeIn("This is a test")

    # Validate spinner button
    app_dialog.root.buttons["start_spin()"].get().mouseClick()
    # FIXME Need to find a way to know that spinner is showing up

    # Validate show message button
    app_dialog.root.buttons["show_message()"].get().mouseClick()
    assert app_dialog.root.captions[
        "Showing this message in the overlay widget.*"
    ].exists(), "Message isn't showing up in the overlay dialog"

    # Validate show message pixmap button
    app_dialog.root.buttons["show_message_pixmap()"].get().mouseClick()
    # FIXME Need to find a way to know that pixmap is showing up

    # Validate show error message button
    app_dialog.root.buttons["show_error_message()"].get().mouseClick()
    assert app_dialog.root.captions[
        "Showing this error message in the overlay widget.*"
    ].exists(), "Message isn't showing up in the overlay dialog"

    # Validate hide button
    app_dialog.root.buttons["hide()"].get().mouseClick()
    assert app_dialog.root.captions[
        "*This is a label widget with an OverlayWidget parented to it. When shown,*"
    ].exists(), "Message isn't showing up in the overlay dialog"

    # Validate text dialog
    assert (
        app_dialog.root.textfields.value == "This is a test"
    ), "Text field doesn't have the right value"


def test_screen_capture(app_dialog):
    # Click on the Screen Capture widget
    app_dialog.open_demo_pane("Screen Capture")
    assert app_dialog.root.captions[
        "Screen Capture"
    ].exists(), "Not on the Screen Capture widget"

    # Validate get_desktop_pixmap button
    app_dialog.root.buttons["get_desktop_pixmap(rect)"].get().mouseClick()

    # Validate screen_capture button
    app_dialog.root.buttons["screen_capture()"].get().mouseClick()
    MyOGL = first(app_dialog.root)
    width, height = MyOGL.size
    MyOGL.mouseSlide(width * 0, height * 0)
    MyOGL.mouseDrag(width * 1, height * 1)

    # Validate screen_capture_file button
    app_dialog.root.buttons["screen_capture_file()"].get().mouseClick()
    MyOGL = first(app_dialog.root)
    width, height = MyOGL.size
    MyOGL.mouseSlide(width * 0, height * 0)
    MyOGL.mouseDrag(width * 1, height * 1)
    assert app_dialog.root.captions["Output file: *"].exists(), "Output file is missing"


def test_search(app_dialog):
    # Click on the Search widget
    app_dialog.open_demo_pane("Search")
    assert app_dialog.root.captions["Search"].exists(), "Not on the Search widget"

    # Validate test dialog
    app_dialog.root.textfields.typeIn("This is a test")
    assert app_dialog.root.captions[
        "search_edited: This is a test"
    ].exists(), "Caption didn't get updated after typing in the Search widget"
    app_dialog.root.textfields.typeIn("{ENTER}")
    assert app_dialog.root.captions[
        "search_changed: This is a test"
    ].exists(), "Caption didn't get updated after clicking on the enter key in the Search widget"


def test_shotgun_field_delegate(app_dialog):
    # Click on the Shotgun Field Delegate widget
    app_dialog.open_demo_pane("Flow Production Tracking Field Delegate")
    assert app_dialog.root.captions[
        "Flow Production Tracking Field Delegate"
    ].exists(), "Not on the Flow Production Tracking Field Delegate widget"
    app_dialog.root.captions[
        "A ShotgunTableView with auto-assigned field delegates:"
    ].waitExist(), 30

    # Validate Demo: Animation is showing up
    if app_dialog.root.tables[0].cells["Demo: Animation*"].exists() is True:
        assert (
            app_dialog.root.tables[0].cells["Demo: Animation*"].exists()
        ), "Demo: Animation project not showing up in the Flow Production Tracking Field Delegate widget"
        assert (
            app_dialog.root.tables[0].cells["https://sg-media*.amazonaws.com*"].exists()
        ), "Demo: Animation project doesn't have a thumbnail"
    else:
        # Scroll down
        activityScrollBar = first(app_dialog.root.scrollbars[1])
        width, height = activityScrollBar.size
        app_dialog.root.scrollbars[1]["Position"].get().mouseSlide()
        activityScrollBar.mouseDrag(width * 0, height * 1)
        # Validate Demo: Animation is showing up
        assert (
            app_dialog.root.tables[0].cells["Demo: Animation*"].exists()
        ), "Demo: Animation project not showing up in the Flow Production Tracking Field Delegate widget"
        assert (
            app_dialog.root.tables[0].cells["https://sg-media*.amazonaws.com*"].exists()
        ), "Demo: Animation project doesn't have a thumbnail"

    # Validate scroll bar is working fine
    activityScrollBar = first(app_dialog.root.scrollbars[1])
    width, height = activityScrollBar.size
    app_dialog.root.scrollbars[1]["Position"].get().mouseSlide()
    activityScrollBar.mouseDrag(width * 0, height * 1)

    # Validate second table
    assert (
        app_dialog.root.tables[1].cells["New Project"].exists()
    ), "New Project not showing up in the Flow Production Tracking Field Delegate widget"

    # Change New Project name
    app_dialog.root.tables[1].cells["New Project"].get().mouseDoubleClick()
    app_dialog.root.tables[1].cells["New Project"].get().mouseDoubleClick()
    app_dialog.root.tables[1].cells["New Project"].typeIn(" Renamed")
    app_dialog.root.tables[1].get().mouseClick()
    assert (
        app_dialog.root.tables[1].cells["Renamed"].exists()
    ), "Project rename didn't work"

    # Validate scroll bar is working fine
    activityScrollBar = first(app_dialog.root.scrollbars[2])
    width, height = activityScrollBar.size
    app_dialog.root.scrollbars[2]["Position"].get().mouseSlide()
    activityScrollBar.mouseDrag(width * 0, height * 1)


def test_shotgun_field_widgets_form(app_dialog):
    # Click on the Shotgun Field Widgets Form widget
    app_dialog.open_demo_pane("Flow Production Tracking Field Widgets Form")
    assert app_dialog.root.captions[
        "Flow Production Tracking Field Widgets Form"
    ].exists(), "Not on the Flow Production Tracking Field Widgets Form widget"
    app_dialog.root.captions["Analytics Truth Finder Onboarded:"].waitExist(), 30

    # Validate widget interactions
    app_dialog.root.checkboxes["analytics_truth_finder_onboarded_widget"].mouseClick()
    assert app_dialog.root.captions[
        "> Analytics Truth Finder Onboarded widget value changed to: True"
    ].exists(), "Checkbox wasn't successfully checked in the Flow Production Tracking Field Widgets Form widget"

    # Validate scroll bar is working fine
    activityScrollBar = first(app_dialog.root.scrollbars[1])
    width, height = activityScrollBar.size
    app_dialog.root.scrollbars[1]["Position"].get().mouseSlide()
    activityScrollBar.mouseDrag(width * 0, height * 1)

    # Validate widget interactions
    app_dialog.root.checkboxes["welcome_page_visited_widget"].mouseClick()
    assert app_dialog.root.captions[
        "> Welcome Page Visited widget value changed to: False"
    ].exists(), "Checkbox wasn't successfully unchecked in the Flow Production Tracking Field Widgets Form widget"


def test_custom_field_widget(app_dialog):
    # Click on the Custom Field Widget widget
    app_dialog.open_demo_pane("Custom Field Widget")
    assert app_dialog.root.captions[
        "Custom Field Widget"
    ].exists(), "Not on the Custom Field Widget widget"

    # Wait until widget is showing up
    app_dialog.root.tables.waitExist(), 30

    # Validate Demo: Animation Project
    app_dialog.root.tables.rows["2"].get().mouseClick()
    assert (
        app_dialog.root.tables.rows["2"].cells["Demo: Animation"].exists()
    ), "Demo: Animation project not showing up in the PTR Field Delegate widget"
    assert (
        app_dialog.root.tables.rows["2"]
        .cells["https://sg-media*.amazonaws.com*"]
        .exists()
    ), "Demo: Animation project doesn't have a thumbnail"
    assert (
        app_dialog.root.tables.rows["2"].cells["False"].exists()
    ), "Missing Demo: Animation project Favorite column"


def test_entity_field_menu(app_dialog):
    # Click on the Entity Field Menu widget
    app_dialog.open_demo_pane("Entity Field Menu")
    assert app_dialog.root.captions[
        "Entity Field Menu"
    ].exists(), "Not on the Entity Field Menu widget"

    # Wait until widget is showing up
    app_dialog.root.captions["Click the button to show the menu."].waitExist(), 30

    # Validate entity field menu
    app_dialog.root.buttons["EntityFieldMenu (HumanUser)"].get().mouseClick()
    time.sleep(5)  # to give some time for the menu to load
    topwindows.menuitems["Id"].get().mouseClick()
    app_dialog.root.buttons["EntityFieldMenu (HumanUser)"].get().mouseClick()
    time.sleep(2)  # to give some time for the menu to load
    assert topwindows.menuitems["Id"].exists(), "Id not on the entity field menu widget"
    topwindows.menuitems["Pipeline Configurations"].get().mouseClick()


def test_shotgun_menu(app_dialog):
    # Click on the Shotgun Menu widget
    app_dialog.open_demo_pane("Flow Production Tracking Menu")
    assert app_dialog.root.captions[
        "Flow Production Tracking Menu"
    ].exists(), "Not on the Flow Production Tracking Menu widget"

    # Wait until widget is showing up
    app_dialog.root.captions["Click the button to show the menu."].waitExist(), 30

    # Validate Shotgun menu
    app_dialog.root.buttons["ShotGridMenu"].get().mouseClick()
    time.sleep(1)  # to give some time for the menu to load
    assert topwindows.menuitems[
        "Action 1"
    ].exists(), "Action 1 not on the Flow Production Tracking menu widget"
    topwindows.menuitems["Submenu"].mouseSlide()
    assert topwindows.menuitems[
        "Action 3"
    ].exists(), "Action 3 not on the Flow Production Tracking menu widget"
    topwindows.menuitems["Action 4"].mouseClick()  # to close the menu


def test_spinner(app_dialog):
    # Click on the Spinner widget
    app_dialog.open_demo_pane("Spinner")
    assert app_dialog.root.captions["Spinner"].exists(), "Not on the Spinner widget"

    # Show the spinner
    app_dialog.root.buttons["spinner.show()"].get().mouseClick()
    time.sleep(2)  # let the spinner show up
    # FIXME Need to find a way to know that spinner is showing up

    # Hide the spinner
    app_dialog.root.buttons["spinner.hide()"].get().mouseClick()
    # FIXME Need to find a way to know that spinner is hidden


def test_shotgun_entity_model(app_dialog):
    # Scroll down in the widgets panel
    activityScrollBar = first(app_dialog.root.indicators.Position)
    width, height = activityScrollBar.size
    app_dialog.root.indicators.Position.get().mouseSlide()
    activityScrollBar.mouseDrag(width * 0, height * 1)

    # Click on the Shotgun Entity Model widget
    app_dialog.open_demo_pane("Flow Production Tracking Entity Model")
    assert app_dialog.root.captions[
        "Flow Production Tracking Entity Model"
    ].exists(), "Not on the Flow Production Tracking Entity Model widget"

    # Wait until widget is showing up
    app_dialog.root.outlineitems["Demo: Animation"].waitExist(), 30

    # Click on Demo: Animation entity model
    app_dialog.root.outlineitems["Demo: Animation"].get().mouseDoubleClick()

    # Validate Asset Types are showing up
    app_dialog.root.outlineitems["Character"].waitExist(), 30
    assert app_dialog.root.outlineitems[
        "Character"
    ].exists(), (
        "Character is missing from the Flow Production Tracking Entity Model widget"
    )
    assert app_dialog.root.outlineitems[
        "Environment"
    ].exists(), (
        "Environment is missing from the Flow Production Tracking Entity Model widget"
    )
    assert app_dialog.root.outlineitems[
        "Matte Painting"
    ].exists(), "Matte Painting is missing from the Flow Production Tracking Entity Model widget"
    assert app_dialog.root.outlineitems[
        "Prop"
    ].exists(), "Prop is missing from the Flow Production Tracking Entity Model widget"
    assert app_dialog.root.outlineitems[
        "Vehicle"
    ].exists(), (
        "Vehicle is missing from the Flow Production Tracking Entity Model widget"
    )

    # Click on Character entity model
    app_dialog.root.outlineitems["Character"].get().mouseDoubleClick()

    # Validate Characters are showing up
    app_dialog.root.outlineitems["Alice"].waitExist(), 30
    assert app_dialog.root.outlineitems[
        "Alice"
    ].exists(), "Character Alice is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Anders"
    ].exists(), "Character Anders is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Blue Jay"
    ].exists(), "Character Blue Jay is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Buck"
    ].exists(), "Character Buck is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Bunny"
    ].exists(), "Character Bunny is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Caterpillar"
    ].exists(), "Character Caterpillar is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Darcy"
    ].exists(), "Character Darcy is not in the navigation widget"

    # Scroll down in the navigation tree to show more asset type characters
    activityScrollBar = first(app_dialog.root.scrollbars[1])
    width, height = activityScrollBar.size
    app_dialog.root.scrollbars[1]["Position"].get().mouseSlide()
    activityScrollBar.mouseDrag(width * 0, height * 1)

    # Continue to validate that all Characters are there
    assert app_dialog.root.outlineitems[
        "Fern"
    ].exists(), "Character Fern is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Flash"
    ].exists(), "Character Flash is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Hamster"
    ].exists(), "Character Hamster is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Jimmy"
    ].exists(), "Character Jimmy is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Jojo"
    ].exists(), "Character Jojo is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Mr Banning"
    ].exists(), "Character Mr Banning is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Mrs Banning"
    ].exists(), "Character Mrs Banning is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Queen"
    ].exists(), "Character Queen is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Scare Crow"
    ].exists(), "Character Scare Crow is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Squirrel"
    ].exists(), "Character Squirrel is not in the navigation widget"
    assert app_dialog.root.outlineitems[
        "Young Bunny"
    ].exists(), "Character Young Bunny is not in the navigation widget"


def test_shotgun_hierarchy(app_dialog):
    # Click on the Shotgun Hierarchy widget
    app_dialog.open_demo_pane("Flow Production Tracking Hierarchy")
    assert app_dialog.root.captions[
        "Flow Production Tracking Hierarchy"
    ].exists(), "Not on the Flow Production Tracking Hierarchy widget"

    # Wait until widget is showing up
    app_dialog.root.outlineitems["Demo: Animation"].waitExist(), 30

    # Click on Demo: Animation entity
    app_dialog.root.outlineitems["Demo: Animation"].get().mouseDoubleClick()
    app_dialog.root.tables.rows["1"].cells["bunny_080_0010_layout_v001"].waitExist(), 30

    # Scroll down in the navigation table to show more asset type characters
    tableScrollBar = first(app_dialog.root.scrollbars[2])
    width, height = tableScrollBar.size
    app_dialog.root.scrollbars[2]["Position"].get().mouseSlide()
    tableScrollBar.mouseDrag(width * 0, height * 1)

    # Validate last entries is available
    assert (
        app_dialog.root.tables.rows["40"].cells["bunny_080_0200_layout_v001"].exists()
    ), "Last Demo: Animation entry is missing in the Flow Production Tracking Hierarchy widget"

    # Click on Demo: Animation Shots entity
    app_dialog.root.outlineitems["Shots"].get().mouseDoubleClick()
    app_dialog.root.tables.rows["40"].cells[
        "bunny_080_0200_layout_v001"
    ].waitExist(), 30

    # Validate Shots are showing up
    app_dialog.root.outlineitems["bunny_010"].waitExist(), 30
    assert app_dialog.root.outlineitems[
        "bunny_010"
    ].exists(), (
        "bunny_010 is missing from the Flow Production Tracking Entity Model widget"
    )
    assert app_dialog.root.outlineitems[
        "bunny_080"
    ].exists(), (
        "bunny_080 is missing from the Flow Production Tracking Entity Model widget"
    )

    # Click on bunny_080 entity model
    app_dialog.root.outlineitems["bunny_080"].get().mouseDoubleClick()
    if (
        app_dialog.root.tables.rows["40"].cells["bunny_080_0200_layout_v001"].exists()
        is True
    ):
        app_dialog.root.tables.rows["40"].cells[
            "bunny_080_0200_layout_v001"
        ].waitExist(), 30
    else:
        # Scroll down
        tableScrollBar = first(app_dialog.root.scrollbars[2])
        width, height = tableScrollBar.size
        app_dialog.root.scrollbars[2]["Position"].get().mouseSlide()
        tableScrollBar.mouseDrag(width * 0, height * 1)
        # Validate bunny_080_0200_layout_v001 is showing up
        app_dialog.root.tables.rows["40"].cells[
            "bunny_080_0200_layout_v001"
        ].waitExist(), 30

    # Select shot bunny_080_0020
    app_dialog.root.outlineitems["bunny_080_0020"].get().mouseClick()
    assert (
        app_dialog.root.tables.rows["2"].cells["bunny_080_0020_layout_v002"].exists()
    ), "bunny_080_0020_layout_v002 is missing in the Flow Production Tracking Hierarchy widget"


def test_shotgun_globals(app_dialog):
    # Click on the Shotgun Globals widget
    app_dialog.open_demo_pane("Flow Production Tracking Globals")
    assert app_dialog.root.captions[
        "Flow Production Tracking Globals"
    ].exists(), "Not on the Flow Production Tracking Globals widget"

    # Wait until widget is showing up
    app_dialog.root.captions["Select an Entity type from the list:"].waitExist(), 30

    # Validate Shotgun globals first dropdown menu
    app_dialog.root.dropdowns.mouseClick()

    # Scroll up in the widgets panel and select Asset entity type
    activityScrollBar = first(topwindows.indicators.Position)
    width, height = activityScrollBar.size
    topwindows.indicators.Position.get().mouseSlide()
    activityScrollBar.mouseDrag(width * 0, height * 0)
    topwindows.listitems["Asset"].get().mouseClick()
    assert app_dialog.root.captions[
        "Asset"
    ].exists(), "Asset didn't get selected from the firts dropdown menu"
    assert app_dialog.root.captions[
        ":/tk-framework-shotgunutils/icon_Asset_dark.png"
    ].exists(), "Asset didn't get selected from the firts dropdown menu"

    # Validate Shotgun globals second dropdown menu
    app_dialog.root.dropdowns[1].mouseClick()
    topwindows.listitems["Description"].get().mouseClick()
    assert app_dialog.root.captions[
        "Description"
    ].exists(), "Description didn't get selected from the second dropdown menu"


def test_busy_dialog(app_dialog):
    # Click on the Busy Dialog widget
    app_dialog.open_demo_pane("Busy Dialog")
    assert app_dialog.root.captions[
        "Busy Dialog"
    ].exists(), "Not on the Busy Dialog widget"

    # Click on show busy button
    app_dialog.root.buttons["show_busy(title, details)"].get().mouseClick()

    # Wait until busy dialog is showing up
    app_dialog.root.topwindows["Flow Production Tracking: Toolkit is busy"].captions[
        "Example: Something is Taking a Long Time..."
    ].waitExist(), 30
    busy_dialog = app_dialog.root.topwindows[
        "Flow Production Tracking: Toolkit is busy"
    ]
    assert busy_dialog.captions[
        "Example: Something is Taking a Long Time..."
    ].exists(), "Busy dialog didn't show up"
    assert busy_dialog.captions[
        "Here is some description of why this is taking so long. Click the clear_busy() button or anywhere in this dialog to clear it."
    ].exists(), "Busy dialog didn't show up"

    # Click on clear busy button
    app_dialog.root.buttons["clear_busy()"].get().mouseClick()
    assert (
        busy_dialog.captions["Example: Something is Taking a Long Time..."].exists()
        is False
    ), "Clear dialog button didn't work"
    assert (
        busy_dialog.captions[
            "Here is some description of why this is taking so long. Click the clear_busy() button or anywhere in this dialog to clear it."
        ].exists()
        is False
    ), "Clear dialog button didn't work"

    # Click on show busy button again
    app_dialog.root.buttons["show_busy(title, details)"].get().mouseClick()

    # Wait until busy dialog is showing up
    busy_dialog.captions["Example: Something is Taking a Long Time..."].waitExist(), 30
    assert busy_dialog.captions[
        "Example: Something is Taking a Long Time..."
    ].exists(), "Busy dialog didn't show up"
    assert busy_dialog.captions[
        "Here is some description of why this is taking so long. Click the clear_busy() button or anywhere in this dialog to clear it."
    ].exists(), "Busy dialog didn't show up"

    # Clear busy dialog by clicking on it
    busy_dialog.captions[
        "Example: Something is Taking a Long Time..."
    ].get().mouseClick()
    assert (
        busy_dialog.captions["Example: Something is Taking a Long Time..."].exists()
        is False
    ), "Clear dialog button didn't work"
    assert (
        busy_dialog.captions[
            "Here is some description of why this is taking so long. Click the clear_busy() button or anywhere in this dialog to clear it."
        ].exists()
        is False
    ), "Clear dialog button didn't work"


def test_help_app(app_dialog):
    # Click on the Help With this App widget
    app_dialog.open_demo_pane("Help With this App")
    assert app_dialog.root.captions[
        "Help With this App"
    ].exists(), "Not on the Help With this App widget"
