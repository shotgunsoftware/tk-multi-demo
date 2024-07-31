# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nav_widget_demo.ui'
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


from ..qtwidgets import NavigationWidget
from ..qtwidgets import BreadcrumbWidget

class Ui_NavigationWidgetDemoUI(object):
    def setupUi(self, NavigationWidgetDemoUI):
        if not NavigationWidgetDemoUI.objectName():
            NavigationWidgetDemoUI.setObjectName(u"NavigationWidgetDemoUI")
        NavigationWidgetDemoUI.resize(349, 338)
        self.verticalLayout = QVBoxLayout(NavigationWidgetDemoUI)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.top_layout = QGridLayout()
        self.top_layout.setSpacing(8)
        self.top_layout.setObjectName(u"top_layout")
        self.nav_widget_lbl = QLabel(NavigationWidgetDemoUI)
        self.nav_widget_lbl.setObjectName(u"nav_widget_lbl")
        self.nav_widget_lbl.setStyleSheet(u"QLabel {\n"
"    color: #999999;\n"
"	font-family: \"Courier New\";\n"
"}")
        self.nav_widget_lbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.top_layout.addWidget(self.nav_widget_lbl, 0, 0, 1, 1)

        self.nav_widget = NavigationWidget(NavigationWidgetDemoUI)
        self.nav_widget.setObjectName(u"nav_widget")

        self.top_layout.addWidget(self.nav_widget, 0, 1, 1, 1)

        self.nav_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.top_layout.addItem(self.nav_spacer, 0, 2, 1, 1)

        self.breadcrumb_widget_lbl = QLabel(NavigationWidgetDemoUI)
        self.breadcrumb_widget_lbl.setObjectName(u"breadcrumb_widget_lbl")
        self.breadcrumb_widget_lbl.setStyleSheet(u"QLabel {\n"
"    color: #999999;\n"
"	font-family: \"Courier New\";\n"
"}")
        self.breadcrumb_widget_lbl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.top_layout.addWidget(self.breadcrumb_widget_lbl, 1, 0, 1, 1)

        self.breadcrumb_widget = BreadcrumbWidget(NavigationWidgetDemoUI)
        self.breadcrumb_widget.setObjectName(u"breadcrumb_widget")

        self.top_layout.addWidget(self.breadcrumb_widget, 1, 1, 1, 2)

        self.top_layout.setColumnStretch(2, 1)

        self.verticalLayout.addLayout(self.top_layout)

        self.tree_view_layout = QHBoxLayout()
        self.tree_view_layout.setObjectName(u"tree_view_layout")
        self.tree_view = QTreeView(NavigationWidgetDemoUI)
        self.tree_view.setObjectName(u"tree_view")

        self.tree_view_layout.addWidget(self.tree_view)

        self.info_lbl = QLabel(NavigationWidgetDemoUI)
        self.info_lbl.setObjectName(u"info_lbl")
        self.info_lbl.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.info_lbl.setWordWrap(True)

        self.tree_view_layout.addWidget(self.info_lbl)

        self.tree_view_layout.setStretch(0, 1)
        self.tree_view_layout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.tree_view_layout)

        self.retranslateUi(NavigationWidgetDemoUI)

        QMetaObject.connectSlotsByName(NavigationWidgetDemoUI)
    # setupUi

    def retranslateUi(self, NavigationWidgetDemoUI):
        NavigationWidgetDemoUI.setWindowTitle(QCoreApplication.translate("NavigationWidgetDemoUI", u"Form", None))
        self.nav_widget_lbl.setText(QCoreApplication.translate("NavigationWidgetDemoUI", u"NavigationWidget:", None))
        self.breadcrumb_widget_lbl.setText(QCoreApplication.translate("NavigationWidgetDemoUI", u"BreadcrumbWidget:", None))
        self.info_lbl.setText(QCoreApplication.translate("NavigationWidgetDemoUI", u"<html><head/><body><p>Select items in the tree view to the left to see the <span style=\" font-family:'Courier New';\">NavigationWidget</span> and <span style=\" font-family:'Courier New';\">BreadcrumbWidget</span> above update. Then use the navigation widgets themselves to traverse the selection history in the tree view. Clicking the <span style=\" font-weight:600;\">Home</span> button in the <span style=\" font-family:'Courier New';\">NavigationWidget</span> will clear selection.</p></body></html>", None))
    # retranslateUi
