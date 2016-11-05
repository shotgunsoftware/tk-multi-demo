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


class FrameworkDemos(sgtk.platform.Application):
    """
    Demo and QA Toolkit app building blocks.
    """

    def init_app(self):
        """
        Initialize the app.
        """

        payload = self.import_module("tk_multi_demo")

        # define a callback method to show the dialog
        def callback():
            payload.dialog.show_dialog(self)

        self.engine.register_command(
            "Toolkit Building Block Demos",
            callback,
            {"short_name": "demos"}
        )
