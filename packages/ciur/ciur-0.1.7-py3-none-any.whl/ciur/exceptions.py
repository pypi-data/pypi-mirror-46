"""
ciur.exceptions
~~~~~~~~~~~~~~~~~~~

This module contains the set of Ciur' exceptions.

"""
import os

from pyparsing import ParseBaseException


class CiurBaseException(BaseException):
    """
    exception class used in ciur
    """
    def __init__(self, data, *args, **kwargs):
        """
        Initialize RequestException with `data`
        """
        BaseException.__init__(self, *args, **kwargs)
        self._data = data

    def __str__(self):
        """
        Display also data
        :rtype: str
        """
        return "%s, %s" % (BaseException.__str__(self), self._data)


class ParseExceptionInCiurFile(ParseBaseException):
    """
    Give more humanity to exceptions raises by `pyparsing.py`
    """
    def __init__(self, file_string, file_name, parse_error):
        """
        introduce also origins of dsl file
        :param file_string:
        :param file_name:
        :param parse_error:
        """
        ParseBaseException.__init__(
            self, parse_error.pstr, parse_error.loc,
            parse_error.msg, parse_error.parserElement
        )
        self._file_string = file_string.splitlines()        
            
        self._file_name = None if not file_name else os.path.abspath(file_name)

    def __str__(self):
        buf = "|from file `%s`" % self._file_name \
            if self._file_name else "from string"

        lineno = self.lineno - 1
        line = "%s" % lineno
        cursor_position = self.col + 1 + len(line)
        
        if lineno == len(self._file_string):
            lineno -= 1            
            cursor_position += len(self._file_string[-1]) + 1 
            
        return "%s,\n    %s \n    |%s: %s\n    %s^" % (
            ParseBaseException.__str__(self),
            buf,
            line,
            self._file_string[lineno],
            " " * cursor_position
        )
