"""
collection of decorators user in `ciur`
"""
from functools import wraps

from ciur.helpers import element2text


def check_new_node(func):
    """
    :param func:
        :type func: function

    xpath allow to return items in list only as a EtreeNones or text,
    in case of others types (f.e. int, float ...):
        - get only first (in case of http://www.w3.org/2005/xpath-functions)
            f.e.
            ## TODO add doctest here
            >> parse("<ul><li>1</li><li>2</li></ul>").xpath("number(/ul/li)")
            1.0

        - raise exception  (in case of
        https://bitbucket.org/ada/ciur/src/docs/2016/xpath-functions)
            f.e.
             ## TODO add doctest here
            >> parse("<ul><li>1</li><li>2</li></ul>").xpath("number(/ul/li)")
                Trace back
                ...
                Exception
        - raise exception  (in case of
            https://bitbucket.org/ada/ciur/src/docs/2016/xpath-functions)
            f.e.
            ## TODO add doctest here
            >> parse("<ul><li>1</li><li>2</li></ul>").xpath("number(/ul/li)")
            Trace back
            ...
            Exception
        - success  (in is only one item)
            f.e.
             ## TODO add doctest here
            >> parse("<ul><li>1</li><li>2</li></ul>").xpath("float(/ul/li)")
            1.0

    """
    @wraps(func)
    def checker(context, value, *_):
        """
        default wrapper function

        :param context: Parent DOM context
            :type context: EtreeElement
        :param value:
            :type value: iterable[object] or object
        :param _:
        :return: object or iterable[object or EtreeElement]
        """
        if isinstance(value, (list, tuple)):
            size = len(value)

            if not size:
                return None

            assert size == 1

            return func(context, value[0], *_)

        return func(context, value, *_)

    return checker


def convert_element2text(func):
    """
    :param func:
        :type func: function
    """
    @wraps(func)
    def checker(context, value, *_):
        """
        default wrapper function

        :param context: Parent DOM context
            :type context: EtreeElement
        :param value:
            :type value: iterable[object] or object
        :param _:
        :return: str or iterable[str]
        """
        text = element2text(value)

        return func(context, text, *_)
    return checker
