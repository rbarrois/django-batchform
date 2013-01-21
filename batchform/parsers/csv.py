# -*- coding: utf-8 -*-
# This code is distributed under the two-clause BSD license.
# Copyright (c) 2013 Raphaël Barrois


"""Handle CSV file formats.

This provides a whole batch of custom CSV parsers, based on either CSV dialects
or explicit delimiter/quotechar setting.

The most user-friendly parser is AutoDialectCsvParser, that will attempt to
detect the dialect from the files content.

Alternately:
    - For a specific dialect, use DialectCsvParser(dialect='my_dialect')
    - For a specific quote/delimiter configuration, use
      ExplicitCsvParser(quotechar='"', delimiter=';')
"""


from __future__ import absolute_import


import csv

from . import base


class BaseCsvParser(base.BaseParser):
    def get_reader_kwargs(self, file_obj):
        """Prepare reader args for a given file."""
        return {}

    def parse_file(self, file_obj):
        reader_kwargs = self.get_reader_kwargs(file_obj)

        reader = csv.reader(file_obj, **reader_kwargs)
        return list(reader)


class DialectCsvParser(BaseCsvParser):
    def __init__(self, dialect='excel', *args, **kwargs):
        # 'excel' is the default dialect for the csv module.
        self.dialect = dialect
        super(DialectCsvParser, self).__init__(*args, **kwargs)

    def get_dialect(self, file_obj):
        return self.dialect

    def get_reader_kwargs(self, file_obj):
        return {
            'dialect': self.get_dialect(file_obj),
        }


class AutoDialectCsvParser(DialectCsvParser):
    def get_dialect(self, file_obj):
        file_obj.open('U')
        dialect = csv.Sniffer().sniff(file_obj.read(1024))
        file_obj.seek(0)
        return dialect


class ExplicitCsvParser(BaseCsvParser):

    def __init__(self, quotechar='"', delimiter=',', *args, **kwargs):
        self.quotechar = quotechar
        self.delimiter = delimiter
        super(ExplicitCsvParser, self).__init__(*args, **kwargs)

    def get_reader_kwargs(self, file_obj):
        return {
            'quotechar': self.quotechar,
            'delimiter': self.delimiter,
        }
