
Creating Demos
==============

Demos are structured like mini Toolkit apps. Each directory under `demos`
contains one demo with the following contents:

* A `demo.py` file which houses a `QtGui.QWidget` subclass which represents the
demo to display to the user.
* An `__init__.py` file which typically just imports the demo widget into the
demo's module namespace
* An `info.yml` file which is *exactly* like the bundle manifest for a regular
toolkit app

You can optionally include `resources` and `ui` sub directories if your demo
requires images or was constructed using **Designer**.

Once everything is in place, edit the `demos/__init__.py` file to import the
demo class and add it into the list of demos in one or more spots under
whichever demo groupings make the most sense.

Keep in mind that while the demo may show up under multiple groupings in the UI,
only one instance of the demo will be created to display.
