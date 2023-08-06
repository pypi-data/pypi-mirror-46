#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
 File: statement.py
 File Created: Thursday, 14th February 2019 3:20:33 pm
 Author: ESR - Romeren (emilromer@hotmail.com)
 -----
 Copyright 2019 OpenSourced, OpenSourced
 -----
 Last Modified:
 Date	By	Comments
 -----
"""

# import six
from influxed.ifql.functions import Func
from influxed.ifql.column import Column
from influxed.ifql.util import ORDER, COMPARISON_OPERATOR, OPERATOR, KEY_WORDS
from influxed.ifql.filter import where_filter
from influxed.ifql.exceptions import MissingArgument


class a_statement(object):
    
    def __init__(self, hook=None):
        self._measurement = None
        self._show_key_word = None
        self._limit = None
        self._order = None
        self._fill = None
        self._order_by = []
        self._group_by = []
        self._into_series = None
        self._select_expressions = []
        self._default_operator = COMPARISON_OPERATOR.eq
        self._default_chaining_operator = OPERATOR.and_
        self._where = where_filter(self._default_chaining_operator)
        self._is_delete = False
        self.database = None
        self.hook = hook

    def on(self, database):
        self.database = database
        return self

    def _format(self):
        raise NotImplementedError

    def format(self):
        return self._format().strip()

    def exec(self):
        """
            Execute a statement on the hook and return the result
        """
        if(self.hook):
            return self.hook.execute(self)
        return self.format()

class uses_from(object):
    
    def __init__(self, isRequired=False):
        self.isRequired = isRequired

    def from_(self, measurement):
        self._measurement = measurement
        return self

    def _format_measurement(self, measurement):
        if(isinstance(measurement, a_statement)):
            return f"({measurement.format()})"
        enquote = (
            not (measurement[0] == '/' and measurement[-1] == '/')
            and (" " in measurement or "-" in measurement))
        if enquote:
            return '"%s"' % measurement
        return measurement

    def _format_from(self):
        if(self._measurement is None and self.isRequired):
            raise MissingArgument('No measurement passed to FROM argument. please use .from_(<measurement>) to specify')
        elif(self._measurement is None):
            return ''
        return f"FROM {self._format_measurement(self._measurement)}" 


class common_statement_formatter(a_statement, uses_from):

    def __init__(self, hook=None):
        a_statement.__init__(self, hook=hook)
        uses_from.__init__(self, isRequired=False)

    def _format_where(self):
        if self._where.empty:
            return ''

        return f"WHERE {self._where._format()}"

    def _format_delete_query(self):
        query = f"DELETE {self._format_from()} {self._format_where()}"
        return query

    def _format_show_query(self):
        if(isinstance(self._show_key_word, KEY_WORDS)):
            return f'SHOW {self._show_key_word._value_} {self._format_from()}'
        return f'SHOW {self._show_key_word} {self._format_from()}'

    def all(self):
        """
            Fetch all rows
        """
        return self.exec()
        
class dummy_statement(common_statement_formatter):
    
    def __init__(self, query, database):
        self.query = query
        self.database = database
    
    def _format(self):
        return self.query
