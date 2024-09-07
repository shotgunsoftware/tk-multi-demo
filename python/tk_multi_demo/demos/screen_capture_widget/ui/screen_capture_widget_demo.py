# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'screen_capture_widget_demo.ui'
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


class Ui_ScreenCaptureWidgetDemoUI(object):
    def setupUi(self, ScreenCaptureWidgetDemoUI):
        if not ScreenCaptureWidgetDemoUI.objectName():
            ScreenCaptureWidgetDemoUI.setObjectName(u"ScreenCaptureWidgetDemoUI")
        ScreenCaptureWidgetDemoUI.resize(608, 306)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ScreenCaptureWidgetDemoUI.sizePolicy().hasHeightForWidth())
        ScreenCaptureWidgetDemoUI.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(ScreenCaptureWidgetDemoUI)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.top_layout = QFormLayout()
        self.top_layout.setObjectName(u"top_layout")
        self.top_layout.setHorizontalSpacing(8)
        self.top_layout.setVerticalSpacing(8)
        self.get_desktop_pixmap_btn = QPushButton(ScreenCaptureWidgetDemoUI)
        self.get_desktop_pixmap_btn.setObjectName(u"get_desktop_pixmap_btn")
        font = QFont()
        font.setFamily(u"Courier New")
        self.get_desktop_pixmap_btn.setFont(font)

        self.top_layout.setWidget(0, QFormLayout.LabelRole, self.get_desktop_pixmap_btn)

        self.get_desktop_pixmap_desc_layout = QVBoxLayout()
        self.get_desktop_pixmap_desc_layout.setObjectName(u"get_desktop_pixmap_desc_layout")
        self.get_desktop_pixmap_desc = QLabel(ScreenCaptureWidgetDemoUI)
        self.get_desktop_pixmap_desc.setObjectName(u"get_desktop_pixmap_desc")
        self.get_desktop_pixmap_desc.setWordWrap(False)

        self.get_desktop_pixmap_desc_layout.addWidget(self.get_desktop_pixmap_desc)

        self.get_desktop_pixmap_rect_layout = QHBoxLayout()
        self.get_desktop_pixmap_rect_layout.setObjectName(u"get_desktop_pixmap_rect_layout")
        self.left_lbl = QLabel(ScreenCaptureWidgetDemoUI)
        self.left_lbl.setObjectName(u"left_lbl")

        self.get_desktop_pixmap_rect_layout.addWidget(self.left_lbl)

        self.left_spin = QSpinBox(ScreenCaptureWidgetDemoUI)
        self.left_spin.setObjectName(u"left_spin")
        self.left_spin.setMaximum(2048)

        self.get_desktop_pixmap_rect_layout.addWidget(self.left_spin)

        self.right_lbl = QLabel(ScreenCaptureWidgetDemoUI)
        self.right_lbl.setObjectName(u"right_lbl")

        self.get_desktop_pixmap_rect_layout.addWidget(self.right_lbl)

        self.right_spin = QSpinBox(ScreenCaptureWidgetDemoUI)
        self.right_spin.setObjectName(u"right_spin")
        self.right_spin.setMaximum(2048)
        self.right_spin.setValue(350)

        self.get_desktop_pixmap_rect_layout.addWidget(self.right_spin)

        self.top_lbl = QLabel(ScreenCaptureWidgetDemoUI)
        self.top_lbl.setObjectName(u"top_lbl")

        self.get_desktop_pixmap_rect_layout.addWidget(self.top_lbl)

        self.top_spin = QSpinBox(ScreenCaptureWidgetDemoUI)
        self.top_spin.setObjectName(u"top_spin")
        self.top_spin.setMaximum(2048)

        self.get_desktop_pixmap_rect_layout.addWidget(self.top_spin)

        self.bottom_lbl = QLabel(ScreenCaptureWidgetDemoUI)
        self.bottom_lbl.setObjectName(u"bottom_lbl")

        self.get_desktop_pixmap_rect_layout.addWidget(self.bottom_lbl)

        self.bottom_spin = QSpinBox(ScreenCaptureWidgetDemoUI)
        self.bottom_spin.setObjectName(u"bottom_spin")
        self.bottom_spin.setMaximum(2048)
        self.bottom_spin.setValue(350)

        self.get_desktop_pixmap_rect_layout.addWidget(self.bottom_spin)

        self.get_desktop_pixmap_rect_layout.setStretch(1, 1)
        self.get_desktop_pixmap_rect_layout.setStretch(3, 1)
        self.get_desktop_pixmap_rect_layout.setStretch(5, 1)
        self.get_desktop_pixmap_rect_layout.setStretch(7, 1)

        self.get_desktop_pixmap_desc_layout.addLayout(self.get_desktop_pixmap_rect_layout)

        self.get_desktop_pixmap_desc_layout.setStretch(0, 1)

        self.top_layout.setLayout(0, QFormLayout.FieldRole, self.get_desktop_pixmap_desc_layout)

        self.screen_capture_btn = QPushButton(ScreenCaptureWidgetDemoUI)
        self.screen_capture_btn.setObjectName(u"screen_capture_btn")
        self.screen_capture_btn.setFont(font)

        self.top_layout.setWidget(1, QFormLayout.LabelRole, self.screen_capture_btn)

        self.screen_capture_desc = QLabel(ScreenCaptureWidgetDemoUI)
        self.screen_capture_desc.setObjectName(u"screen_capture_desc")

        self.top_layout.setWidget(1, QFormLayout.FieldRole, self.screen_capture_desc)

        self.screen_capture_file_btn = QPushButton(ScreenCaptureWidgetDemoUI)
        self.screen_capture_file_btn.setObjectName(u"screen_capture_file_btn")
        self.screen_capture_file_btn.setFont(font)

        self.top_layout.setWidget(2, QFormLayout.LabelRole, self.screen_capture_file_btn)

        self.screen_capture_file_lbl = QLabel(ScreenCaptureWidgetDemoUI)
        self.screen_capture_file_lbl.setObjectName(u"screen_capture_file_lbl")

        self.top_layout.setWidget(2, QFormLayout.FieldRole, self.screen_capture_file_lbl)

        self.verticalLayout.addLayout(self.top_layout)

        self.output_layout = QHBoxLayout()
        self.output_layout.setObjectName(u"output_layout")
        self.output_left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.output_layout.addItem(self.output_left_spacer)

        self.output_file = QLabel(ScreenCaptureWidgetDemoUI)
        self.output_file.setObjectName(u"output_file")
        font1 = QFont()
        font1.setItalic(True)
        self.output_file.setFont(font1)
        self.output_file.setStyleSheet(u"QLabel {\n"
"    color: #888888;\n"
"}")
        self.output_file.setAlignment(Qt.AlignCenter)
        self.output_file.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextSelectableByMouse)

        self.output_layout.addWidget(self.output_file)

        self.output_right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.output_layout.addItem(self.output_right_spacer)

        self.verticalLayout.addLayout(self.output_layout)

        self.results_layout = QHBoxLayout()
        self.results_layout.setObjectName(u"results_layout")
        self.results_left_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.results_layout.addItem(self.results_left_spacer)

        self.results_pixmap = QLabel(ScreenCaptureWidgetDemoUI)
        self.results_pixmap.setObjectName(u"results_pixmap")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.results_pixmap.sizePolicy().hasHeightForWidth())
        self.results_pixmap.setSizePolicy(sizePolicy1)
        self.results_pixmap.setMinimumSize(QSize(192, 108))
        self.results_pixmap.setStyleSheet(u"QLabel {\n"
"    background-color: #000000;\n"
"    border: 1px solid #000000;\n"
"}")
        self.results_pixmap.setFrameShape(QFrame.NoFrame)
        self.results_pixmap.setAlignment(Qt.AlignCenter)

        self.results_layout.addWidget(self.results_pixmap)

        self.results_right_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.results_layout.addItem(self.results_right_spacer)

        self.verticalLayout.addLayout(self.results_layout)

        self.dummy_label = QLabel(ScreenCaptureWidgetDemoUI)
        self.dummy_label.setObjectName(u"dummy_label")

        self.verticalLayout.addWidget(self.dummy_label)

        self.verticalLayout.setStretch(3, 1)
        self.output_file.raise_()
        self.dummy_label.raise_()

        self.retranslateUi(ScreenCaptureWidgetDemoUI)

        QMetaObject.connectSlotsByName(ScreenCaptureWidgetDemoUI)
    # setupUi

    def retranslateUi(self, ScreenCaptureWidgetDemoUI):
        ScreenCaptureWidgetDemoUI.setWindowTitle(QCoreApplication.translate("ScreenCaptureWidgetDemoUI", u"Form", None))
        self.get_desktop_pixmap_btn.setText(QCoreApplication.translate("ScreenCaptureWidgetDemoUI", u"get_desktop_pixmap(rect)", None))
        self.get_desktop_pixmap_desc.setText(QCoreApplication.translate("ScreenCaptureWidgetDemoUI", u"Performs a screen capture on the specified rectangle:", None))
        self.left_lbl.setText(QCoreApplication.translate("ScreenCaptureWidgetDemoUI", u"L:", None))
        self.right_lbl.setText(QCoreApplication.translate("ScreenCaptureWidgetDemoUI", u"R:", None))
        self.top_lbl.setText(QCoreApplication.translate("ScreenCaptureWidgetDemoUI", u"T:", None))
        self.bottom_lbl.setText(QCoreApplication.translate("ScreenCaptureWidgetDemoUI", u"B:", None))
        self.screen_capture_btn.setText(QCoreApplication.translate("ScreenCaptureWidgetDemoUI", u"screen_capture()", None))
        self.screen_capture_desc.setText(QCoreApplication.translate("ScreenCaptureWidgetDemoUI", u"Modally displays the screen capture tool", None))
        self.screen_capture_file_btn.setText(QCoreApplication.translate("ScreenCaptureWidgetDemoUI", u"screen_capture_file()", None))
        self.screen_capture_file_lbl.setText(QCoreApplication.translate("ScreenCaptureWidgetDemoUI", u"Modally display the screen capture tool, saving to a file", None))
        self.output_file.setText("")
        self.results_pixmap.setText("")
        self.dummy_label.setText("")
    # retranslateUi
