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

This Hawat pluggable module provides special authentication method, that is
particularly usable for developers and enables them to impersonate any user.

After enabling this module special authentication endpoint will be available
and will provide simple authentication form with list of all currently available
user accounts. It will be possible for that user to log in as any other user
without entering password.

This module is disabled by default in *production* environment and enabled by
default in *development* environment.

.. warning::

    This module must never ever be enabled on production systems, because it is
    a huge security risk and enables possible access control management violation.
    You have been warned!


Provided endpoints
------------------

``/auth_dev/login``
    Page providing special developer login form.

    * *Authentication:* no authentication
    * *Methods:* ``GET``, ``POST``
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import sys
import traceback
import sqlalchemy

#
# Flask related modules.
#
import flask
import flask_login
import flask_principal
from flask_babel import gettext, lazy_gettext

#
# Custom modules.
#
import hawat.const
import hawat.forms
from hawat.base import HTMLMixin, SQLAlchemyMixin, SimpleView, HawatBlueprint
from hawat.models.user import GuiUserModel
from hawat.blueprints.auth_dev.forms import LoginForm


BLUEPRINT_NAME = 'auth_dev'
"""Name of the blueprint as module global constant."""


class LoginView(HTMLMixin, SQLAlchemyMixin, SimpleView):
    """
    View enabling special developer login.
    """
    methods = ['GET', 'POST']

    @classmethod
    def get_view_name(cls):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_view_name`."""
        return 'login'

    @classmethod
    def get_menu_icon(cls):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_menu_icon`."""
        return 'login'

    @classmethod
    def get_menu_title(cls, item = None):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_menu_title`."""
        return lazy_gettext('Developer login')

    @property
    def dbmodel(self):
        """*Implementation* of :py:func:`hawat.base.SQLAlchemyMixin.dbmodel`."""
        return GuiUserModel

    def dispatch_request(self):
        """
        Mandatory interface required by the :py:func:`flask.views.View.dispatch_request`.
        Will be called by the *Flask* framework to service the request.
        """
        form = LoginForm()

        if form.validate_on_submit():
            dbsess = hawat.db.db_get().session
            try:
                user = dbsess.query(GuiUserModel).filter(GuiUserModel.login == form.login.data).one()

                if not user.enabled:
                    self.flash(
                        flask.Markup(gettext(
                            'Please be aware, that the account for user <strong>%(login)s (%(name)s)</strong> is currently disabled.',
                            login = user.login,
                            name = user.fullname
                        )),
                        hawat.const.HAWAT_FLASH_FAILURE
                    )

                flask_login.login_user(user)

                # Tell Flask-Principal the identity changed. Access to private method
                # _get_current_object is according to the Flask documentation:
                #   http://flask.pocoo.org/docs/1.0/reqcontext/#notes-on-proxies
                flask_principal.identity_changed.send(
                    flask.current_app._get_current_object(),   # pylint: disable=locally-disabled,protected-access
                    identity = flask_principal.Identity(user.get_id())
                )

                self.flash(
                    flask.Markup(gettext(
                        'You have been successfully logged in as <strong>%(user)s</strong>.',
                        user = str(user)
                    )),
                    hawat.const.HAWAT_FLASH_SUCCESS
                )
                self.logger.info(
                    "User '{}' successfully logged in with 'auth_dev'.".format(
                        user.login
                    )
                )

                # Redirect user back to original page.
                return self.redirect(
                    default_url = flask.url_for(
                        flask.current_app.config['HAWAT_LOGIN_REDIRECT']
                    )
                )

            except sqlalchemy.orm.exc.MultipleResultsFound:
                self.logger.error(
                    "Multiple results found for user login '{}'.".format(
                        form.login.data
                    )
                )
                self.abort(500)

            except sqlalchemy.orm.exc.NoResultFound:
                self.flash(
                    gettext('You have entered wrong login credentials.'),
                    hawat.const.HAWAT_FLASH_FAILURE
                )

            except Exception:  # pylint: disable=locally-disabled,broad-except
                self.flash(
                    flask.Markup(gettext(
                        "Unable to perform developer login as <strong>%(user)s</strong>.",
                        user = str(form.login.data)
                    )),
                    hawat.const.HAWAT_FLASH_FAILURE
                )
                flask.current_app.log_exception_with_label(
                    traceback.TracebackException(*sys.exc_info()),
                    'Unable to perform developer login.',
                )

        self.response_context.update(
            form = form,
            next = hawat.forms.get_redirect_target()
        )
        return self.generate_response()


#-------------------------------------------------------------------------------


class DevAuthBlueprint(HawatBlueprint):
    """
    Hawat pluggable module - special developer authentication (*auth_dev*).
    """

    @classmethod
    def get_module_title(cls):
        """*Implementation* of :py:func:`hawat.base.HawatBlueprint.get_module_title`."""
        return lazy_gettext('Hawat developer authentication service pluggable module')

    def register_app(self, app):
        """
        *Callback method*. Will be called from :py:func:`hawat.base.HawatApp.register_blueprint`
        method and can be used to customize the Flask application object. Possible
        use cases:

        * application menu customization

        :param hawat.base.HawatApp app: Flask application to be customize.
        """
        app.menu_anon.add_entry(
            'view',
            'login_dev',
            position = 20,
            view = LoginView,
            hidelegend = True
        )
        app.menu_auth.add_entry(
            'view',
            'login_dev',
            position = 50,
            view = LoginView,
            hidelegend = True
        )


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface and factory function. This function must return a valid
    instance of :py:class:`hawat.base.HawatBlueprint` or :py:class:`flask.Blueprint`.
    """

    hbp = DevAuthBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates',
        url_prefix = '/{}'.format(BLUEPRINT_NAME)
    )

    hbp.register_view_class(LoginView, '/login')

    return hbp
