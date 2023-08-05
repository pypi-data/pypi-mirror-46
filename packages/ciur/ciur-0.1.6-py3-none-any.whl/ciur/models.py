"""
place where to hold all Models related class of ``ciur``
"""
from requests.models import Response


class Document(object):  # pylint: disable=too-few-public-methods
    """
    Model for encapsulate data.
    Scope:
        workaround for too-many-arguments for pylint, to not pass more than
        5 argument in a functions
    """
    def __init__(
            self,
            content,
            namespace=None,
            encoding=None,
            url=None,
            doctype="/html"
    ):
        """
        :param doctype: MIME types to specify the nature of the file currently
            being handled.
            see http://www.freeformatter.com/mime-types-list.html
        """
        if isinstance(content, Response):
            self.content = content.content
            self.encoding = content.apparent_encoding
            self.url = content.url
            doctype = content.headers["content-type"]
        else:
            self.content = content
            self.encoding = encoding
            self.url = url

        if "/xml" in doctype:
            doctype = "xml"
        elif "/pdf" in doctype:
            doctype = "pdf"
        elif "/html" in doctype:
            doctype = "html"

        self.doctype = doctype

        self.namespace = namespace

    def __str__(self):
        _ = {
            "content": self.content
        }
        if self.encoding:
            _["encoding"] = self.encoding

        if self.url:
            _["url"] = self.url

        if self.namespace:
            _["namespace"] = self.namespace

        return "Document%s" % _
