# -*- coding: utf-8 -*-
"""
Custom xpath functions available from `ciur` namespaces.
This namespace is identified by the namespace prefix ciur:, which is a
predefined prefix in this context of this lib.
This document describes implementation of function namespace
https://bitbucket.org/ada/ciur/src/docs/2016/xpath-functions

NOTE:
    local convention for all public cast function is `[a-z]+[a-z0-9_]+_`
    it should end with underscore
"""

from decimal import Decimal


import html
from html.parser import HTMLParser
from urllib.parse import urlparse
from dateutil import parser
from lxml.etree import tostring

from ciur.helpers import load_xpath_functions
from ciur.helpers import element2text
from ciur.decorators import check_new_node
from ciur.decorators import convert_element2text
from ciur.exceptions import CiurBaseException
from ciur.dateutil_aditional_languages import MONTHS


def url_(url, base_url):
    """
    get absolute url
    """
    return urlparse.urljoin(base_url, url)


def url_param_(url, param, *_):
    """
    get param from url
    """
    parsed = urlparse.urlparse(url)
    return urlparse.parse_qs(parsed.query)[param]


@convert_element2text
def fn_int(context, value, *_):
    """
    convert data into integer
    :param context: Parent DOM context
        :type context: EtreeElement
    :param value:
        :type value: basestring
    :param _: unused

    :rtype: int
    """
    del context

    return int(value)


def fn_raw(context, value, *_):
    """
    get raw representation of DOM
    :param context: Parent DOM context
        :type context: EtreeElement
    :param value:
        :type value: EtreeElement or basestring
    :param _: unused args
    """
    del context

    if isinstance(value, str):
        return value

    raw_html = tostring(value).decode()
    return html.unescape(raw_html)


def fn_iraw(context, value, *_):
    """
    get raw representation of children DOM aka innerHTML

    :param context: Parent DOM context
        :type context: EtreeElement
    :param value:
        :type value: EtreeElement or basestring
    :param _: unused args
    """

    text = value.text.strip() if value.text else ""
    tail = value.tail.strip() if value.tail else ""
    if tail:
        tail = " " + tail

    return text + "".join(fn_raw(context, child) for child in value) + tail


def size_(got, mandatory_or_optional, expect):
    """
    check if expected size match result size
    """
    if mandatory_or_optional == "mandatory":
        if not got:  # + got 0
            assert False, "expect mandatory"
        elif expect is 0:  # +0 got 1
            pass
        else:  # +10 got 1
            assert got == expect, "expect size `%s`, got `%s`" % (expect, got)
    else:
        if not got:  # * got 0
            pass
        elif expect is 0:  # * got 19
            pass
        else:  # *5 got 5
            assert got == expect, "expect size `%s`, got `%s`" % (expect, got)


@convert_element2text
def fn_datetime(context, value):
    """
    because of exception (bellow) string do datetime CAN NOT be embedded
    into lxml namespace functions:

        File "extensions.pxi", line 612, in lxml.etree._wrapXPathObject
        (src/lxml/lxml.etree.c:145847)
        lxml.etree.XPathResultError: Unknown return type: datetime.datetime

    So this is the reason why it is implemented in type_list casting chain
    """
    del context

    text = element2text(value)

    if not text:
        return value

    for foreign, english in MONTHS.items():
        text = text.replace(foreign, english)

    try:
        return parser.parse(text)
    except (ValueError,) as value_error:
        raise CiurBaseException(value_error, {"text": text})


@convert_element2text
@check_new_node
def fn_float(context, text):
    """
    workaround for fn:number
    http://stackoverflow.com/questions/33789196/is-xpath-number-function-lies

    :param context: Parent DOM context
        :type context: EtreeElement
    :param text:
        :type text: basestring
    :return: float or None
    """
    # TODO: move from cast_
    del context

    if text in ["", None]:
        return None

    try:
        return float(text)
    except (ValueError,) as value_error:
        if "invalid literal for float()" in value_error.message:
            return float(text.replace(",", "."))
        else:
            raise value_error


@check_new_node
def fn_tail(context, value):
    """
    >> xpath(<div><p>paragraph</p>tail_text</div>).tail
    tail_text
    :param context: Parent DOM context
        :type context: EtreeElement

    :param value:
        :type value: EtreeElement or basestring
    :rtype str
    """
    del context

    return value.tail

@convert_element2text
def fn_text(context, value):
    """
    del context
    """

    return value


@convert_element2text
def fn_decimal(context, value, *_):
    """
    convert textual into Decimal (required for AWS Dynamodb)
    :param context: Parent DOM context
        :type context: EtreeElement
    :param value:
        :type value: basestring
    :param _: unused

    :rtype: decimal
    """
    del context

    return Decimal(value)



HTML_PARSER = HTMLParser()

load_xpath_functions(locals())
