"""
By following **Single Responsible** principle
Ciur should extract only data from Markup-ed text and
should not be concern about about how this input string is received

As a result request lib should be an option and not a must
"""

try:
    import requests
except ImportError:
    display_version = ""
else:
    display_version = f"{requests.__title__}/{requests.__version__}"
