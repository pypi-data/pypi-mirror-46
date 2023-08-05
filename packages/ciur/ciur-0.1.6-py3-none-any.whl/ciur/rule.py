"""
ciur internal dsl (python api)
"""
from collections import OrderedDict
from types import FunctionType
import json
import re

import ciur
import ciur.xpath_functions_ciur
from ciur import pretty_json, bnf_parser

_JSON = str

_SELECTOR_TYPE_SET = {"xpath", "css"}


class Rule(ciur.CommonEqualityMixin):
    """
    >>> rule1 = Rule("root", "/h3", "+",
    ...  Rule("name", ".//h1[contains(., 'Justin')]/text()", "+1"),
    ...  Rule("count_list", ".//h2[contains(., 'Andrei')]/p", ["int", "+"]),
    ...  Rule("user", ".//h5[contains(., 'Andrei')]/p", "+",
    ...         Rule("name", "./spam/text()", "+1"),
    ...         Rule("sure_name", "./bold/text()", "+1"),
    ...         Rule("age", "./it", "int"),
    ...         Rule("hobby", "./li/text()", "+"),
    ...         Rule("indexes", "./li/bold", ["int", "+"])
    ...       )
    ... )

    >>> res1 = pretty_json(rule1.to_dict())
    >>> print(res1)  # doctest: +NORMALIZE_WHITESPACE
    {
        "name": "root",
        "selector": "/h3",
        "selector_type": "xpath",
        "type_list": "+",
        "rule": [
            {
                "name": "name",
                "selector": ".//h1[contains(., 'Justin')]/text()",
                "selector_type": "xpath",
                "type_list": "+1"
            },
            {
                "name": "count_list",
                "selector": ".//h2[contains(., 'Andrei')]/p",
                "selector_type": "xpath",
                "type_list": [
                    "int",
                    "+"
                ]
            },
            {
                "name": "user",
                "selector": ".//h5[contains(., 'Andrei')]/p",
                "selector_type": "xpath",
                "type_list": "+",
                "rule": [
                    {
                        "name": "name",
                        "selector": "./spam/text()",
                        "selector_type": "xpath",
                        "type_list": "+1"
                    },
                    {
                        "name": "sure_name",
                        "selector": "./bold/text()",
                        "selector_type": "xpath",
                        "type_list": "+1"
                    },
                    {
                        "name": "age",
                        "selector": "./it",
                        "selector_type": "xpath",
                        "type_list": "int"
                    },
                    {
                        "name": "hobby",
                        "selector": "./li/text()",
                        "selector_type": "xpath",
                        "type_list": "+"
                    },
                    {
                        "name": "indexes",
                        "selector": "./li/bold",
                        "selector_type": "xpath",
                        "type_list": [
                            "int",
                            "+"
                        ]
                    }
                ]
            }
        ]
    }

    >>> rule2 = Rule.from_dict(res1)
    >>> rule1.to_dict() == rule2.to_dict()
    True
    >>> rule1 == rule2
    True
    """

    def __init__(self, name, selector, type_list_, *selector_type_and_or_rule):
        self.name = name
        self.selector = selector

        if not selector_type_and_or_rule:
            self.selector_type = "xpath"
            self.rule = ()
        else:
            if isinstance(selector_type_and_or_rule[0], self.__class__):
                self.selector_type = "xpath"
                self.rule = selector_type_and_or_rule
            elif selector_type_and_or_rule[0] in _SELECTOR_TYPE_SET:
                self.selector_type = selector_type_and_or_rule[0]
                self.rule = selector_type_and_or_rule[1]
            else:
                raise NotImplementedError("new Use case not Rule, css or xpath")

        # mutable object is eval !
        if isinstance(self.rule, list):
            self.rule = tuple(self.rule)

        tmp = []

        for type_i in self._2complex(type_list_):
            #  assert isinstance(type_i, basestring)

            if isinstance(type_i, list):
                func_name = type_i[0]
                args = type_i[1:]

            else:
                match = re.search(r"^([*+])(\d*)$", type_i)
                if match:
                    func_name = "size"
                    args = (
                        "mandatory" if match.group(1) == "+" else "optional",
                        int(match.group(2) or 0),
                    )
                else:
                    func_name = type_i
                    args = tuple()

            # TODO there are 2 entity function and methods of object,
            # TODO  rename func_name into callable_name
            if isinstance(func_name, list):
                obj_str, method_str = func_name
                import builtins
                obj = getattr(builtins, obj_str)
                method = getattr(obj, method_str)
                tmp.append([method, args])
            else:
                for casting_module in bnf_parser.casting_modules:
                    try:
                        tmp.append([
                            getattr(casting_module, func_name + "_"),
                            args
                        ])
                        break
                    except (AttributeError,) as attribute_error:
                        pass

                    try:
                        tmp.append([
                            getattr(casting_module, "fn_" + func_name),
                            args
                        ])
                        break
                    except (AttributeError,) as attribute_error:
                        pass
                else:
                    raise attribute_error


        self.type_list = tmp

    @classmethod
    def _2complex(cls, value):
        """
        convert data from simple/compact format into complex/verbose format
        :param value:
            :type value: tuple or list or str
        :rtype: tuple
        """
        if not isinstance(value, (tuple, list)):

            # noinspection PyRedundantParentheses
            return (value, )

        return value

    @classmethod
    def _2simple(cls, value):
        """
        convert data from complex/verbose format into simple/compact
        :param value:
            :type value: list or tuple or str
        :rtype: value or list or tuple
        """
        if isinstance(value, (list, tuple)):
            tmp = []
            for value_i in value:
                tmp_i = value_i
                if isinstance(value_i[0], FunctionType):
                    function = value_i[0].__name__
                    if function == "size_":
                        tmp_i = "%s%s" % (
                            "+" if value_i[1][0] == "mandatory" else "*",
                            "" if value_i[1][1] == 0 else value_i[1][1]
                        )
                    else:
                        if not value_i[1]:
                            if function.startswith("fn_"):
                                tmp_i = ("%s" % function[3:])
                            elif function.endswith("_"):
                                tmp_i = ("%s" % function[:-1])
                            else:
                                # TODO remove this in future
                                raise Exception("new use case")

                tmp.append(tmp_i)
            value = tmp

            if len(value) == 1:
                return value[0]

        return value

    @staticmethod
    def from_dict(dict_):
        """
        factory method, build `Rule` object from `dict_`
        :param dict_:
            :type dict_: dict or basestring
        :rtype: Rule
        """
        # TODO: check load root list

        assert isinstance(dict_, (dict, _JSON))

        if isinstance(dict_, _JSON):
            dict_ = json.loads(dict_)

        # check for children [] means no children
        rule = [Rule.from_dict(rule) for rule in dict_.get("rule", [])]

        return Rule(
            dict_["name"], dict_["selector"], dict_["type_list"],
            *(dict_.get("selector_type", "xpath"), rule)
        )

    @staticmethod
    def from_list(list_):
        """
        factory method, build ListOf `Rule` objects from `list_`
        :param list_:
            :type list_: list
        :rtype: list of Rule
        """
        return ListOfT(Rule.from_dict(i) for i in list_)

    @staticmethod
    def from_dsl(dsl):
        """
        factory method, build rule from dsl
        :param dsl:
            :type dsl: FileIO or str
        :rtype: list of Rule
        """
        res = bnf_parser.external2dict(dsl)

        return Rule.from_list(res)

    def to_dict(self):
        """
        exporting/serializing `Rule` object into `OrderedDict`
        :rtype OrderedDict
        """
        ret = OrderedDict()
        ret["name"] = self.name
        ret["selector"] = self.selector
        ret["selector_type"] = self.selector_type
        ret["type_list"] = self._2simple(self.type_list)

        rule = [i.to_dict() for i in self.rule]
        if rule:
            ret["rule"] = rule

        return ret

    def __repr__(self):
        return "%s.%s(%s)" % (
            self.__class__.__module__,
            self.__class__.__name__,
            self.to_dict()
        )

    def __str__(self):
        pretty = pretty_json(self.to_dict())
        return "%s.%s(%s)" % (
            self.__class__.__module__,
            self.__class__.__name__,
            pretty
        )


class ListOfT(list):
    """
    wrapper for List Of Dict
    The purpose is to have pretty print option for that complex type
    """
    @classmethod
    def _callback(cls, value):
        """
        define logic of serialization
        :param value:
            :type value: object
        :rtype: value
        """
        return value

    def __str__(self):
        name = "%s.%s:" % (self.__class__.__module__, self.__class__.__name__)
        res = name + "".join(
            "\n-----------%d-\n%s" % (index, self._callback(t))
            for index, t in enumerate(self, 1)
        ).replace("\n", "\n    ")

        return res


class ListOfDict(ListOfT):
    """
    wrapper for List Of Dict
    The purpose is to have pretty print option for that complex type
    """
    @classmethod
    def _callback(cls, x):
        return pretty_json(x)
