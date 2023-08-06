#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains application menu model for Hawat user interface.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import collections

import flask
import flask_login
import flask_principal

import hawat.acl


ENTRY_TYPE_DBSUBMENU = 'dbsubmenu'
ENTRY_TYPE_SUBMENU   = 'submenu'
ENTRY_TYPE_VIEW      = 'view'
ENTRY_TYPE_ENDPOINT  = 'endpoint'
ENTRY_TYPE_LINK      = 'link'
ENTRY_TYPE_TEST      = 'test'


def _url_segments(path):
    parts = path.split('/')[1:]
    if parts and parts[-1] == '':
        parts.pop()
    return parts

def _is_active(this_url, request):
    request_path = request.script_root + request.path
    if len(this_url) > 1:
        segments_url = _url_segments(this_url)
        segments_request = _url_segments(request_path)
        matching_segments = segments_request == segments_url
    else:
        matching_segments = False
    matching_completpath = (request.script_root + request.full_path) == this_url
    return matching_segments or matching_completpath


def _filter_menu_entries(entries, item = None):
    """
    Filter given list of menu entries for current user. During the filtering
    following operations will be performed:

    * Remove all entries accessible only for authenticated users, when the current
      user is not authenticated.
    * Remove all entries for which the current user has not sufficient permissions.
    * Remove all empty submenu entries.

    :param collections.OrderedDict entries: List of menu entries.
    :param item: Optional item for which the menu should be parametrized.
    :return: Filtered list of menu entries.
    :rtype: collections.OrderedDict
    """
    result = collections.OrderedDict()
    for entry_id, entry in entries.items():
        #print("Processing menu entry '{}'.".format(entry_id))

        # Filter out entries protected with authentication.
        if entry.authentication:
            if not flask_login.current_user.is_authenticated:
                #print("Hiding menu entry '{}', accessible only to authenticated users.".format(entry_id))
                continue

        # Filter out entries protected with authorization.
        if entry.authorization:
            hideflag = False
            for authspec in entry.authorization:
                # Authorization rules may be specified as instances of flask_principal.Permission.
                if isinstance(authspec, flask_principal.Permission):
                    if not authspec.can():
                        #print("Hiding menu entry '{}', accessible only to '{}'.".format(entry_id, str(authspec)))
                        hideflag = True
                # Authorization rules may be specified as indices to hawat.acl permission dictionary.
                else:
                    if not hawat.acl.PERMISSIONS[authspec].can():
                        #print("Hiding menu entry '{}', accessible only to '{}'.".format(entry_id, str(authspec)))
                        hideflag = True
            if hideflag:
                continue

        if entry.type == ENTRY_TYPE_SUBMENU:
            # Filter out empty submenus.
            if not _filter_menu_entries(entry.entries, item):
                #print("Hiding menu entry '{}', empty submenu.".format(entry_id))
                continue

        if entry.type == ENTRY_TYPE_VIEW:
            # Check item action authorization callback, if exists.
            if hasattr(entry.view, 'authorize_item_action'):
                item = entry.pick_item(item)
                if not entry.view.authorize_item_action(item):
                    #print("Hiding menu entry '{}', inaccessible item action for item '{}'.".format(entry_id, str(item)))
                    continue

            # Check item change validation callback, if exists.
            if hasattr(entry.view, 'validate_item_change'):
                item = entry.pick_item(item)
                if not entry.view.validate_item_change(item):
                    #print("Hiding menu entry '{}', invalid item change for item '{}'.".format(entry_id, str(item)))
                    continue

        result[entry_id] = entry

    return result

def _get_menu_entries(entries, item = None):
    """
    *Helper function*. Return filtered and sorted menu entries for current user.

    :param collections.OrderedDict entries: List of menu entries.
    :param item: Optional item for which the menu should be parametrized.
    :return: Filtered list of menu entries.
    :rtype: collections.OrderedDict
    """
    return sorted(list(_filter_menu_entries(entries, item).values()), key = lambda x: x.position)


#-------------------------------------------------------------------------------


class HawatMenuEntry:
    """
    Base class for all menu entries.
    """
    def __init__(self, ident, **kwargs):
        self.type       = None
        self.ident      = ident
        self.position   = kwargs.get('position', 0)
        self.group      = kwargs.get('group', None)
        self._title     = kwargs.get('title', None)
        self._icon      = kwargs.get('icon', None)
        self._legend    = kwargs.get('legend', None)
        self.hidetitle  = kwargs.get('hidetitle', False)
        self.hideicon   = kwargs.get('hideicon', False)
        self.hidelegend = kwargs.get('hidelegend', False)
        self.resptitle  = kwargs.get('resptitle', False)
        self.respicon   = kwargs.get('respicon', False)
        self.resplegend = kwargs.get('resplegend', False)

    def __repr__(self):
        return '{}'.format(self.ident)

    def get_title(self, item = None):
        """
        Return menu title for current entry.

        :param item: Optional item for which the menu entry should be parametrized.
        :return: Title for current menu entry.
        :rtype: str
        """
        if not self.hidetitle:
            if self._title:
                if callable(self._title):
                    return self._title(item)
                return self._title
        return None

    def get_icon(self, item = None):
        """
        Return menu icon for current entry.

        :param item: Optional item for which the menu entry should be parametrized.
        :return: Icon for current menu entry.
        :rtype: str
        """
        if not self.hideicon:
            if self._icon:
                if callable(self._icon):
                    return self._icon(item)
                return self._icon
        return None

    def get_legend(self, item = None):
        """
        Return menu legend for current entry.

        :param item: Optional item for which the menu entry should be parametrized.
        :return: Legend for current menu entry.
        :rtype: str
        """
        if not self.hidelegend:
            if self._legend:
                if callable(self._legend):
                    return self._legend(item)
                return self._legend
        return None

    def get_menu(self, item = None):
        """
        Get list of submenu entries for this entry.

        :param item: Optional item for which the menu entry should be parametrized.
        :return: List of submenu entries for this entry.
        :rtype: list
        """
        raise NotImplementedError()

    def add_entry(self, ident, subentry):
        """
        Add new entry into the submenu of this entry.

        :param str ident: Unique identifier of the subentry within the submenu.
        """
        raise NotImplementedError()

    def is_active(self, request, item = None):
        """
        Check, if this menu entry is active thanks to the given request.

        :param flask.Request request: Current request object.
        :param item: Optional item for which the menu entry should be parametrized.
        :return: ``True`` in case menu entry is active, ``False`` otherwise.
        :rtype: bool
        """
        raise NotImplementedError()


class HawatSubmenuMenuEntry(HawatMenuEntry):
    """
    Class for entries representing whole submenu trees.
    """

    def __init__(self, ident, **kwargs):
        super().__init__(ident, **kwargs)
        self.type           = ENTRY_TYPE_SUBMENU
        self.align_right    = kwargs.get('align_right', False)
        self.authentication = kwargs.get('authentication', False)
        self.authorization  = kwargs.get('authorization', [])
        self.entries        = collections.OrderedDict()

    def get_menu(self, item = None):
        return _get_menu_entries(self.entries, item)

    def add_entry(self, ident, subentry):
        path = ident.split('.', 1)
        # Last chunk.
        if len(path) == 1:
            self.entries[path[0]] = subentry
        # Delegate to sub-submenu
        else:
            self.entries[path[0]].add_entry(path[1], subentry)

    def is_active(self, request, item = None):
        return False


class HawatDbSubmenuMenuEntry(HawatMenuEntry):
    """
    Class for entries representing whole submenu trees whose contents are fetched
    on demand from database.
    """

    def __init__(self, ident, **kwargs):
        super().__init__(ident, **kwargs)
        self.type           = ENTRY_TYPE_SUBMENU
        self.align_right    = kwargs.get('align_right', False)
        self.authentication = kwargs.get('authentication', False)
        self.authorization  = kwargs.get('authorization', [])
        self.entry_fetcher  = kwargs['entry_fetcher']
        self.entry_builder  = kwargs['entry_builder']

    @property
    def entries(self):
        """
        Dynamical property fetching current set of submenu entries from database.
        """
        entries = collections.OrderedDict()
        items = self.entry_fetcher()
        if items:
            for i in items:
                entry_id = '{}'.format(str(i))
                entries[entry_id] = self.entry_builder(entry_id, i)
        return entries

    def get_menu(self, item = None):
        return _get_menu_entries(self.entries)

    def add_entry(self, ident, subentry):
        raise RuntimeError("Unable to append submenu to '{}' DB menu item.".format(self.ident))

    def is_active(self, request, item = None):
        return False


class HawatViewMenuEntry(HawatMenuEntry):
    """
    Class representing menu entries pointing to application views.
    """

    def __init__(self, ident, **kwargs):
        super().__init__(ident, **kwargs)
        self.type  = ENTRY_TYPE_VIEW
        self._link = kwargs.get('link', None)
        self._item = kwargs.get('item', None)
        self.view  = kwargs.get('view', None)

    def pick_item(self, item = None):
        """
        Pick item to be used for current menu entry parametrization.
        """
        item = self._item or item or None
        try:
            return item()
        except TypeError:
            return item

    @property
    def endpoint(self):
        """
        Property containing routing endpoint for current entry.

        :return: Routing endpoint for current menu entry.
        :rtype: str
        """
        return self.view.get_view_endpoint()

    @property
    def authentication(self):
        """
        Property containing authentication information for current entry.

        :return: Authentication information for current menu entry.
        :rtype: str
        """
        return self.view.authentication

    @property
    def authorization(self):
        """
        Property containing authorization information for current entry.

        :return: Authorization information for current menu entry.
        :rtype: str
        """
        return self.view.authorization

    def get_title(self, item = None):
        """
        Return menu title for current entry.

        :param item: Optional item for which the menu entry should be parametrized.
        :return: Title for current menu entry.
        :rtype: str
        """
        item = self.pick_item(item)
        if not self.hidetitle:
            value = self._title or self.view.get_menu_title(item = item) or self.view.get_view_title(item = item)
            if value:
                if callable(value):
                    return value(item)
                return value
        return None

    def get_icon(self, item = None):
        """
        Return menu icon for current entry.

        :param item: Optional item for which the menu entry should be parametrized.
        :return: Icon for current menu entry.
        :rtype: str
        """
        item = self.pick_item(item)
        try:
            if not self.hideicon:
                value = self._icon or self.view.get_menu_icon()
                if value:
                    if callable(value):
                        return value(item)
                    return value
            return None
        except NotImplementedError:
            return 'missing-icon'

    def get_legend(self, item = None):
        """
        Return menu legend for current entry.

        :param item: Optional item for which the menu entry should be parametrized.
        :return: Legend for current menu entry.
        :rtype: str
        """
        item = self.pick_item(item)
        if not self.hidelegend:
            value = self._legend or self.view.get_menu_legend(item = item)
            if value:
                if callable(value):
                    return value(item)
                return value
        return None

    def get_url(self, item = None):
        """
        Return URL for current entry.

        :param item: Optional item for which the menu should be parametrized.
        :return: URL for current menu entry.
        :rtype: str
        """
        item = self.pick_item(item)
        value = self._link or self.view.get_menu_link(item = item)
        if value:
            if callable(value):
                return value(item)
            return value
        return flask.url_for(self.endpoint)

    def get_menu(self, item = None):
        return []

    def add_entry(self, ident, subentry):
        raise RuntimeError("Unable to append submenu to '{}' view menu item.".format(self.ident))

    def is_active(self, request, item = None):
        #print("Checking if menu entry '{}' is active.".format(self.ident))
        item = self.pick_item(item)
        return _is_active(self.get_url(item), request)


class HawatEndpointMenuEntry(HawatViewMenuEntry):
    """
    Class representing menu entries pointing to application routing endpoints.
    """

    def __init__(self, ident, endpoint, **kwargs):
        kwargs['view'] = flask.current_app.get_endpoint_class(endpoint)
        super().__init__(ident, **kwargs)


class HawatLinkMenuEntry(HawatMenuEntry):
    """
    Class representing menu entries pointing to application views.
    """

    def __init__(self, ident, **kwargs):
        super().__init__(ident, **kwargs)
        self.type           = ENTRY_TYPE_LINK
        self.authentication = kwargs.get('authentication', False)
        self.authorization  = kwargs.get('authorization', [])
        self._link          = kwargs.get('link')

    def get_url(self, item = None):
        """
        Return URL for current entry.

        :param item: Optional item for which the menu should be parametrized.
        :return: URL for current menu entry.
        :rtype: str
        """
        try:
            return self._link(item)
        except TypeError:
            return self._link

    def get_menu(self, item = None):
        return []

    def add_entry(self, ident, subentry):
        raise RuntimeError("Unable to append submenu to '{}' view menu item.".format(self.ident))

    def is_active(self, request, item = None):
        #print("Checking if menu entry '{}' is active.".format(self.ident))
        return _is_active(self.get_url(), request)


class HawatTestMenuEntry(HawatMenuEntry):
    """
    Class for menu entries for testing and demonstration purposes.
    """

    def __init__(self, ident, **kwargs):
        super().__init__(ident, **kwargs)
        self.type           = ENTRY_TYPE_TEST
        self.authentication = kwargs.get('authentication', False)
        self.authorization  = kwargs.get('authorization', [])

    def get_menu(self, item = None):
        return []

    def add_entry(self, ident, subentry):
        raise RuntimeError("Unable to append submenu to '{}' view menu item.".format(self.ident))

    def is_active(self, request, item = None):
        raise RuntimeError("This method makes no sense for test menu entries.")


class HawatMenu:
    """
    Class for application menu.
    """
    def __init__(self):
        self.entries = collections.OrderedDict()

    def __repr__(self):
        return '{}'.format(self.entries)

    def get_menu(self, item = None):
        """
        Get list of entries for this menu.

        :param item: Optional item for which the menu should be parametrized.
        :return: List of entries for this menu.
        :rtype: list
        """
        return _get_menu_entries(self.entries, item)

    def add_entry(self, entry_type, ident, **kwargs):
        """
        Add new entry into the menu.

        :param str entry_type: Type/class of the menu entry as string, object of the correct class will be created.
        :param str ident: Unique identifier of the entry within the menu.
        :param dict kwargs: Additional arguments, that will be passed to the constructor of the appropriate entry class.
        """
        entry = None
        if entry_type == 'submenu':
            entry = HawatSubmenuMenuEntry(ident, **kwargs)
        if entry_type == 'dbsubmenu':
            entry = HawatDbSubmenuMenuEntry(ident, **kwargs)
        elif entry_type == 'view':
            entry = HawatViewMenuEntry(ident, **kwargs)
        elif entry_type == 'endpoint':
            entry = HawatEndpointMenuEntry(ident, **kwargs)
        elif entry_type == 'link':
            entry = HawatLinkMenuEntry(ident, **kwargs)
        elif entry_type == 'test':
            entry = HawatTestMenuEntry(ident, **kwargs)
        if not entry:
            raise ValueError("Invalid value '{}' for HawatMenu entry type for entry '{}'.".format(entry_type, ident))

        path = ident.split('.', 1)
        # Last chunk.
        if len(path) == 1:
            self.entries[path[0]] = entry
        else:
            self.entries[path[0]].add_entry(path[1], entry)


if __name__ == '__main__':

    MENU = HawatMenu()
    MENU.add_entry('test', 'test0', position = 10)
    MENU.add_entry('test', 'test1', position = 10)
    MENU.add_entry('test', 'test2', position = 20)
    MENU.add_entry('test', 'test3', position = 40)
    MENU.add_entry('test', 'test4', position = 30)

    MENU.add_entry('submenu', 'sub1', position = 50)
    MENU.add_entry('submenu', 'sub2', position = 60)

    MENU.add_entry('test', 'sub1.test1', position = 10)
    MENU.add_entry('test', 'sub1.test2', position = 20)
    MENU.add_entry('test', 'sub1.test3', position = 40)
    MENU.add_entry('test', 'sub1.test4', position = 30)
    MENU.add_entry('test', 'sub2.test1', position = 10)
    MENU.add_entry('test', 'sub2.test2', position = 20)
    MENU.add_entry('test', 'sub2.test3', position = 40)
    MENU.add_entry('test', 'sub2.test4', position = 30)

    import pprint

    pprint.pprint(MENU.get_menu())

    pprint.pprint(MENU.__class__)
