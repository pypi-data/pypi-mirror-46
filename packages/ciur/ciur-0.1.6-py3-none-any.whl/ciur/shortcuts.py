"""
This module collects helper functions and classes.
"""

import inspect
import sys

import requests

from ciur import bnf_parser
from ciur import get_logger
from ciur import parse
from ciur import pretty_json
from ciur.exceptions import CiurBaseException
from ciur import CONF
from ciur.helpers import is_url
from ciur.models import Document
from ciur.rule import Rule
import ciur

REQ_SESSION = requests.Session()

HTTP_HEADERS = {
    "User-Agent": "%s/%s %s/%s %s" % (
        ciur.__title__, ciur.__version__,
        requests.__title__, requests.__version__,

        ciur.__git__
    )
}


LOGGER = get_logger(__name__)


def pretty_parse(ciur_file_or_path,
                  url,
                  doctype=None,
                  namespace=None,
                  headers=None,
                  encoding=None,
                  req_callback=None):
    """
    WARN:
        do not use this helper in production,
        use only for sake of example,
        because of redundant rules and http session

    :param doctype: MIME types to specify the nature of the file currently
        being handled.
        see http://www.freeformatter.com/mime-types-list.html

    :param req_callback:
    :param ciur_file_or_path: external dsl
    :param url: url to be fetch with GET requests lib
    :return : extracted data as pretty json
    """
    if not headers:
        headers = HTTP_HEADERS

    # workaround for get relative files
    called_by_script = inspect.stack()[1][1]

    if isinstance(ciur_file_or_path, file):
        ciur_file_path, ciur_file = ciur_file_or_path.name, ciur_file_or_path
    else:
        ciur_file_path = ciur.path(ciur_file_or_path, called_by_script)

        ciur_file = open(ciur_file_path)

    res = bnf_parser.external2dict(ciur_file, namespace=namespace)
    rule = Rule.from_list(res)

    if req_callback:
        response = req_callback()
    else:
        response = REQ_SESSION.get(url, headers=headers)
        # TODO: set http timeout 10

    if not CONF["IGNORE_WARNING"]:
        for key in ("Etag", "Last-Modified", "Expires", "Cache-Control"):
            if response.headers.get(key):
                sys.stderr.write("[WARN] request.response has Etag, . "
                                 "TODO: link to documentation\n")

    if not doctype:
        for i_doc_type in dir(parse):
            if i_doc_type.endswith("_type") and i_doc_type.replace(
                    "_type", "") in response.headers["content-type"]:

                doctype = i_doc_type
                break
        else:
            raise CiurBaseException("can not autodetect doc_type `%s`" %
                                    response.headers["content-type"])

    parse_fun = getattr(parse, doctype)

    if not encoding:
        encoding = response.apparent_encoding

    data = parse_fun(ciur.models.Document(
        response.content,
        url=response.url,
        namespace=namespace,
        encoding=encoding
    ), rule[0])

    return pretty_json(data)


def pretty_parse_from_document(rule, document):
    # type(file or )
    """
    WARN:
        do not use this helper in production,
        use only for sake of example,
        because of redundant rules and http session

    :param req_callback:
    :param rule: row text for external dsl
    :param url: url to be fetch with GET requests lib
    :return : extracted data as pretty json
    """

    res = bnf_parser.external2dict(rule, namespace=document.namespace)
    rule = Rule.from_list(res)

    parse_fun = getattr(parse, document.doctype + "_type")

    data = parse_fun(document, rule[0])

    return pretty_json(data)


def pretty_parse_from_resources(ciur_rule, document_to_parse, namespace=None, doctype=None):
    if is_url(ciur_rule):
        LOGGER.info("Downloading rule %r", ciur_rule)
        response = REQ_SESSION.get(ciur_rule, headers=HTTP_HEADERS)
        ciur_rule = response.text
    # else:
    #     with ciur.open_file(ciur_rule, __file__) as file_cursor:
    #         ciur_rule = file_cursor.read()

    if is_url(document_to_parse):
        LOGGER.info("Downloading document to parse %r", document_to_parse)
        response = REQ_SESSION.get(document_to_parse, headers=HTTP_HEADERS)
        document = Document(response, namespace=namespace)
    else:
        # with ciur.open_file(document_to_parse, __file__) as file_cursor:
        #     document_to_parse = file_cursor.read()

        document = Document(document_to_parse, namespace=namespace,
                            doctype=doctype)

    return pretty_parse_from_document(ciur_rule, document)
