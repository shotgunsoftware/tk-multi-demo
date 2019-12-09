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
from tk_toolchain.cmd_line_tools import tk_run_app
from MA.UI import first

try:
    from MA.UI import topwindows
except ImportError:
    pytestmark = pytest.mark.skip()


@pytest.fixture(scope="session")
def context():
    # A task in Big Buck Bunny which we're going to use
    # for the current context.
    return {"type": "Project", "id": 65}


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

        if app_dialog.exists() == True:
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
        self._root = parent["Shotgun: Shotgun Toolkit Demos"].get()

    def exists(self):
        """
        ``True`` if the widget was found, ``False`` otherwise.
        """
        return self._root.exists()

    def close(self):
        self._root.buttons["Close"].get().mouseClick()


def test_activity_stream(app_dialog):
    # Validate that Demo app is on the welcome page
    assert (
        app_dialog._root.captions["Help With this App"].exists() == True
    ), "Not on the Demos app Welcome Page"

    # Click on the Activity Stream widget
    app_dialog._root.outlineitems["Activity Stream"].get().mouseClick()
    assert (
        app_dialog._root.captions["Activity Stream"].exists() == True
    ), "Not on the Activity Stream widget"

    # Wait until note creation field is showing up.
    while app_dialog._root.captions["Loading Shotgun Data..."].exists() == True:
        sleep(1)

    # Click to create a new note
    app_dialog._root.captions["Click to create a new note..."].get().mouseClick()

    # Validate that all buttons are available
    assert (
        app_dialog._root.buttons["Cancel"].exists() == True
    ), "Cancel buttons is not showing up"
    assert (
        app_dialog._root.buttons["Attach Files"].exists() == True
    ), "Attach Screenshot buttons is not showing up"
    assert (
        app_dialog._root.buttons["Take Screenshot"].exists() == True
    ), "Take Screenshot buttons is not showing up"
    assert (
        app_dialog._root.buttons["Create Note"].exists() == True
    ), "Create Note buttons is not showing up"

    # Add a note
    app_dialog._root.textfields.typeIn("New Note")
    app_dialog._root.buttons["Create Note"].get().mouseClick()
    app_dialog._root.waitIdle(), 30
    app_dialog._root.captions["New Note"].get().waitExist(), 30

    # Validate the Note gets created
    assert (
        app_dialog._root.captions["New Note"].exists() == True
    ), "New note wasn't created"
    assert (
        app_dialog._root.captions["Reply to this Note"].exists() == True
    ), "New note wasn't created"

    # Scroll down in the activity stream
    activityScrollBar = first(app_dialog._root.scrollbars[1])
    width, height = activityScrollBar.size
    app_dialog._root.scrollbars[1]["Position"].get().mouseSlide()
    activityScrollBar.mouseDrag(width * 0, height * 1)
    assert (
        app_dialog._root.buttons[
            "Click here to see the Activity stream in Shotgun."
        ].exists()
        == True
    ), "Hyperlink to see the Activity Stream in Shotgun is missing"


def test_context_selector(app_dialog):
    # Click on the Context Selector widget
    app_dialog._root.outlineitems["Context Selector Widget"].get().mouseClick()
    assert (
        app_dialog._root.captions["Context Selector Widget"].exists() == True
    ), "Not on the Context Selector Widget"

    # Validate that all selectors are available
    if app_dialog._root.captions["Editing is now enabled."].exists() == True:
        assert (
            app_dialog._root.captions["Task:*"].exists() == True
        ), "Task: is not available"
        assert (
            app_dialog._root.captions[
                "*The task that the selected item will be associated with the Shotgun entity being acted upon.*"
            ].exists()
            == True
        ), "Task field is not available"
        assert (
            app_dialog._root.checkboxes[
                "*Toggle this button to allow searching for a Task to associate with the selected item*"
            ].exists()
            == True
        ), "Task search is not available"
        assert (
            app_dialog._root.captions["Link:*"].exists() == True
        ), "Link: is not available"
        assert (
            app_dialog._root.captions["*Big Buck Bunny"].exists() == True
        ), "Link field isn't set"
        assert (
            app_dialog._root.checkboxes[
                "*Toggle this button to allow searching for an entity to link to the selected item.*"
            ].exists()
            == True
        ), "Link search is not available"
        app_dialog._root.checkboxes["Click to Toggle Editing"].get().mouseClick()
        assert (
            app_dialog._root.captions["Editing is now disabled."].exists() == True
        ), "Toggle to disable context switch doesn't work."
        app_dialog._root.checkboxes["Click to Toggle Editing"].get().mouseClick()
        assert (
            app_dialog._root.captions["Editing is now enabled."].exists() == True
        ), "Toggle to disable context switch doesn't work."
    elif app_dialog._root.captions["Editing is now disabled."].exists() == True:
        app_dialog._root.checkboxes["Click to Toggle Editing"].get().mouseClick()
        assert (
            app_dialog._root.captions["Editing is now enabled."].exists() == True
        ), "Toggle to disable context switch doesn't work."
        assert (
            app_dialog._root.captions["Task:*"].exists() == True
        ), "Task: is not available"
        assert (
            app_dialog._root.captions[
                "*The task that the selected item will be associated with the Shotgun entity being acted upon.*"
            ].exists()
            == True
        ), "Task field is not available"
        assert (
            app_dialog._root.checkboxes[
                "*Toggle this button to allow searching for a Task to associate with the selected item*"
            ].exists()
            == True
        ), "Task search is not available"
        assert (
            app_dialog._root.captions["Link:*"].exists() == True
        ), "Link: is not available"
        assert (
            app_dialog._root.captions["*Big Buck Bunny"].exists() == True
        ), "Link field isn't set"
        assert (
            app_dialog._root.checkboxes[
                "*Toggle this button to allow searching for an entity to link to the selected item.*"
            ].exists()
            == True
        ), "Link search is not available"

    # Change Context
    app_dialog._root.checkboxes[
        "*Toggle this button to allow searching for a Task to associate with the selected item*"
    ].get().mouseClick()
    app_dialog._root.textfields.typeIn("Art")
    topwindows.listitems["Art"].get().mouseClick()
    app_dialog._root.captions["*Art"].get().waitExist(), 30

    # Validate context Changed successfully
    assert (
        app_dialog._root.captions["*Art"].exists() == True
    ), "Task field didn't update"
    assert (
        app_dialog._root.captions["*Acorn"].exists() == True
    ), "Link field didn't update"
    assert (
        app_dialog._root.captions["Context set to: Art, Asset Acorn"].exists() == True
    ), "Context wasn't set correctly"


def test_auto_elide_label(app_dialog):
    # Click on the Context Selector widget
    app_dialog._root.outlineitems["Auto-Elide Label"].get().mouseClick()
    assert (
        app_dialog._root.captions["Auto-Elide Label"].exists() == True
    ), "Not on the Auto-Elide Label Widget"

    # Validate default lable value
    assert (
        app_dialog._root.captions[
            "Lorem ipsum dolor sit amet, consectetur adipiscing el..."
        ].exists()
        == True
    ), "Default Auto-Elide text value is good"

    # Slide to the left side to remove the text and validate
    labelIndicator = first(app_dialog._root.buttons["Page left"])
    width, height = labelIndicator.size
    app_dialog._root.indicators.Position[1].mouseSlide()
    labelIndicator.mouseDrag(width * 0, height * 0)
    assert (
        app_dialog._root.captions[""].exists() == True
    ), "Empty Auto-Elide text value is good"

    # Slide to the right side to show all the text and validate
    labelIndicator = first(app_dialog._root.buttons["Page right"])
    width, height = labelIndicator.size
    app_dialog._root.indicators.Position[1].mouseSlide()
    labelIndicator.mouseDrag(width * 1, height * 0)
    assert (
        app_dialog._root.captions[
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque non posuere lorem. Donec non lobortis mauris...."
        ].exists()
        == True
    ), "Full Auto-Elide text value is good"


def test_global_search(app_dialog):
    # Click on the Global Search widget
    app_dialog._root.outlineitems["Global Search"].get().mouseClick()
    assert (
        app_dialog._root.captions["Global Search"].exists() == True
    ), "Not on the Global Search Widget"

    # Search for a specific entity
    app_dialog._root.textfields.typeIn("Art")
    topwindows.listitems["Art"].get().mouseClick()

    # Validate search complete successfully
    assert (
        app_dialog._root.captions["Task 'Art' with id 448 activated"].exists() == True
    ), "Global search is not working"


def test_help_screen(app_dialog):
    # Click on the Help Screen Popup widget
    app_dialog._root.outlineitems["Help Screen Popup"].get().mouseClick()
    assert (
        app_dialog._root.captions["Help Screen Popup"].exists() == True
    ), "Not on the Help Screen Popup Widget"

    # Click on the show_help_screen button
    app_dialog._root.buttons["show_help_screen()"].get().mouseClick()

    # Validate Show Help Screen
    assert (
        app_dialog._root.dialogs["Toolkit Help"].exists() == True
    ), "Show Help Screen is not showing up"
    assert (
        app_dialog._root.dialogs["Toolkit Help"]
        .buttons["Jump to Documentation"]
        .exists()
        == True
    ), "Jump to Documentation button is not available"
    assert (
        app_dialog._root.dialogs["Toolkit Help"].buttons["Close"].exists() == True
    ), "Close button is not available"
    assert (
        app_dialog._root.dialogs["Toolkit Help"]
        .buttons["Scroll to the next slide"]
        .exists()
        == True
    ), "Scroll to the next slide button is not available"

    # Click on Scroll to the next slide until you reach the last slide
    while (
        app_dialog._root.dialogs["Toolkit Help"]
        .buttons["Scroll to the next slide"]
        .exists()
        == True
    ):
        app_dialog._root.dialogs["Toolkit Help"].buttons[
            "Scroll to the next slide"
        ].get().mouseClick()

    # Validate Show Help Screen last slide
    assert (
        app_dialog._root.dialogs["Toolkit Help"].exists() == True
    ), "Show Help Screen is not showing up"
    assert (
        app_dialog._root.dialogs["Toolkit Help"]
        .buttons["Jump to Documentation"]
        .exists()
        == True
    ), "Jump to Documentation button is not available"
    assert (
        app_dialog._root.dialogs["Toolkit Help"].buttons["Close"].exists() == True
    ), "Close button is not available"
    assert (
        app_dialog._root.dialogs["Toolkit Help"]
        .buttons["Scroll to the previous slide"]
        .exists()
        == True
    ), "Scroll to the previous slide button is not available"

    # Close Show Help Screen
    app_dialog._root.dialogs["Toolkit Help"].buttons["Close"].get().mouseClick()


def test_navigation(app_dialog):
    # Click on the Navigation widget
    app_dialog._root.outlineitems["Navigation"].get().mouseClick()
    assert (
        app_dialog._root.captions["Navigation"].exists() == True
    ), "Not on the Navigation widget"


def test_note_editor(app_dialog):
    # Click on the Note Editor widget
    app_dialog._root.outlineitems["Note Editor"].get().mouseClick()
    assert (
        app_dialog._root.captions["Note Editor"].exists() == True
    ), "Not on the Note Editor widget"

    # Click to create a new note
    if app_dialog._root.captions["Click to create a new note..."].exists() == True:
        app_dialog._root.captions["Click to create a new note..."].get().mouseClick()

    # Validate that all buttons are available
    assert (
        app_dialog._root.buttons["Cancel"].exists() == True
    ), "Cancel buttons is not showing up"
    assert (
        app_dialog._root.buttons["Attach Files"].exists() == True
    ), "Attach Screenshot buttons is not showing up"
    assert (
        app_dialog._root.buttons["Take Screenshot"].exists() == True
    ), "Take Screenshot buttons is not showing up"
    assert (
        app_dialog._root.buttons["Create Note"].exists() == True
    ), "Create Note buttons is not showing up"

    # Add a note
    app_dialog._root.textfields.typeIn("New Note")
    app_dialog._root.buttons["Create Note"].get().mouseClick()
    app_dialog._root.captions["Click to create a new note..."].waitExist(), 30


def test_overlay(app_dialog):
    # Click on the Overlay widget
    app_dialog._root.outlineitems["Overlay"].get().mouseClick()
    assert (
        app_dialog._root.captions["Overlay"].exists() == True
    ), "Not on the Overlay widget"


def test_screen_capture(app_dialog):
    # Click on the Screen Capture widget
    app_dialog._root.outlineitems["Screen Capture"].get().mouseClick()
    assert (
        app_dialog._root.captions["Screen Capture"].exists() == True
    ), "Not on the Screen Capture widget"


def test_search(app_dialog):
    # Click on the Search widget
    app_dialog._root.outlineitems["Search"].get().mouseClick()
    assert (
        app_dialog._root.captions["Search"].exists() == True
    ), "Not on the Search widget"


def test_shotgun_field_delegate(app_dialog):
    # Click on the Shotgun Field Delegate widget
    app_dialog._root.outlineitems["Shotgun Field Delegate"].get().mouseClick()
    assert (
        app_dialog._root.captions["Shotgun Field Delegate"].exists() == True
    ), "Not on the Shotgun Field Delegate widget"


def test_shotgun_field_widgets_form(app_dialog):
    # Click on the Shotgun Field Widgets Form widget
    app_dialog._root.outlineitems["Shotgun Field Widgets Form"].get().mouseClick()
    assert (
        app_dialog._root.captions["Shotgun Field Widgets Form"].exists() == True
    ), "Not on the Shotgun Field Widgets Form widget"


def test_custom_field_widget(app_dialog):
    # Click on the Custom Field Widget widget
    app_dialog._root.outlineitems["Custom Field Widget"].get().mouseClick()
    assert (
        app_dialog._root.captions["Custom Field Widget"].exists() == True
    ), "Not on the Custom Field Widget widget"


def test_entity_field_menu(app_dialog):
    # Click on the Entity Field Menu widget
    app_dialog._root.outlineitems["Entity Field Menu"].get().mouseClick()
    assert (
        app_dialog._root.captions["Entity Field Menu"].exists() == True
    ), "Not on the Entity Field Menu widget"


def test_shotgun_menu(app_dialog):
    # Click on the Shotgun Menu widget
    app_dialog._root.outlineitems["Shotgun Menu"].get().mouseClick()
    assert (
        app_dialog._root.captions["Shotgun Menu"].exists() == True
    ), "Not on the Shotgun Menu widget"


def test_spinner(app_dialog):
    # Click on the Spinner widget
    app_dialog._root.outlineitems["Spinner"].get().mouseClick()
    assert (
        app_dialog._root.captions["Spinner"].exists() == True
    ), "Not on the Spinner widget"


def test_shotgun_entity_model(app_dialog):
    # Scroll down in the widgets panel
    activityScrollBar = first(app_dialog._root.indicators.Position)
    width, height = activityScrollBar.size
    app_dialog._root.indicators.Position.get().mouseSlide()
    activityScrollBar.mouseDrag(width * 0, height * 1)

    # Click on the Shotgun Entity Model widget
    app_dialog._root.outlineitems["Shotgun Entity Model"].get().mouseClick()
    assert (
        app_dialog._root.captions["Shotgun Entity Model"].exists() == True
    ), "Not on the Shotgun Entity Model widget"


def test_shotgun_hierarchy(app_dialog):
    # Click on the Shotgun Hierarchy widget
    app_dialog._root.outlineitems["Shotgun Hierarchy"].get().mouseClick()
    assert (
        app_dialog._root.captions["Shotgun Hierarchy"].exists() == True
    ), "Not on the Shotgun Hierarchy widget"


def test_shotgun_globals(app_dialog):
    # Click on the Shotgun Globals widget
    app_dialog._root.outlineitems["Shotgun Globals"].get().mouseClick()
    assert (
        app_dialog._root.captions["Shotgun Globals"].exists() == True
    ), "Not on the Shotgun Globals widget"


def test_busy_dialog(app_dialog):
    # Click on the Busy Dialog widget
    app_dialog._root.outlineitems["Busy Dialog"].get().mouseClick()
    assert (
        app_dialog._root.captions["Busy Dialog"].exists() == True
    ), "Not on the Busy Dialog widget"


def test_help_app(app_dialog):
    # Click on the Help With this App widget
    app_dialog._root.outlineitems["Help With this App"].get().mouseClick()
    assert (
        app_dialog._root.captions["Help With this App"].exists() == True
    ), "Not on the Help With this App widget"
