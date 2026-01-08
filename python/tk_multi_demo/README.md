[![Supported VFX Platform: CY2022 - CY2026](https://img.shields.io/badge/VFX_Reference_Platform-CY2022_|_CY2023_|_CY2024_|_CY2025_|_CY2026-blue)](http://www.vfxplatform.com/ "Supported VFX Reference Platform versions")
[![Supported Python versions: 3.9, 3.10, 3.11, 3.13](https://img.shields.io/badge/Python-3.9_|_3.10_|_3.11_|_3.13-blue?logo=python&logoColor=f5f5f5)](https://www.python.org/ "Supported Python versions")

[![Build Status](https://dev.azure.com/shotgun-ecosystem/Toolkit/_apis/build/status/shotgunsoftware.tk-multi-demo?branchName=master)](https://dev.azure.com/shotgun-ecosystem/Toolkit/_build/latest?definitionId=38&branchName=master) # TODO change link
[![codecov](https://codecov.io/gh/shotgunsoftware/tk-multi-demo/branch/master/graph/badge.svg)](https://codecov.io/gh/shotgunsoftware/tk-multi-demo)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Creating Demos
==============

Demos are structured like mini Toolkit apps. Each directory under `demos`
contains one demo with the following contents:

* A `demo.py` file which houses a `QtGui.QWidget` subclass which represents the
demo to display to the user.
* An `__init__.py` file which typically just imports the demo widget into the
demo's module namespace
* A `demo.yml` file which provides information about the demo such as
    `display_name`, `description`, `documentation_url`, and required frameworks.

You can optionally include `resources` and `ui` sub directories if your demo
requires images or was constructed using **Designer**.

Once everything is in place, edit the `demos/__init__.py` file to import the
demo class and add it into the list of demos in one or more spots under
whichever demo groupings make the most sense.

Keep in mind that while the demo may show up under multiple groupings in the UI,
only one instance of the demo will be created to display.

The `app_scaffold` directory holds the basic scaffolding needed to generate a
ready-to-use app from any of the demo. There are some tokens in the scaffolding
which are replaced as the app is generated. These tokens are:

* `{{WIDGET_CLASS_NAME}}` - The name of the demo class to use as the primary
  widget in the app
* `{{APP_TITLE}}` - The title of the demo, used for the app dialog
* `{{APP_COMMAND_NAME}}` - The name of the

The tokens will either be pulled form the `demo.yml` file or computed based on
values in that file in conjuction with some introspection of the demo code itself.
