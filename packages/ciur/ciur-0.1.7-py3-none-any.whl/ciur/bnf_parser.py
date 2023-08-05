"""
ciur external dsl

FIXME: using russian characters in pyparsing

>>> import pprint
>>> bnf = _get_bnf()

example.com.doctest
===================
>>> rules = '''
... root `/html/body` +1
...    name `.//h1/text()` +1
...    paragraph `.//p/text()` +1
... '''

>>> pprint.pprint(external2list(rules))
[['root',
  'xpath',
  '/html/body',
  ['+1'],
  [['name', 'xpath', './/h1/text()', ['+1']],
   ['paragraph', 'xpath', './/p/text()', ['+1']]]]]

import.io_jobs.doctest
======================
>>> rules = '''
... root `/jobs/job` +
...
...     title `./title/text()` +
...     url `./url/text()` +1
...     location `.` *
...         country `./country/text()` +1
...         city `./city/text()` +1
...         zip `./postalcode/text()` *1
... '''
>>> pprint.pprint(external2list(rules))
[['root',
  'xpath',
  '/jobs/job',
  ['+'],
  [['title', 'xpath', './title/text()', ['+']],
   ['url', 'xpath', './url/text()', ['+1']],
   ['location',
    'xpath',
    '.',
    ['*'],
    [['country', 'xpath', './country/text()', ['+1']],
     ['city', 'xpath', './city/text()', ['+1']],
     ['zip', 'xpath', './postalcode/text()', ['*1']]]]]]]

>>> print(external2json(rules))  # doctest: +NORMALIZE_WHITESPACE
[
    {
        "name": "root",
        "selector_type": "xpath",
        "selector": "/jobs/job",
        "type_list": [
            "+"
        ],
        "rule": [
            {
                "name": "title",
                "selector_type": "xpath",
                "selector": "./title/text()",
                "type_list": [
                    "+"
                ]
            },
            {
                "name": "url",
                "selector_type": "xpath",
                "selector": "./url/text()",
                "type_list": [
                    "+1"
                ]
            },
            {
                "name": "location",
                "selector_type": "xpath",
                "selector": ".",
                "type_list": [
                    "*"
                ],
                "rule": [
                    {
                        "name": "country",
                        "selector_type": "xpath",
                        "selector": "./country/text()",
                        "type_list": [
                            "+1"
                        ]
                    },
                    {
                        "name": "city",
                        "selector_type": "xpath",
                        "selector": "./city/text()",
                        "type_list": [
                            "+1"
                        ]
                    },
                    {
                        "name": "zip",
                        "selector_type": "xpath",
                        "selector": "./postalcode/text()",
                        "type_list": [
                            "*1"
                        ]
                    }
                ]
            }
        ]
    }
]

scrapy.org_support.doctest
==========================
>>> rules = '''
... company_list `.//div[@class='company-box']` +
...     name `.//span[@class='highlight']/text()` +
...     company_url `./a/@href` +1
...     blog_url `./p/a/@href` *
...     logo `./a/img/@src` +
... '''

>>> pprint.pprint(external2list(rules))
[['company_list',
  'xpath',
  ".//div[@class='company-box']",
  ['+'],
  [['name', 'xpath', ".//span[@class='highlight']/text()", ['+']],
   ['company_url', 'xpath', './a/@href', ['+1']],
   ['blog_url', 'xpath', './p/a/@href', ['*']],
   ['logo', 'xpath', './a/img/@src', ['+']]]]]

>>> print(external2json(rules))  # doctest: +NORMALIZE_WHITESPACE
[
    {
        "name": "company_list",
        "selector_type": "xpath",
        "selector": ".//div[@class='company-box']",
        "type_list": [
            "+"
        ],
        "rule": [
            {
                "name": "name",
                "selector_type": "xpath",
                "selector": ".//span[@class='highlight']/text()",
                "type_list": [
                    "+"
                ]
            },
            {
                "name": "company_url",
                "selector_type": "xpath",
                "selector": "./a/@href",
                "type_list": [
                    "+1"
                ]
            },
            {
                "name": "blog_url",
                "selector_type": "xpath",
                "selector": "./p/a/@href",
                "type_list": [
                    "*"
                ]
            },
            {
                "name": "logo",
                "selector_type": "xpath",
                "selector": "./a/img/@src",
                "type_list": [
                    "+"
                ]
            }
        ]
    }
]
"""

import os
import re
from collections import OrderedDict
from io import TextIOWrapper

from lxml import etree
from pyparsing import (
    ParseFatalException,
    ParseException,
    FollowedBy,
    Word,
    Regex,
    Optional,
    Forward,
    OneOrMore,
    Group,
    Literal,
    Suppress,
    ParseBaseException,
    ZeroOrMore,
    Or,
    QuotedString
)
from pyparsing import (
    col,
    lineEnd,
    empty,
    alphas,
    alphanums,
    pythonStyleComment,
    delimitedList,
    oneOf)

from ciur import xpath_functions_ciur
from ciur import pretty_json
from ciur.exceptions import CiurBaseException, ParseExceptionInCiurFile

# noinspection PyUnresolvedReferences
# load namespace function in lxml.etree
import ciur.xpath_functions  # pylint: disable=unused-import

_INDENT_STACK = [1]


def _check_peer_indent(string, location, token):
    """
    :param string: the original string being parsed
        :type string: str

    :param location: the location of the matching substring
        :type location: int

    :param token: matched token, packaged as a C{L{ParseResults}} object
        :type token: C{L{ParseResults}}
    """
    del token

    cur_col = col(location, string)
    if cur_col != _INDENT_STACK[-1]:
        if (not _INDENT_STACK) or cur_col > _INDENT_STACK[-1]:
            raise ParseFatalException(string, location, "illegal nesting")
        raise ParseException(string, location, "not a peer entry ????")


def _check_sub_indent(string, location, token):
    """
    :param string: the original string being parsed
        :type string: str

    :param location: the location of the matching substring
        :type location: int

    :param token: matched token, packaged as a C{L{ParseResults}} object
        :type token: C{L{ParseResults}}
    """
    del token

    cur_col = col(location, string)
    if cur_col > _INDENT_STACK[-1]:
        _INDENT_STACK.append(cur_col)
    else:
        raise ParseException(string, location, "not a subentry")


def _check_unindent(string, location):
    """
    :param string: the original string being parsed
        :type string: str

    :param location: the location of the matching substring
        :type location: int
    """
    if location >= len(string):
        return

    cur_col = col(location, string)
    if not(cur_col < _INDENT_STACK[-1] and cur_col <= _INDENT_STACK[-2]):
        raise ParseException(string, location, "not an unindent")


def do_unindent():
    """detect end of indent and unindent stack back"""
    _INDENT_STACK.pop()


def validate_identifier(string, location, tokens):
    """
    :param string: the original string being parsed
        :type string: str

    :param location: the location of the matching substring
        :type location: int

    :param tokens: list of matched tokens, packaged as a C{L{ParseResults}}
        object
        :type tokens: iterable[C{L{ParseResults}}]
    """
    identifier = tokens[0]
    if identifier.endswith(":"):
        raise ParseFatalException(
            string,
            location + len(identifier),
            "validate_identifier-> not allowed `:` delimiter symbol at the end"
        )

    if identifier.startswith(":"):
        raise ParseFatalException(
            string,
            location + 1,
            "validate_identifier-> not allowed `:` delimiter symbol at the"
            "begin"
        )

    index = identifier.find("::")
    if index >= 0:
        raise ParseFatalException(
            string,
            location + index + 1,
            "validate_identifier-> duplicate `:` delimiter"
        )


def type_list_validation(string, location, expr, error):
    """
    add more explicit error handling in case if bnf fail caused by invalid
    type_list

    :param string: the original string being parsed
        :type string: str

    :param location: the location of the matching substring
        :type location: int

    :param expr: the parse expression that failed
        :type expr: expr

    :param error: raised exception
        :type error: Exception
    """

    raise ParseFatalException(
        string,
        location + 1,
        "type_list_validation->%s, %s" % (error, expr)
    )

casting_modules = {
    ciur.xpath_functions_ciur,
    ciur.xpath_functions,
}


def _type_list():
    casting_functions_args = Optional(
        Suppress("(") +
        delimitedList(IDENTIFIER | QuotedString(quoteChar="\'", )) +
        Suppress(")")
    )

    casting_functions_list = [
        Group(Literal(i[:-1]) + casting_functions_args)
        for i in xpath_functions_ciur.__dict__.keys()
        if i.endswith("_") and not i.startswith("__")
    ]

    for i_module in casting_modules:
        casting_functions_list += [
            Group(Literal(k[3:]) + casting_functions_args)
            for k in i_module.__dict__.keys()
            if k.startswith("fn_")
        ]

    _ = Group("str" + Suppress(".") + IDENTIFIER) + casting_functions_args
    casting_functions_list.append(Group(_))

    _ = Group("unicode" + Suppress(".") + IDENTIFIER) + casting_functions_args
    casting_functions_list.append(Group(_))

    casting_functions = Or(
        casting_functions_list
    )

    return Group(
        # url ./url <str> +1 => functions chains for transformation
        ZeroOrMore(casting_functions) +

        # url ./url str <+1>  => size match: + mandatory,
        # * optional, \d+ exact len
        Regex(r"[+*]\d*")
    ).setFailAction(type_list_validation)


def _get_bnf(namespace=None):
    """
    :param namespace:
        :type namespace: dict

    :return: Backus-Naur Form grammars
    :rtype pyparsing.ParserElement
    """

    def validate_xpath(string, location, tokens):
        """
        :param string: the original string being parsed
            :type string: str

        :param location: the location of the matching substring
            :type location: int

        :param tokens: list of matched tokens, packaged as a C{L{ParseResults}}
            object
            :type tokens: iterable[C{L{ParseResults}}]
        """
        xpath_ = tokens[0]
        try:
            if re.search(r"number\(.*?\)", string):
                import sys
                sys.stderr.write(
                    "[WARNING] use `float` from type_list instead of"
                    "`number` from xpath, because number lies see "
                    "http://stackoverflow.com/questions/33789196/"
                    "is-xpath-number-function-lies\n"
                )

            context = etree.fromstring("<root></root>")
            context.xpath(xpath_, namespaces=namespace)
            # XPATH_EVALUATOR(xpath_, namespaces=namespace)
        except (etree.XPathEvalError, ) as xpath_eval_error:
            raise ParseFatalException(
                string,
                location,
                "validate_xpath->%s" % xpath_eval_error
            )

    # url <./url> str +1 => xpath query
    xpath = Optional(oneOf("xpath css"), default="xpath") + \
        QuotedString(quoteChar="`")

    type_list = _type_list()

    rule = (IDENTIFIER + xpath + type_list)  # <url ./url str +1> => rule line

    stmt = Forward().setParseAction(_check_peer_indent)
    bnf = OneOrMore(stmt)

    children = Group(INDENT + bnf + UNDENT).ignore(pythonStyleComment)

    # check for children
    # pylint: disable=expression-not-assigned
    stmt << Group(rule + Optional(children))

    return bnf


def external2list(rules, namespace=None):
    """
    Transform external ciur dsl (file or text) into grammar list
    :param rules: file or basestring
        :type rules: Rule

    :param namespace: DOM namespace
        :type namespace: dict

    :rtype: list[str]
    """
    assert isinstance(rules, (TextIOWrapper, str))

    file_name = None
    if isinstance(rules, TextIOWrapper):
        file_name = rules.name
        rules = rules.read()

    if not rules.strip():
        raise CiurBaseException(
            "DSL is empty", {
                "file_name": os.path.abspath(file_name) if file_name else None
            }
        )

    if not re.search(r"\n\s*$", rules):
        raise CiurBaseException(
            "no new line at the end of file", {
                "file_name": os.path.abspath(file_name) if file_name else None
            }
        )

    bnf = _get_bnf(namespace=namespace)
    try:
        parse_tree = bnf.parseString(rules, parseAll=True)
    except (ParseBaseException,) as parse_error:
        raise ParseExceptionInCiurFile(rules, file_name, parse_error)

    return parse_tree.asList()


def _list_grammar2dict_list(rule_list):
    """
    convert list of grammar into list of `dict`
    :param rule_list:
        :type rule_list: list

    :rtype: list[OrderedDict]
    """
    rule_list_out = []

    for rule_i in rule_list:
        dict_ = OrderedDict()
        dict_["name"] = rule_i[0]
        dict_["selector_type"] = rule_i[1]
        dict_["selector"] = rule_i[2]
        dict_["type_list"] = rule_i[3]
        if len(rule_i) == 5:
            dict_["rule"] = _list_grammar2dict_list(rule_i[4])

        rule_list_out.append(dict_)

    return rule_list_out


def ensure_unicode_provision(data):
    """
    Ensure that we use unicode but not string items
    :param data:
        :type data: list[basestring] or basestring or object

    :rtype list[unicode] or unicode or object
    """
    if isinstance(data, list):
        return [ensure_unicode_provision(i) for i in data]

    return data


def external2dict(rules, namespace=None):
    """
    convert external_dls (*.ciur) to dict_dsl
    TODO: define in documentation type of DSL:
        external, dict, json, grammar_list, internal_dsl (Rule)
    :param rules:
        :type rules: FileIO or str

    :param namespace:
        :type namespace: xml namespace

    :rtype: list[OrderedDict]
    """
    list_ = external2list(rules, namespace=namespace)
    list_ = ensure_unicode_provision(list_)

    data = _list_grammar2dict_list(list_)

    return data


def external2json(rules):
    """
    convert external dls (*.ciur) to python json str
    :param rules:
        :type rules: file or str

    :return: json
        :rtype: str
    """

    data = external2dict(rules)

    return pretty_json(data)

###############################################################################
# constants
###############################################################################

INDENT = lineEnd.suppress() + empty + empty.copy(
).setParseAction(_check_sub_indent)

UNDENT = FollowedBy(
    empty
).setParseAction(
    _check_unindent
).setParseAction(
    do_unindent
)

# TODO: describe ":" variable comprehension
# <url> ./url str +1 => label of rule
IDENTIFIER = Word(alphas, alphanums + "_:").addParseAction(validate_identifier)
