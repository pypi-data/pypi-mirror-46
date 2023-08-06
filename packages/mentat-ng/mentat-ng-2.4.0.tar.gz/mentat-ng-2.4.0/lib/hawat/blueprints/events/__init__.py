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
--------------------------------------------------------------------------------

This pluggable module provides access to `IDEA <https://idea.cesnet.cz/en/index>`__
message database. It enables users to execute custom queries via provided search
form, display the details of the messages or download them locally to their own
computers. Additionally the overview dashboard panel is provided.


.. _section-hawat-plugin-events-endpoints:

Provided endpoints
--------------------------------------------------------------------------------

``/events/search``
    Endpoint providing search form for querying the `IDEA <https://idea.cesnet.cz/en/index>`__
    message database.

    * *Authentication:* login required
    * *Authorization:* any role
    * *Methods:* ``GET``

``/api/events/search``
    Endpoint providing API search form for querying the `IDEA <https://idea.cesnet.cz/en/index>`__
    message database. See appropriate :ref:`section <section-hawat-plugin-events-webapi-search>`
    below for the description of API interface.

    * *Authentication:* login required
    * *Authorization:* any role
    * *Methods:* ``GET``, ``POST``

``/events/<item_id>/show``
    Endpoint providing detail view of given `IDEA <https://idea.cesnet.cz/en/index>`__
    message.

    * *Authentication:* login required
    * *Authorization:* any role
    * *Methods:* ``GET``

``/api/events/<item_id>/show``
    Endpoint providing API for retrieving given `IDEA <https://idea.cesnet.cz/en/index>`__
    message. See appropriate :ref:`section <section-hawat-plugin-events-webapi-show>`
    below for the description of API interface.

    * *Authentication:* login required
    * *Authorization:* any role
    * *Methods:* ``GET``

``/events/<item_id>/download``
    Endpoint enabling users to download given `IDEA <https://idea.cesnet.cz/en/index>`__
    message as JSON file.

    * *Authentication:* login required
    * *Authorization:* any role
    * *Methods:* ``GET``

``/events/dashboard``
    Endpoint providing overall `IDEA <https://idea.cesnet.cz/en/index>`__ message
    dashboard overview.

    * *Authentication:* login required
    * *Authorization:* any role
    * *Methods:* ``GET``

``/api/events/dashboard``
    Endpoint providing API for retrieving overall `IDEA <https://idea.cesnet.cz/en/index>`__
    message dashboard overview. See appropriate :ref:`section <section-hawat-plugin-events-webapi-dashboard>`
    below for the description of API interface.

    * *Authentication:* login required
    * *Authorization:* any role
    * *Methods:* ``GET``

``/api/events/metadata``
    Endpoint providing API for retrieving various `IDEA <https://idea.cesnet.cz/en/index>`__
    message metadata. See appropriate :ref:`section <section-hawat-plugin-events-webapi-metadata>`
    below for the description of API interface.

    * *Authentication:* login required
    * *Authorization:* any role
    * *Methods:* ``GET``


.. _section-hawat-plugin-events-webapi:

Web API
--------------------------------------------------------------------------------

The API interface must be accessed by authenticated user. For web client side scripts
and applications it should be sufficient to use standard cookie-based authentication.
If you need to access the API from outside of the web browser, it might be usefull
to generate yourself an API access token and use the token based authentication.
For security reasons you have to use ``POST`` method for sending the token, otherwise
it might get logged on many different and insecure places (like web server logs).


.. _section-hawat-plugin-events-webapi-search:

API endpoint: **search**
````````````````````````````````````````````````````````````````````````````````

Endpoint URL: ``/api/events/search``

The URL for web API interface is available as normal endpoint to the user of the web
interface. This fact can be used to debug the queries interactively and then simply
copy them to another application. One might for example start with filling in the
search form in the ``/events/search`` endpoint. Once you are satisfied with the
result, you can simply switch the base URL to the ``/api/events/search`` endpoint
and you are all set.


**Available query parameters**:

Following parameters may be specified as standard HTTP query parameters:

*Time related query parameters*

``dt_from``
    * *Description:* Lower event detection time boundary
    * *Datatype:* Datetime in the format ``YYYY-MM-DD HH:MM:SS``, for example ``2018-01-01 00:00:00``
    * *Default:* Previous midnight
    * *Note:* Default value kicks in in case the parameter is not specified, explicitly use empty value for boundless search
``dt_to``
    * *Description:* Upper event detection time boundary
    * *Datatype:* Datetime in the format ``YYYY-MM-DD HH:MM:SS``, for example ``2018-01-01 00:00:00``
``st_from``
    * *Description:* Lower event storage time boundary
    * *Datatype:* Datetime in the format ``YYYY-MM-DD HH:MM:SS``, for example ``2018-01-01 00:00:00``
``st_to``
    * *Description:* Upper event storage time boundary
    * *Datatype:* Datetime in the format ``YYYY-MM-DD HH:MM:SS``, for example ``2018-01-01 00:00:00``

*Origin related query parameters*

``source_addrs``
    * *Description:* List of required event sources
    * *Datatype:* ``list of IP(4|6) addressess|networks|ranges as strings``
    * *Logical operation:* All given values are *OR*ed
``source_ports``
    * *Description:* List of required event source ports
    * *Datatype:* ``list of integers``
    * *Logical operation:* All given values are *OR*ed
``source_types``
    * *Description:* List of required event source `types (tags) <https://idea.cesnet.cz/en/classifications#sourcetargettagsourcetarget_classification>`__
    * *Datatype:* ``list of strings``
    * *Logical operation:* All given values are *OR*ed
``target_addrs``
    * *Description:* List of required event targets
    * *Datatype:* ``list of IP(4|6) addressess|networks|ranges as strings``
    * *Logical operation:* All given values are *OR*ed
``target_ports``
    * *Description:* List of required event target ports
    * *Datatype:* ``list of integers``
    * *Logical operation:* All given values are *OR*ed
``target_types``
    * *Description:* List of required event target ports
    * *Datatype:*  ``list of strings``
    * *Logical operation:* All given values are *OR*ed
``host_addrs``
    * *Description:* List of required event sources or targets
    * *Datatype:* ``list of IP(4|6) addressess|networks|ranges as strings``
    * *Logical operation:* All given values are *OR*ed
``host_ports``
    * *Description:* List of required event source or target ports
    * *Datatype:* ``list of integers``
    * *Logical operation:* All given values are *OR*ed
``host_types``
    * *Description:* List of required event source or target ports
    * *Datatype:* ``list of strings``
    * *Logical operation:* All given values are *OR*ed

*Event related query parameters*

``groups``
    * *Description:* List of required event resolved groups
    * *Datatype:* ``list of strings``
    * *Logical operation:* All given values are *OR*ed
``not_groups``
    * *Description:* Invert group selection
    * *Datatype:* ``boolean``
``protocols``
    * *Description:* List of required event protocols
    * *Datatype:* ``list of strings``
    * *Logical operation:* All given values are *OR*ed
``not_protocols``
    * *Description:* Invert protocol selection
    * *Datatype:* ``boolean``
``description``
    * *Description:* Event description
    * *Datatype:* ``string``
``categories``
    * *Description:* List of required event `categories <https://idea.cesnet.cz/en/classifications>`__
    * *Datatype:* ``list of strings``
    * *Logical operation:* All given values are *OR*ed
``not_categories``
    * *Description:* Invert the category selection
    * *Datatype:* ``boolean``
``severities``
    * *Description:* List of required event severities
    * *Datatype:* ``list of strings``
    * *Logical operation:* All given values are *OR*ed
``not_severities``
    * *Description:* Invert the severity selection
    * *Datatype:* ``boolean``

*Detector related query parameters*

``detectors``
    * *Description:* List of required event detectors
    * *Datatype:* ``list of strings``
    * *Logical operation:* All given values are *OR*ed
``not_detectors``
    * *Description:* Invert detector selection
    * *Datatype:* ``boolean``
``detector_types``
    * *Description:* List of required event detector `types (tags) <https://idea.cesnet.cz/en/classifications#nodetagclassification_of_detection_nodes>`__
    * *Datatype:* ``list of strings``
    * *Logical operation:* All given values are *OR*ed
``not_detector_types``
    * *Description:*
    * *Datatype:* ``boolean``

*Special query parameters*

``inspection_errs``
    * *Description:* List of required event inspection errors
    * *Datatype:* ``list of strings``
    * *Logical operation:* All given values are *OR*ed
``not_inspection_errs``
    * *Description:* Invert inspection error selection
    * *Datatype:* ``boolean``
``classes``
    * *Description:* List of required event classes
    * *Datatype:* ``list of strings``
    * *Logical operation:* All given values are *OR*ed
``not_classess``
    * *Description:* Invert class selection
    * *Datatype:* ``boolean``

*Common query parameters*

``page``
    * *Description:* Result page
    * *Datatype:* ``integer``
    * *Default:* ``1``
``limit``
    * *Description:* Limit the number of results on single page
    * *Datatype:* ``integer`` (``5``, ``10``, ``20``, ``30``, ``50``, ``100``, ``200``, ``500``, ``1000``, ``10000``)
    * *Default:* ``100``
``sortby``
    * *Description:* Result sorting condition
    * *Datatype:* ``string`` (``"time.desc"``, ``"time.asc"``, ``"detecttime.desc"``, ``"detecttime.asc"``, ``"storagetime.desc"``, ``"storagetime.asc"``)
    * *Default:* ``"time.desc"``
``submit``
    * *Description:* Search trigger button
    * *Datatype:* ``boolean`` or ``string`` (``True`` or ``"Search"``)
    * *Note:* This query parameter must be present to trigger the search


**Search examples**

* Default search query::

    /api/events/search?submit=Search

* Search without default lower detect time boundary::

    /api/events/search?dt_from=&submit=Search


**Response format**

JSON document, that will be received as a response for the search, can contain
following keys:

``form_data``
    * *Description:* This subkey is present in case search operation was triggered.
      It contains a dictionary with all query parameters described above and their
      appropriate processed values.
    * *Datatype:* ``dictionary``
``form_errors``
    * *Description:* This subkey is present in case there were any errors in the
      submitted search form and the search operation could not be triggered. So
      in another words the presence of this subkey is an indication of search failure.
      This subkey contains list of all form errors as pairs of strings: name of
      the form field and error description. The error description is localized
      according to the user`s preferences.
    * *Datatype:* ``list of tuples of strings``
    * *Example:* ``[["dt_from", "Not a valid datetime value"]]``
``items``
    * *Description:* This subkey is present in case search operation was triggered.
      It contains a list of IDEA messages that matched the query parameters. The
      messages are formated according to the `IDEA specification <https://idea.cesnet.cz/en/index>`__.
    * *Datatype:* ``list of IDEA messages as dictionaries``
``items_count``
    * *Description:* This subkey is present in case search operation was triggered.
      It contains the number of messages in the result set ``items``. By comparing
      this number with the value of ``pager_index_limit`` it is possible to determine,
      if the current result set/page is the last, or whether there are any more
      results.
    * *Datatype:* ``integer``
``pager_index_limit``
    * *Description:* This subkey is present in case search operation was triggered.
      It contains the value of the maximal number of messages, that are returned
      within the single response.
    * *Datatype:* ``integer``
``pager_index_high``
    * *Description:* This subkey is present in case search operation was triggered.
      It contains the index of the last item in the result set with counting beginning
      with ``1``.
    * *Datatype:* ``integer``
``pager_index_low``
    * *Description:* This subkey is present in case search operation was triggered.
      It contains the index of the first item in the result set with counting beginning
      with ``1``.
    * *Datatype:* ``integer``
``query_params``
    * *Description:* This subkey is always present in the response. It contains
      processed search query parameters that the user actually explicitly specified.
    * *Datatype:* ``dictionary``
    * *Example:* ``{"dt_from": "", "submit": "Search"}``
``search_widget_item_limit``
    * *Description:* This subkey is always present in the response. It is intended
      for internal purposes.
    * *Datatype:* ``integer``
``searched``
    * *Description:* This subkey is present in case search operation was triggered.
      It is a simple indication of the successfull search operation.
    * *Datatype:* ``boolean`` always set to ``True``
``sqlquery``
    * *Description:* This subkey is present in case search operation was triggered.
      It contains the actual SQL query, that was issued to the database backend.
    * *Datatype:* ``string``
    * *Example:* ``"b'SELECT * FROM events ORDER BY \"detecttime\" DESC LIMIT 100'"``

**Example usage with curl:**

.. code-block:: shell

    $ curl -X POST -d "api_key=your%AP1_k3y" "https://.../api/events/search?submit=Search"


.. _section-hawat-plugin-events-webapi-show:

API endpoint: **show**
````````````````````````````````````````````````````````````````````````````````

Endpoint URL: ``/api/events/<item_id>/show``

**Response format**

JSON document, that will be received as a response for the search, can contain
following keys:

``item``
    * *Description:* This subkey is present in case requested item exists. It
      contains the IDEA message according to the `IDEA specification <https://idea.cesnet.cz/en/index>`__.
    * *Datatype:* ``IDEA message as dictionary``
``item_id``
    * *Description:* This subkey is present in case requested item exists. It
      contains the identifier of the message.
    * *Datatype:* ``string``
``search_widget_item_limit``
    * *Description:* This subkey is always present in the response. It is intended
      for internal purposes.
    * *Datatype:* ``integer``
``status``
    * *Description:* This subkey is present in case there were any errors in the
      submitted request. So in another words the presence of this subkey is an
      indication of failure. This subkey contains the HTTP status code of the
      error.
    * *Datatype:* ``integer``
``message``
    * *Description:* This subkey is present in case there were any errors in the
      submitted request. So in another words the presence of this subkey is an
      indication of failure. This subkey contains the human readable message
      describing the error that occured.
    * *Datatype:* ``string``

**Example usage with curl:**

.. code-block:: shell

    $ curl -X POST -d "api_key=your%AP1_k3y" "https://.../api/events/event_id/show"


. _section-hawat-plugin-events-webapi-metadata:

API endpoint: **metadata**
````````````````````````````````````````````````````````````````````````````````

Endpoint URL: ``/api/events/metadata``

The main reason for existence of this endpoint is the ability to somehow retrieve
all possible and correct values for various IDEA message attributes. These lists
can be then used for example for rendering some UI widgets.

**Response format**

JSON document, that will be received as a response for the search, can contain
following keys:

``categories``
    * *Description:* This subkey contains all possible values for IDEA message
      categories.
    * *Datatype:* ``list of strings``
``classes``
    * *Description:* This subkey contains all possible values for IDEA message
      classes.
    * *Datatype:* ``list of strings``
``detector_types``
    * *Description:* This subkey contains all possible values for IDEA message
      detector types.
    * *Datatype:* ``list of strings``
``detectors``
    * *Description:* This subkey contains all possible values for IDEA message
      detector names.
    * *Datatype:* ``list of strings``
``host_types``
    * *Description:* This subkey contains all possible values for IDEA message
      host types.
    * *Datatype:* ``list of strings``
``inspection_errs``
    * *Description:* This subkey contains all possible values for IDEA message
      inspection errors.
    * *Datatype:* ``list of strings``
``protocols``
    * *Description:* This subkey contains all possible values for IDEA message
      protocols.
    * *Datatype:* ``list of strings``
``severities``
    * *Description:* This subkey contains all possible values for IDEA message
      severities.
    * *Datatype:* ``list of strings``
``source_types``
    * *Description:* This subkey contains all possible values for IDEA message
      source types.
    * *Datatype:* ``list of strings``
``target_types``
    * *Description:* This subkey contains all possible values for IDEA message
      target types.
    * *Datatype:* ``list of strings``

**Example usage with curl:**

.. code-block:: shell

    $ curl -X POST -d "api_key=your%AP1_k3y" "https://.../api/events/metadata"


API endpoint: **dashboard**
````````````````````````````````````````````````````````````````````````````````

Endpoint URL: ``/api/events/dashboard``

The URL for web API interface is available as normal endpoint to the user of the web
interface. This fact can be used to debug the queries interactively and then simply
copy them to another application. One might for example start with filling in the
search form in the ``/events/dashboard`` endpoint. Once you are satisfied with the
result, you can simply switch the base URL to the ``/api/events/dashboard`` endpoint
and you are all set.


**Available query parameters**:

Following parameters may be specified as standard HTTP query parameters:

``dt_from``
    * *Description:* Lower event detection time boundary
    * *Datatype:* Datetime in the format ``YYYY-MM-DD HH:MM:SS``, for example ``2018-01-01 00:00:00``
    * *Default:* Previous midnight
    * *Note:* Default value kicks in in case the parameter is not specified, explicitly use empty value for boundless search
``dt_to``
    * *Description:* Upper event detection time boundary
    * *Datatype:* Datetime in the format ``YYYY-MM-DD HH:MM:SS``, for example ``2018-01-01 00:00:00``


**Response format**

JSON document, that will be received as a response for the search, can contain
following keys:

``form_data``
    * *Description:* This subkey is present in case search operation was triggered.
      It contains a dictionary with all query parameters described above and their
      appropriate processed values.
    * *Datatype:* ``dictionary``
``form_errors``
    * *Description:* This subkey is present in case there were any errors in the
      submitted search form and the search operation could not be triggered. So
      in another words the presence of this subkey is an indication of search failure.
      This subkey contains list of all form errors as pairs of strings: name of
      the form field and error description. The error description is localized
      according to the user`s preferences.
    * *Datatype:* ``list of tuples of strings``
    * *Example:* ``[["dt_from", "Not a valid datetime value"]]``
``items``
    * *Description:* This subkey is present in case search operation was triggered.
      It contains a list of IDEA messages that matched the query parameters. The
      messages are formated according to the `IDEA specification <https://idea.cesnet.cz/en/index>`__.
    * *Datatype:* ``list of IDEA messages as dictionaries``
``items_count``
    * *Description:* This subkey is present in case search operation was triggered.
      It contains the number of messages in the result set ``items``. By comparing
      this number with the value of ``pager_index_limit`` it is possible to determine,
      if the current result set/page is the last, or whether there are any more
      results.
    * *Datatype:* ``integer``
``query_params``
    * *Description:* This subkey is always present in the response. It contains
      processed search query parameters that the user actually explicitly specified.
    * *Datatype:* ``dictionary``
    * *Example:* ``{"dt_from": "", "submit": "Search"}``
``search_widget_item_limit``
    * *Description:* This subkey is always present in the response. It is intended
      for internal purposes.
    * *Datatype:* ``integer``
``searched``
    * *Description:* This subkey is present in case search operation was triggered.
      It is a simple indication of the successfull search operation.
    * *Datatype:* ``boolean`` always set to ``True``

**Example usage with curl:**

.. code-block:: shell

    $ curl -X POST -d "api_key=your%AP1_k3y" "https://.../api/events/dashboard?submit=Search"

"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import datetime
import pytz

#
# Flask related modules.
#
import flask
from flask_babel import lazy_gettext

#
# Custom modules.
#
import mentat.stats.idea
import mentat.services.eventstorage
from mentat.datatype.sqldb import EventStatisticsModel
from mentat.const import tr_

import hawat.const
import hawat.events
import hawat.acl
from hawat.base import HTMLMixin, PsycopgMixin, AJAXMixin, SQLAlchemyMixin,\
    BaseView, BaseSearchView, ItemShowView, SimpleView, HawatBlueprint,\
    URLParamsBuilder
from hawat.blueprints.events.forms import SimpleEventSearchForm, EventDashboardForm


BLUEPRINT_NAME = 'events'
"""Name of the blueprint as module global constant."""


def _get_enums():
    # Get lists of available options for various event search form select fields.
    enums = {}
    enums.update(
        source_types    = hawat.events.get_event_source_types(),
        target_types    = hawat.events.get_event_target_types(),
        detectors       = hawat.events.get_event_detectors(),
        detector_types  = hawat.events.get_event_detector_types(),
        categories      = hawat.events.get_event_categories(),
        severities      = hawat.events.get_event_severities(),
        classes         = hawat.events.get_event_classes(),
        protocols       = hawat.events.get_event_protocols(),
        inspection_errs = hawat.events.get_event_inspection_errs()
    )
    enums.update(
        host_types = sorted(list(set(enums['source_types'] + enums['target_types']))),
    )
    return enums


class AbstractSearchView(PsycopgMixin, BaseSearchView):  # pylint: disable=locally-disabled,abstract-method
    """
    Base class for view responsible for searching `IDEA <https://idea.cesnet.cz/en/index>`__
    event database and presenting the results.
    """
    authentication = True

    authorization = [hawat.acl.PERMISSION_ANY]

    @classmethod
    def get_menu_title(cls, item = None):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_menu_title`."""
        return lazy_gettext('Events')

    @classmethod
    def get_view_title(cls, item = None):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_view_title`."""
        return lazy_gettext('Search IDEA event database')

    @staticmethod
    def get_search_form(request_args):
        """
        *Interface implementation* of :py:func:`hawat.base.SearchView.get_search_form`.
        """
        # Get lists of available options for various event search form select fields.
        enums = _get_enums()
        choices = {}
        for key, vals in enums.items():
            choices[key] = list(zip(vals, vals))

        return SimpleEventSearchForm(
            request_args,
            meta = {'csrf': False},
            choices_source_types    = choices['source_types'],
            choices_target_types    = choices['target_types'],
            choices_host_types      = choices['host_types'],
            choices_detectors       = choices['detectors'],
            choices_detector_types  = choices['detector_types'],
            choices_categories      = choices['categories'],
            choices_severities      = choices['severities'],
            choices_classes         = choices['classes'],
            choices_protocols       = choices['protocols'],
            choices_inspection_errs = choices['inspection_errs'],
        )

    def do_before_search(self, form_data):  # pylint: disable=locally-disabled,no-self-use,unused-argument
        """
        *Interface implementation* of :py:func:`hawat.base.SearchView.do_before_search`.
        """
        form_data['groups'] = [item.name for item in form_data['groups']]


class SearchView(HTMLMixin, AbstractSearchView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for querying `IDEA <https://idea.cesnet.cz/en/index>`__
    event database and presenting the results in the form of HTML page.
    """
    methods = ['GET']

    @classmethod
    def get_breadcrumbs_menu(cls):
        """
        *Interface implementation* of :py:func:`hawat.base.SearchView.get_breadcrumbs_menu`.
        """
        breadcrumbs_menu = hawat.menu.HawatMenu()
        breadcrumbs_menu.add_entry(
            'endpoint',
            'home',
            endpoint = flask.current_app.config['HAWAT_ENDPOINT_HOME']
        )
        breadcrumbs_menu.add_entry(
            'endpoint',
            'search',
            endpoint = '{}.search'.format(cls.module_name)
        )
        return breadcrumbs_menu

    @classmethod
    def get_context_action_menu(cls):
        """
        *Interface implementation* of :py:func:`hawat.base.SearchView.get_context_action_menu`.
        """
        action_menu = hawat.menu.HawatMenu()
        action_menu.add_entry(
            'endpoint',
            'show',
            endpoint = 'events.show',
            hidetitle = True
        )
        action_menu.add_entry(
            'endpoint',
            'download',
            endpoint = 'events.download',
            hidetitle = True
        )
        return action_menu


class APISearchView(AJAXMixin, AbstractSearchView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for querying `IDEA <https://idea.cesnet.cz/en/index>`__
    event database and presenting the results in the form of JSON document.
    """
    methods = ['GET','POST']

    @classmethod
    def get_view_name(cls):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_view_name`."""
        return 'apisearch'


class AbstractShowView(PsycopgMixin, ItemShowView):  # pylint: disable=locally-disabled,abstract-method
    """
    Base class responsible for fetching and presenting single `IDEA <https://idea.cesnet.cz/en/index>`__
    message.
    """
    authentication = True

    authorization = [hawat.acl.PERMISSION_ANY]

    @classmethod
    def get_menu_title(cls, item = None):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_menu_title`."""
        return lazy_gettext('Show IDEA event')

    @classmethod
    def get_menu_legend(cls, item = None):
        """
        *Interface implementation* of :py:func:`hawat.base.BaseView.get_menu_legend`.
        """
        return lazy_gettext('View details of event &quot;%(item)s&quot;', item = item.get_id())


class ShowView(HTMLMixin, AbstractShowView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    Detailed `IDEA <https://idea.cesnet.cz/en/index>`__ message view that presents
    the result as HTML page.
    """
    methods = ['GET']

    @classmethod
    def get_action_menu(cls):  # pylint: disable=locally-disabled,unused-argument
        """
        *Interface implementation* of :py:func:`hawat.base.SearchView.get_action_menu`.
        """
        action_menu = hawat.menu.HawatMenu()
        action_menu.add_entry(
            'endpoint',
            'download',
            endpoint = 'events.download'
        )
        return action_menu


class APIShowView(AJAXMixin, AbstractShowView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    Detailed `IDEA <https://idea.cesnet.cz/en/index>`__ message view that presents
    the result as HTML page.
    """
    methods = ['GET','POST']

    @classmethod
    def get_view_name(cls):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_view_name`."""
        return 'apishow'


class DownloadView(PsycopgMixin, BaseView):
    """
    Download `IDEA <https://idea.cesnet.cz/en/index>`__ event view.
    """
    methods = ['GET']

    authentication = True

    authorization = [hawat.acl.PERMISSION_ANY]

    @classmethod
    def get_view_name(cls):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_view_name`."""
        return 'download'

    @classmethod
    def get_menu_title(cls, item = None):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_menu_title`."""
        return lazy_gettext('Download')

    @classmethod
    def get_menu_legend(cls, item = None):
        """
        *Interface implementation* of :py:func:`hawat.base.BaseView.get_menu_legend`.
        """
        return lazy_gettext('Download event &quot;%(item)s&quot;', item = item.get_id())

    @classmethod
    def get_menu_link(cls, item = None):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_menu_link`."""
        return flask.url_for(cls.get_view_endpoint(), item_id = item.get_id())

    #---------------------------------------------------------------------------

    def dispatch_request(self, item_id):  # pylint: disable=locally-disabled,arguments-differ
        """
        Mandatory interface required by the :py:func:`flask.views.View.dispatch_request`.
        Will be called by the *Flask* framework to service the request.

        Single item with given unique identifier will be retrieved from database
        and injected into template to be displayed to the user.
        """
        item = self.fetch(item_id)
        if not item:
            flask.abort(404)

        self.logger.debug(
            "IDEA event %s is being downloaded as a standalone file.",
            item['ID']
        )

        response = flask.make_response(
            item.to_json(indent = 4, sort_keys = True)
        )
        response.mimetype = 'application/json'
        response.headers['Content-Disposition'] = 'attachment; filename={}.idea.json'.format(item_id)
        return response


class AbstractDashboardView(SQLAlchemyMixin, BaseSearchView):  # pylint: disable=locally-disabled,abstract-method
    """
    Base class for presenting overall `IDEA <https://idea.cesnet.cz/en/index>`__
    event statistics dashboard.
    """
    authentication = True

    authorization = [hawat.acl.PERMISSION_ANY]

    @classmethod
    def get_menu_icon(cls):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_menu_icon`."""
        return 'module-{}'.format(BLUEPRINT_NAME)

    @classmethod
    def get_menu_title(cls, item = None):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_menu_title`."""
        return lazy_gettext('Events')

    @classmethod
    def get_view_title(cls, item = None):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_view_title`."""
        return lazy_gettext('Overall event dashboards')

    @classmethod
    def get_view_template(cls):
        """*Implementation* of :py:func:`hawat.base.RenderableView.get_view_template`."""
        return '{}/{}.html'.format(cls.module_name, cls.get_view_name())

    #---------------------------------------------------------------------------

    @property
    def dbmodel(self):
        """*Implementation* of :py:func:`hawat.base.SQLAlchemyMixin.dbmodel`."""
        return EventStatisticsModel

    @staticmethod
    def get_search_form(request_args):
        """
        *Interface implementation* of :py:func:`hawat.base.SearchView.get_search_form`.
        """
        return EventDashboardForm(request_args, meta = {'csrf': False})

    @staticmethod
    def build_query(query, model, form_args):
        """
        *Interface implementation* of :py:func:`hawat.base.SQLAlchemyMixin.build_query`.
        """
        # Adjust query based on lower time boudary selection.
        if 'dt_from' in form_args and form_args['dt_from']:
            query = query.filter(model.dt_from >= form_args['dt_from'])
        # Adjust query based on upper time boudary selection.
        if 'dt_to' in form_args and form_args['dt_to']:
            query = query.filter(model.dt_to <= form_args['dt_to'])

        # Return the result sorted by interval.
        return query.order_by(model.interval)

    def do_after_search(self, items):
        """
        *Interface implementation* of :py:func:`hawat.base.SearchView.do_after_search`.
        """
        self.logger.debug(
            "Calculating IDEA event dashboard overview from %d records.",
            len(items)
        )
        if items:
            dt_from = self.response_context['form_data'].get('dt_from', None)
            if dt_from:
                dt_from = dt_from.astimezone(pytz.utc)
                dt_from = dt_from.replace(tzinfo = None)
            dt_to   = self.response_context['form_data'].get('dt_to', None)
            if dt_to:
                dt_to = dt_to.astimezone(pytz.utc)
                dt_to = dt_to.replace(tzinfo = None)

            if not dt_from:
                dt_from = self.dbcolumn_min(self.dbmodel.createtime)
            if not dt_to:
                dt_to = datetime.datetime.utcnow()

            self.response_context.update(
                statistics = mentat.stats.idea.aggregate_timeline_groups(
                    items,
                    dt_from = dt_from,
                    dt_to = dt_to,
                    max_count = flask.current_app.config['HAWAT_CHART_TIMELINE_MAXSTEPS'],
                    min_step = 300
                )
            )

    def do_before_response(self, **kwargs):
        """*Implementation* of :py:func:`hawat.base.RenderableView.do_before_response`."""
        self.response_context.update(
            quicksearch_list = self.get_quicksearch_by_time()
        )


class DashboardView(HTMLMixin, AbstractDashboardView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for presenting overall `IDEA <https://idea.cesnet.cz/en/index>`__
    event statistics dashboard in the form of HTML page.
    """

    @classmethod
    def get_view_name(cls):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_view_name`."""
        return 'dashboard'


class APIDashboardView(AJAXMixin, AbstractDashboardView):  # pylint: disable=locally-disabled,too-many-ancestors
    """
    View responsible for presenting overall `IDEA <https://idea.cesnet.cz/en/index>`__
    event statistics dashboard in the form of HTML page.
    """

    @classmethod
    def get_view_name(cls):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_view_name`."""
        return 'apidashboard'


class APIMetadataView(AJAXMixin, SimpleView):
    """
    Application view providing access event database status information.
    """
    authentication = True

    authorization = [hawat.acl.PERMISSION_ANY]

    @classmethod
    def get_view_name(cls):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_view_name`."""
        return 'metadata'

    @classmethod
    def get_menu_title(cls, item = None):
        """*Implementation* of :py:func:`hawat.base.BaseView.get_menu_title`."""
        return lazy_gettext('Event metadata')

    def do_before_response(self, **kwargs):
        """*Implementation* of :py:func:`hawat.base.RenderableView.do_before_response`."""
        self.response_context.update(**_get_enums())


#-------------------------------------------------------------------------------


class EventsBlueprint(HawatBlueprint):
    """
    Hawat pluggable module - IDEA events.
    """

    @classmethod
    def get_module_title(cls):
        """*Implementation* of :py:func:`hawat.base.HawatBlueprint.get_module_title`."""
        return lazy_gettext('IDEA events pluggable module')

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
            'dashboards.{}'.format(BLUEPRINT_NAME),
            position = 10,
            view = DashboardView
        )
        app.menu_main.add_entry(
            'view',
            BLUEPRINT_NAME,
            position = 140,
            view = SearchView,
            resptitle = True
        )

        # Register context search actions provided by this module.
        app.set_csag(
            hawat.const.HAWAT_CSAG_ABUSE,
            tr_('Search for abuse group <strong>%(name)s</strong> in event database'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('groups', True)
        )

        app.set_csag(
            hawat.const.HAWAT_CSAG_ADDRESS,
            tr_('Search for source <strong>%(name)s</strong> in event database'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('source_addrs', True)
        )
        app.set_csag(
            hawat.const.HAWAT_CSAG_ADDRESS,
            tr_('Search for target <strong>%(name)s</strong> in event database'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('target_addrs', True)
        )
        app.set_csag(
            hawat.const.HAWAT_CSAG_ADDRESS,
            tr_('Search for host <strong>%(name)s</strong> in event database'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('host_addrs', True)
        )

        app.set_csag(
            hawat.const.HAWAT_CSAG_CATEGORY,
            tr_('Search for category <strong>%(name)s</strong> in event database'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('categories', True)
        )

        app.set_csag(
            hawat.const.HAWAT_CSAG_CLASS,
            tr_('Search for class <strong>%(name)s</strong> in event database'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('classes', True)
        )

        app.set_csag(
            hawat.const.HAWAT_CSAG_DETECTOR,
            tr_('Search for detector <strong>%(name)s</strong> in event database'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('detectors', True)
        )

        app.set_csag(
            hawat.const.HAWAT_CSAG_DETTYPE,
            tr_('Search for detector type <strong>%(name)s</strong> in event database'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('detector_types', True)
        )

        app.set_csag(
            hawat.const.HAWAT_CSAG_HOSTTYPE,
            tr_('Search for source type <strong>%(name)s</strong> in event database'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('source_types', True)
        )
        app.set_csag(
            hawat.const.HAWAT_CSAG_HOSTTYPE,
            tr_('Search for target type <strong>%(name)s</strong> in event database'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('target_types', True)
        )
        app.set_csag(
            hawat.const.HAWAT_CSAG_HOSTTYPE,
            tr_('Search for host type <strong>%(name)s</strong> in event database'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('host_types', True)
        )

        app.set_csag(
            hawat.const.HAWAT_CSAG_PORT,
            tr_('Search for source port <strong>%(name)s</strong> in event database'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('source_ports', True)
        )
        app.set_csag(
            hawat.const.HAWAT_CSAG_PORT,
            tr_('Search for target port <strong>%(name)s</strong> in event database'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('target_ports', True)
        )
        app.set_csag(
            hawat.const.HAWAT_CSAG_PORT,
            tr_('Search for host port <strong>%(name)s</strong> in event database'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('host_ports', True)
        )

        app.set_csag(
            hawat.const.HAWAT_CSAG_PROTOCOL,
            tr_('Search for protocol <strong>%(name)s</strong> in event database'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('protocols', True)
        )

        app.set_csag(
            hawat.const.HAWAT_CSAG_SEVERITY,
            tr_('Search for severity <strong>%(name)s</strong> in event database'),
            SearchView,
            URLParamsBuilder({'submit': tr_('Search')}).add_rule('severities', True)
        )


#-------------------------------------------------------------------------------


def get_blueprint():
    """
    Mandatory interface and factory function. This function must return a valid
    instance of :py:class:`hawat.base.HawatBlueprint` or :py:class:`flask.Blueprint`.
    """

    hbp = EventsBlueprint(
        BLUEPRINT_NAME,
        __name__,
        template_folder = 'templates'
    )

    hbp.register_view_class(SearchView,       '/{}/search'.format(BLUEPRINT_NAME))
    hbp.register_view_class(ShowView,         '/{}/<item_id>/show'.format(BLUEPRINT_NAME))
    hbp.register_view_class(DownloadView,     '/{}/<item_id>/download'.format(BLUEPRINT_NAME))
    hbp.register_view_class(DashboardView,    '/{}/dashboard'.format(BLUEPRINT_NAME))
    hbp.register_view_class(APISearchView,    '/api/{}/search'.format(BLUEPRINT_NAME))
    hbp.register_view_class(APIShowView,      '/api/{}/<item_id>/show'.format(BLUEPRINT_NAME))
    hbp.register_view_class(APIDashboardView, '/api/{}/dashboard'.format(BLUEPRINT_NAME))
    hbp.register_view_class(APIMetadataView,  '/api/{}/metadata'.format(BLUEPRINT_NAME))

    return hbp
