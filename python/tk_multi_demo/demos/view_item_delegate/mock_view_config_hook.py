# Copyright (c) 2021 Autodesk, Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the ShotGrid Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
#
# agreement to the ShotGrid Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Autodesk, Inc.

import sgtk
from sgtk.platform.qt import QtCore, QtGui


class MockViewConfigHook(object):
    """
    A mock hook, to demonstrate how a Qt model class can optionally call a hook method to
    retrieve view configuration customizations.
    """

    @staticmethod
    def _get_item_thumbnail(item):
        """
        Return the thumbnail data for item.

        :param item: The model item
        :type item: QStandardItem
        """

        thumbnail = item.data(QtCore.Qt.DecorationRole)

        if thumbnail is None:
            thumbnail = QtGui.QPixmap()

        return thumbnail

    @staticmethod
    def _get_item_header(item):
        """
        Return the header data for the item.

        Notice that the return value is a tuple. The ViewItemDelegate will handle
        a tuple that contains a templated string as the first item, and a ShotGrid
        data dictionary as the second item. The delegate will process the template
        and data provided to search and replace tokens before displaying the value.

        See tk-framework-qtwidgets utils.py method convert_token_string for more
        details on how string template resolution is done.

        :param item: The model item
        :type item: QStandardItem

        :return: The item header data.
        :rtype: tuple(str, dict)
        """

        sg_data = item.get_sg_data()
        template_string = "<span style='font-size:16px;'>{content}</span>"
        return (template_string, sg_data)

    @staticmethod
    def _get_item_subtitle(item):
        """
        Return the subtitle data for the item.

        Notice that the return value is a tuple. The ViewItemDelegate will handle
        a tuple that contains a templated string as the first item, and a ShotGrid
        data dictionary as the second item. The delegate will process the template
        and data provided to search and replace tokens before displaying the value.

        See tk-framework-qtwidgets utils.py method convert_token_string for more
        details on how string template resolution is done.

        :param item: The model item
        :type item: QStandardItem

        :return: The item subtitle data.
        :rtype: tuple(str, dict)
        """

        sg_data = item.get_sg_data()
        template_string = (
            "<span style='color: rgba(200, 200, 200, 40%);'>{sg_status_list}</span>"
        )
        return (template_string, sg_data)

    @staticmethod
    def _get_item_text(item):
        """
        Return the detailed text data for the item.

        Notice that the return value is a tuple. The ViewItemDelegate will handle
        a tuple that contains a templated string as the first item, and a ShotGrid
        data dictionary as the second item. The delegate will process the template
        and data provided to search and replace tokens before displaying the value.

        See tk-framework-qtwidgets utils.py method convert_token_string for more
        details on how string template resolution is done.

        :param item: The model item
        :type item: QStandardItem

        :return: The item long text data.
        :rtype: tuple(str, dict)
        """

        sg_data = item.get_sg_data()
        template_string = "<br/>".join(
            [
                "{project::showtype}",
                "{entity::showtype}",
                "{[<span style='color:#18A7E3'>Assigned to </span>]task_assignees}",
                "{[By: ]created_by|Unknown} {created_at}",
            ]
        )
        return (template_string, sg_data)

    @staticmethod
    def _get_item_short_text(item):
        """
        Return the condensed text data for the item.

        Notice that the return value is a tuple. The ViewItemDelegate will handle
        a tuple that contains a templated string as the first item, and a ShotGrid
        data dictionary as the second item. The delegate will process the template
        and data provided to search and replace tokens before displaying the value.

        See tk-framework-qtwidgets utils.py method convert_token_string for more
        details on how string template resolution is done.

        :param item: The model item
        :type item: QStandardItem

        :return: The item short text data.
        :rtype: tuple(str, dict)
        """

        sg_data = item.get_sg_data()
        template_string = "<br/>".join(
            [
                "<span style='font-size:10px;'>{content}</span>",
                "<span style='font-size:10px;'>{entity::showtype}</span>",
            ]
        )
        return (template_string, sg_data)
