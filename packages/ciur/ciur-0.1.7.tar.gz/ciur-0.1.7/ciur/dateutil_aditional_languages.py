# -*- coding, utf-8 -*-
# coding=utf-8
"""
additional language support for python-dateutil lib
see http//stackoverflow.com/questions/8896038/
    how-to-use-python-dateutil-1-5-parse-function-to-work-with-unicode

TODO, create separated package of this python-dateutil-language
"""

# noinspection SpellCheckingInspection
from collections import OrderedDict

MONTHS = OrderedDict((
    # russian

    (u"Января", "January"),
    (u"Февраля", "February"),
    (u"Марта", "March"),
    (u"Апреля", "April"),
    (u"Мая", "May"),
    (u"Июня", "June"),
    (u"Июля", "July"),
    (u"Августа", "August"),
    (u"Сентября", "September"),
    (u"Октября", "October"),
    (u"Ноября", "November"),
    (u"Декабря", "December"),

    (u"Янв", "January"),
    (u"Февр", "February"),
    (u"Март", "March"),
    (u"Апр", "April"),
    (u"Май", "May"),
    (u"Июнь", "June"),
    (u"Июль", "July"),
    (u"Авг", "August"),
    (u"Сент", "September"),
    (u"Окт", "October"),
    (u"Нояб", "November"),
    (u"Дек", "December"),



    # ukranian

    (u"Січня", "January"),
    (u"Лютого", "February"),
    (u"Березня", "March"),
    (u"Квітня", "April"),
    (u"Травня", "May"),
    (u"Червня", "June"),
    (u"Липня", "July"),
    (u"серпня", "August"),
    (u"Вересня", "September"),
    (u"Жовтня", "October"),
    (u"Листопада", "November"),
    (u"Грудня", "December"),

    (u"Січень", "January"),
    (u"Лютий", "February"),
    (u"Березень", "March"),
    (u"Квітень", "April"),
    (u"Травень", "May"),
    (u"Червень", "June"),
    (u"Липень", "July"),
    (u"Серпень", "August"),
    (u"Вересень", "September"),
    (u"Жовтень", "October"),
    (u"Листопад", "November"),
    (u"Грудень", "December"),

    # romanian
    ("ianuarie", "January"),
    ("februarie", "February"),
    ("martie", "March"),
    ("aprilie", "April"),
    ("mai", "May"),
    ("iunie", "June"),
    ("iulie", "July"),
    ("august", "August"),
    ("septembrie", "September"),
    ("octombrie", "October"),
    ("noiembrie", "November"),
    ("decembrie", "December"),

    ("ian.", "January")
))


for foreign, eng in dict(MONTHS).items():
    MONTHS[foreign.lower()] = eng
    MONTHS[foreign.lower()] = eng
    MONTHS[foreign.capitalize()] = eng
