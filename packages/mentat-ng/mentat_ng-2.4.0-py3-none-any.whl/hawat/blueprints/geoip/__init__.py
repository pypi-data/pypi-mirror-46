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

This pluggable module provides access to internal IP geolocation service. It is
built upon custom :py:mod:`mentat.services.geoip` module, which in turn uses the
geolocation service `GeoLite2 <https://dev.maxmind.com/geoip/geoip2/geolite2/>`__
created by `MaxMind <http://www.maxmind.com/>`__.


Provided endpoints
------------------

``/geoip/search``
    Page providing search form and displaying search results.

    * *Authentication:* login required
    * *Methods:* ``GET``
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"

#
# Flask related modules.
#
import flask
from flask_babel import lazy_gettext

#
# Custom modules.
#
import mentat.services.geoip
from mentat.const import tr_

import hawat.const
import hawat.db
import hawat.acl
from hawat.base import HTMLMixin, RenderableView, HawatBlueprint, URLParamsBuilder
from hawat.blueprints.geoip.forms import GeoipSearchForm


BLUEPRINT_NAME = 'geoip'
"""Name of the blueprint as module global constant."""


class SearchView(HTMLMixin, RenderableView):
    """
    Application view providing search form for internal IP geolocation service
    and appropriate result page.

    The geolocation is implemented using :py:mod:`mentat.services.geoip` module.
    """
    methods = ['GET']

    authentication = True

    authorization = [hawat.acl.PERMISSION_ANY]

    @classmethod
    def get_view_name(cls):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_view_name`."""
        return 'search'

    @classmethod
    def get_menu_title(cls, item = None):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_menu_title`."""
        return lazy_gettext('Internal geoip')

    @classmethod
    def get_view_title(cls, item = None):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_view_title`."""
        return lazy_gettext('Search internal geoip database')

    #---------------------------------------------------------------------------

    def dispatch_request(self):
        """
        Mandatory interface required by the :py:func:`flask.views.View.dispatch_request`.
        Will be called by the *Flask* framework to service the request.
        """
        form = GeoipSearchForm(flask.request.args, meta = {'csrf': False})

        if hawat.const.HAWAT_FORM_ACTION_SUBMIT in flask.request.args:
            if form.validate():
                form_data = form.data
                geoip_manager = mentat.services.geoip.GeoipServiceManager(flask.current_app.mconfig)
                geoip_service = geoip_manager.service()
                self.response_context.update(
                    search_item   = form.search.data,
                    search_result = geoip_service.lookup(form.search.data),
                    form_data     = form_data
                )

        self.response_context.update(
            search_form  = form,
            request_args = flask.request.args,
        )
        return self.generate_response()

#-------------------------------------------------------------------------------


class GeoipBlueprint(HawatBlueprint):
    """
    Hawat pluggable module - IP geolocation service.
    """

    @classmethod
    def get_module_title(cls):
        """*Implementation* of :py:func:`hawat.base.HawatBlueprint.get_module_title`."""
        return lazy_gettext('Internal geoip pluggable module')

    def register_app(self, app):
        """
        *Callback method*. Will be called from :py:func:`hawat.base.HawatApp.register_blueprint`
        method and can be used to customize the Flask application object. Possible
        use cases:

        * application menu customization

        :param hawat.base.HawatApp app: Flask application to be customize.
        """
        app.menu_main.add_entry(
            'view',
            'more.{}'.format(BLUEPRINT_NAME),
            position = 10,
            group = lazy_gettext('Tools'),
            view = SearchView
        )

        # Register context actions provided by this module.
        app.set_csag(
            hawat.const.HAWAT_CSAG_ADDRESS,
            tr_('Search for address <strong>%(name)s</strong> in internal IP geolocation database'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('search')
        )


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface and factory function. This function must return a valid
    instance of :py:class:`hawat.base.HawatBlueprint` or :py:class:`flask.Blueprint`.
    """

    hbp = GeoipBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates',
        url_prefix = '/{}'.format(BLUEPRINT_NAME)
    )

    hbp.register_view_class(SearchView, '/search')

    return hbp
