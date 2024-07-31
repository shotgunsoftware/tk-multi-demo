# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'shotgun_widget_demo.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from tank.platform.qt import QtCore
for name, cls in QtCore.__dict__.items():
    if isinstance(cls, type): globals()[name] = cls

from tank.platform.qt import QtGui
for name, cls in QtGui.__dict__.items():
    if isinstance(cls, type): globals()[name] = cls


class Ui_ShotgunWidgetDemoUI(object):
    def setupUi(self, ShotgunWidgetDemoUI):
        if not ShotgunWidgetDemoUI.objectName():
            ShotgunWidgetDemoUI.setObjectName(u"ShotgunWidgetDemoUI")
        ShotgunWidgetDemoUI.resize(400, 340)
        self.verticalLayout = QVBoxLayout(ShotgunWidgetDemoUI)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.view = QListView(ShotgunWidgetDemoUI)
        self.view.setObjectName(u"view")

        self.verticalLayout.addWidget(self.view)

        self.view_mode_switch = QPushButton(ShotgunWidgetDemoUI)
        self.view_mode_switch.setObjectName(u"view_mode_switch")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.view_mode_switch.sizePolicy().hasHeightForWidth())
        self.view_mode_switch.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily(u"Courier New")
        self.view_mode_switch.setFont(font)

        self.verticalLayout.addWidget(self.view_mode_switch)

        self.retranslateUi(ShotgunWidgetDemoUI)

        QMetaObject.connectSlotsByName(ShotgunWidgetDemoUI)
    # setupUi

    def retranslateUi(self, ShotgunWidgetDemoUI):
        ShotgunWidgetDemoUI.setWindowTitle(QCoreApplication.translate("ShotgunWidgetDemoUI", u"Form", None))
        self.view_mode_switch.setText(QCoreApplication.translate("ShotgunWidgetDemoUI", u"Switch to Icon View", None))
    # retranslateUi
