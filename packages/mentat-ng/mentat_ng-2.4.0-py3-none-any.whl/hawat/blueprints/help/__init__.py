#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Description
-----------

This pluggable module provides built-in help service.

"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


#
# Flask related modules.
#
from flask_babel import lazy_gettext

#
# Custom modules.
#
from hawat.base import HTMLMixin, SimpleView, HawatBlueprint


BLUEPRINT_NAME = 'help'
"""Name of the blueprint as module global constant."""


class ViewView(HTMLMixin, SimpleView):
    """
    View responsible for presenting built-in help.
    """
    authentication = True

    @classmethod
    def get_view_name(cls):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_view_name`."""
        return 'view'

    @classmethod
    def get_menu_icon(cls):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_menu_icon`."""
        return 'module-{}'.format(BLUEPRINT_NAME)

    @classmethod
    def get_menu_title(cls, item = None):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_menu_title`."""
        return lazy_gettext('Help')


#-------------------------------------------------------------------------------


class HelpBlueprint(HawatBlueprint):
    """
    Hawat pluggable module - built-in help.
    """

    @classmethod
    def get_module_title(cls):
        """*Implementation* of :py:func:`hawat.base.HawatBlueprint.get_module_title`."""
        return lazy_gettext('System help')


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface and factory function. This function must return a valid
    instance of :py:class:`hawat.base.HawatBlueprint` or :py:class:`flask.Blueprint`.
    """

    hbp = HelpBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates',
        url_prefix = '/{}'.format(BLUEPRINT_NAME)
    )

    hbp.register_view_class(ViewView, '/view')

    return hbp
