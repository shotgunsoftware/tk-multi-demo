# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'screen_capture_widget_demo.ui'
#
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from tank.platform.qt import QtCore, QtGui

class Ui_ShotgunWidgetDemoUI(object):
    def setupUi(self, ShotgunWidgetDemoUI):
        ShotgunWidgetDemoUI.setObjectName("ShotgunWidgetDemoUI")
        ShotgunWidgetDemoUI.resize(400, 340)
        self.verticalLayout = QtGui.QVBoxLayout(ShotgunWidgetDemoUI)
        self.verticalLayout.setObjectName("verticalLayout")
        self.view = QtGui.QListView(ShotgunWidgetDemoUI)
        self.view.setObjectName("view")
        self.verticalLayout.addWidget(self.view)
        self.view_mode_switch = QtGui.QPushButton(ShotgunWidgetDemoUI)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.view_mode_switch.sizePolicy().hasHeightForWidth())
        self.view_mode_switch.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.view_mode_switch.setFont(font)
        self.view_mode_switch.setObjectName("view_mode_switch")
        self.verticalLayout.addWidget(self.view_mode_switch)

        self.retranslateUi(ShotgunWidgetDemoUI)
        QtCore.QMetaObject.connectSlotsByName(ShotgunWidgetDemoUI)

    def retranslateUi(self, ShotgunWidgetDemoUI):
        ShotgunWidgetDemoUI.setWindowTitle(QtGui.QApplication.translate("ShotgunWidgetDemoUI", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.view_mode_switch.setText(QtGui.QApplication.translate("ShotgunWidgetDemoUI", "Switch to Icon View", None, QtGui.QApplication.UnicodeUTF8))

