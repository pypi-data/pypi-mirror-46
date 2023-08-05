"""
Common function that can not be hold in ciur.__init__ because it is doing
third party library calls
"""
import os
from http.cookiejar import LWPCookieJar

from lxml.etree import FunctionNamespace
from lxml.etree import _Element as EtreeElement

from requests import Session


def load_xpath_functions(locals_):
    """
    load xpath functions into lxml scopes
    see http://lxml.de/extensions.html#the-functionnamespace

    :param locals_:  dictionary containing the current scope's local variables.
        :type locals_: dict
    """
    function_namespaces = FunctionNamespace(None)

    function_namespaces.update({
        k[3:].replace("_", "-"): v for (k, v) in locals_.items()
        if k.startswith("fn_")
    })


def get_session(callback_log_in, cookie_file_path):
    """
    get session with cookies file support save / load

    :param cookie_file_path:
        :type cookie_file_path: str
    :param callback_log_in:
        :type callback_log_in: function

    :rtype: Session
    """

    session = Session()

    session.cookies = LWPCookieJar(cookie_file_path)

    if not os.path.exists(cookie_file_path):
        print("[INFO] setting cookies")
        session.cookies.save()
        callback_log_in(session)
    else:
        print("[INFO] loading cookies")
        session.cookies.load(ignore_discard=True)

    return session


def element2text(value):
    """
    convert value to text if is EtreeElement or strip value is is text already
    :param value:
        :type value: EtreeElement or list or str
    :rtype str or iterable[str]
    """
    if isinstance(value, EtreeElement):
        return value.text
    elif isinstance(value, list) and len(value) > 0:
        return [element2text(i) for i in value]

    if not value:
        return value

    if not isinstance(value, str):
        value = str(value)

    return value.strip()


def is_url(path):
    return (
        hasattr(path, "startswith") and
        (path.startswith("https://") or path.startswith("http://"))
    )
