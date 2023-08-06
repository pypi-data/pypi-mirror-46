#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom developer login form for Hawat.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


#
# Flask related modules.
#
import wtforms
import flask_wtf
from flask_babel import lazy_gettext

#
# Custom modules.
#
import hawat.db
from hawat.models.user import GuiUserModel


class LoginForm(flask_wtf.FlaskForm):
    """
    Class representing developer authentication login form. This form provides
    list of all currently existing user accounts in simple selectbox, so that
    the developer can quickly login as different user.
    """
    login  = wtforms.SelectField(
        lazy_gettext('User account:'),
        validators = [
            wtforms.validators.DataRequired()
        ]
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Login')
    )
    cancel = wtforms.SubmitField(
        lazy_gettext('Cancel')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_choices()

    def set_choices(self):
        """
        Load list of all user accounts and populate the ``choices`` attribute of
        the ``login`` selectbox.
        """
        dbsess = hawat.db.db_get().session
        users = dbsess.query(GuiUserModel).order_by(GuiUserModel.login).all()

        choices = []
        for usr in users:
            choices.append((usr.login, "{} ({}, #{})".format(usr.fullname, usr.login, usr.id)))
        choices = sorted(choices, key=lambda x: x[1])
        self.login.choices = choices
