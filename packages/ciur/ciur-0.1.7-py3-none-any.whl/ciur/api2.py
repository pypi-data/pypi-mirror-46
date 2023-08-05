"""
shortcuts for api version 2
ciur.shortcuts is version 1
"""
from ciur.models import Document
from ciur.rule import Rule
from ciur import bnf_parser
import ciur


def parse(http_response, ciur_rule):
    document = Document(http_response)

    with ciur.open_file(ciur_rule, __file__) as file_cursor:
        ciur_rule = file_cursor.read()

    res = bnf_parser.external2dict(ciur_rule, namespace=document.namespace)
    rule = Rule.from_list(res)

    parse_fun = getattr(ciur.parse, document.doctype + "_type")

    return parse_fun(document, rule[0])
