#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains user account model for Hawat.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


#
# Custom modules.
#
import mentat.datatype.sqldb


class GuiUserModel(mentat.datatype.sqldb.UserModel):
    """
    Custom user account model for Hawat. The implementation is based on the
    :py:class:`mentat.datatype.sqldb.UserModel` and basically just adds couple of
    methods required by the :py:mod:`flask_login` extension.
    """
    @property
    def is_authenticated(self):
        """
        Mandatory interface required by the :py:mod:`flask_login` extension.
        """
        return True

    @property
    def is_active(self):
        """
        Mandatory interface required by the :py:mod:`flask_login` extension.
        """
        return self.enabled

    @property
    def is_anonymous(self):
        """
        Mandatory interface required by the :py:mod:`flask_login` extension.
        """
        return False

    def get_id(self):
        """
        Mandatory interface required by the :py:mod:`flask_login` extension.
        """
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def has_role(self, role):
        """
        Returns ``True`` if the user identifies with the specified role.

        :param str role: A role name.
        """
        return role in self.roles

    def has_no_role(self):
        """
        Returns ``True`` if the user has no role.
        """
        return len(self.roles) == 0
