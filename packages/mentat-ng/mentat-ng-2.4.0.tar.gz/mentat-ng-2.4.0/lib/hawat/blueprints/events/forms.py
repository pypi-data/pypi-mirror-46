#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
This module contains custom internal event search form for Hawat.
"""


__author__ = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import wtforms
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

import flask_wtf
from flask_babel import lazy_gettext

import hawat.const
import hawat.db
import hawat.forms
from mentat.datatype.sqldb import GroupModel


def get_available_groups():
    """
    Query the database for list of all available groups.
    """
    return hawat.db.db_query(GroupModel).order_by(GroupModel.name).all()


class SimpleEventSearchForm(hawat.forms.BaseSearchForm):
    """
    Class representing simple event search form.
    """
    dt_from = hawat.forms.DateTimeLocalField(
        lazy_gettext('Detection time from:'),
        validators = [
            wtforms.validators.Optional()
        ],
        format = '%Y-%m-%d %H:%M:%S'
    )
    dt_to = hawat.forms.DateTimeLocalField(
        lazy_gettext('Detection time to:'),
        validators = [
            wtforms.validators.Optional()
        ],
        format = '%Y-%m-%d %H:%M:%S'
    )
    st_from = hawat.forms.DateTimeLocalField(
        lazy_gettext('Storage time from:'),
        validators = [
            wtforms.validators.Optional()
        ],
        format = '%Y-%m-%d %H:%M:%S'
    )
    st_to = hawat.forms.DateTimeLocalField(
        lazy_gettext('Storage time to:'),
        validators = [
            wtforms.validators.Optional()
        ],
        format = '%Y-%m-%d %H:%M:%S'
    )
    source_addrs = hawat.forms.CommaListField(
        lazy_gettext('Source addresses:'),
        validators = [
            wtforms.validators.Optional(),
            hawat.forms.check_network_record_list
        ],
        widget = wtforms.widgets.TextArea()
    )
    target_addrs = hawat.forms.CommaListField(
        lazy_gettext('Target addresses:'),
        validators = [
            wtforms.validators.Optional(),
            hawat.forms.check_network_record_list
        ],
        widget = wtforms.widgets.TextArea()
    )
    host_addrs = hawat.forms.CommaListField(
        lazy_gettext('Host addresses:'),
        validators = [
            wtforms.validators.Optional(),
            hawat.forms.check_network_record_list
        ],
        widget = wtforms.widgets.TextArea()
    )
    source_ports = hawat.forms.CommaListField(
        lazy_gettext('Source ports:'),
        validators = [
            wtforms.validators.Optional(),
            hawat.forms.check_port_list
        ]
    )
    target_ports = hawat.forms.CommaListField(
        lazy_gettext('Target ports:'),
        validators = [
            wtforms.validators.Optional(),
            hawat.forms.check_port_list
        ]
    )
    host_ports = hawat.forms.CommaListField(
        lazy_gettext('Host ports:'),
        validators = [
            wtforms.validators.Optional(),
            hawat.forms.check_port_list
        ]
    )
    source_types = wtforms.SelectMultipleField(
        lazy_gettext('Source types:'),
        validators = [
            wtforms.validators.Optional()
        ],
        choices = [],
        filters = [lambda x: x or []]
    )
    target_types = wtforms.SelectMultipleField(
        lazy_gettext('Target types:'),
        validators = [
            wtforms.validators.Optional()
        ],
        choices = [],
        filters = [lambda x: x or []]
    )
    host_types = wtforms.SelectMultipleField(
        lazy_gettext('Host types:'),
        validators = [
            wtforms.validators.Optional()
        ],
        choices = [],
        filters = [lambda x: x or []]
    )
    detectors = wtforms.SelectMultipleField(
        lazy_gettext('Detectors:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [
            ('__EMPTY__', lazy_gettext('<< without value >>')),
            ('__ANY__', lazy_gettext('<< any value >>'))
        ],
        filters = [lambda x: x or []]
    )
    not_detectors = wtforms.BooleanField(
        lazy_gettext('Negate detector selection:'),
        validators = [
            wtforms.validators.Optional(),
        ]
    )
    detector_types = wtforms.SelectMultipleField(
        lazy_gettext('Detector types:'),
        validators = [
            wtforms.validators.Optional()
        ],
        choices = [
            ('__EMPTY__', lazy_gettext('<< without value >>')),
            ('__ANY__', lazy_gettext('<< any value >>'))
        ],
        filters = [lambda x: x or []]
    )
    not_detector_types = wtforms.BooleanField(
        lazy_gettext('Negate detector_type selection:'),
        validators = [
            wtforms.validators.Optional(),
        ]
    )
    categories = wtforms.SelectMultipleField(
        lazy_gettext('Categories:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [
            ('__EMPTY__', lazy_gettext('<< without value >>')),
            ('__ANY__', lazy_gettext('<< any value >>'))
        ],
        filters = [lambda x: x or []]
    )
    not_categories = wtforms.BooleanField(
        lazy_gettext('Negate category selection:'),
        validators = [
            wtforms.validators.Optional(),
        ]
    )
    severities = wtforms.SelectMultipleField(
        lazy_gettext('Severities:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [
            ('__EMPTY__', lazy_gettext('<< without value >>')),
            ('__ANY__', lazy_gettext('<< any value >>'))
        ],
        filters = [lambda x: x or []]
    )
    not_severities = wtforms.BooleanField(
        lazy_gettext('Negate severity selection:'),
        validators = [
            wtforms.validators.Optional(),
        ]
    )
    classes = wtforms.SelectMultipleField(
        lazy_gettext('Classes:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [
            ('__EMPTY__', lazy_gettext('<< without value >>')),
            ('__ANY__', lazy_gettext('<< any value >>'))
        ],
        filters = [lambda x: x or []]
    )
    not_classess = wtforms.BooleanField(
        lazy_gettext('Negate class selection:'),
        validators = [
            wtforms.validators.Optional(),
        ]
    )
    description = wtforms.StringField(
        lazy_gettext('Description:'),
        validators = [
            wtforms.validators.Optional()
        ]
    )
    protocols = wtforms.SelectMultipleField(
        lazy_gettext('Protocols:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [
            ('__EMPTY__', lazy_gettext('<< without value >>')),
            ('__ANY__', lazy_gettext('<< any value >>'))
        ],
        filters = [lambda x: x or []]
    )
    not_protocols = wtforms.BooleanField(
        lazy_gettext('Negate protocol selection:'),
        validators = [
            wtforms.validators.Optional(),
        ]
    )
    groups = QuerySelectMultipleField(
        lazy_gettext('Abuse group:'),
        query_factory = get_available_groups,
        allow_blank = False,
        get_pk = lambda item: item.name
    )
    not_groups = wtforms.BooleanField(
        lazy_gettext('Negate group selection:'),
        validators = [
            wtforms.validators.Optional(),
        ]
    )
    inspection_errs = wtforms.SelectMultipleField(
        lazy_gettext('Inspection errors:'),
        validators = [
            wtforms.validators.Optional(),
        ],
        choices = [
            ('__EMPTY__', lazy_gettext('<< without value >>')),
            ('__ANY__', lazy_gettext('<< any value >>'))
        ],
        filters = [lambda x: x or []]
    )
    not_inspection_errs = wtforms.BooleanField(
        lazy_gettext('Negate inspection error selection:'),
        validators = [
            wtforms.validators.Optional(),
        ]
    )

    sortby = wtforms.SelectField(
        lazy_gettext('Sort by:'),
        validators = [
            wtforms.validators.Optional()
        ],
        choices = [
            ('time.desc', lazy_gettext('by time descending')),
            ('time.asc',  lazy_gettext('by time ascending')),
            ('detecttime.desc', lazy_gettext('by detection time descending')),
            ('detecttime.asc',  lazy_gettext('by detection time ascending')),
            ('storagetime.desc', lazy_gettext('by storage time descending')),
            ('storagetime.asc',  lazy_gettext('by storage time ascending'))
        ],
        default = 'time.desc'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.source_types.choices   = kwargs['choices_source_types']
        self.target_types.choices   = kwargs['choices_target_types']
        self.host_types.choices     = kwargs['choices_host_types']

        self.detectors.choices[2:]       = kwargs['choices_detectors']
        self.detector_types.choices[2:]  = kwargs['choices_detector_types']
        self.categories.choices[2:]      = kwargs['choices_categories']
        self.severities.choices[2:]      = kwargs['choices_severities']
        self.classes.choices[2:]         = kwargs['choices_classes']
        self.protocols.choices[2:]       = kwargs['choices_protocols']
        self.inspection_errs.choices[2:] = kwargs['choices_inspection_errs']

    @staticmethod
    def is_multivalue(field_name):
        """
        Check, if given form field is a multivalue field.

        :param str field_name: Name of the form field.
        :return: ``True``, if the field can contain multiple values, ``False`` otherwise.
        :rtype: bool
        """
        if field_name in ('source_addrs', 'target_addrs', 'host_addrs', 'source_ports', 'target_ports', 'host_ports', 'source_types', 'target_types', 'host_types', 'detectors', 'detector_types', 'categories', 'severities', 'classess', 'protocols', 'groups', 'inspection_errs'):
            return True
        return False


class EventDashboardForm(flask_wtf.FlaskForm):
    """
    Class representing event dashboard search form.
    """
    dt_from = hawat.forms.DateTimeLocalField(
        lazy_gettext('From:'),
        validators = [
            wtforms.validators.Optional()
        ],
        format = '%Y-%m-%d %H:%M:%S',
        default = lambda: hawat.forms.default_dt_with_delta(hawat.const.HAWAT_DEFAULT_RESULT_TIMEDELTA)
    )
    dt_to = hawat.forms.DateTimeLocalField(
        lazy_gettext('To:'),
        validators = [
            wtforms.validators.Optional()
        ],
        format = '%Y-%m-%d %H:%M:%S'
    )
    submit = wtforms.SubmitField(
        lazy_gettext('Search')
    )
