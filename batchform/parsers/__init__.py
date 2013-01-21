# -*- coding: utf-8 -*-


class ParserError(Exception):
    """Raised for all parser-related errors."""


class BaseParser(object):
    """Base class for all file parsers.

    A file parser's role is to read a raw, binary file and return lists of rows,
    where a row is a list of cell value (either text or a more adequate Python
    value).
    """

    def parse_file(self, file_obj):
        """Parse a file data (the raw file object)."""
        raise ParserError(u"Unable to parse file.")


class CSVParser(BaseParser):
    def parse_file(self, file_obj):
        for line in file_obj:
            yield line.strip().split(';')
