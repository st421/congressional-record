from dateutil.parser import parse

from bs4 import NavigableString
from html2ans.parsers.base import NullParser
from congressionalrecord.govinfo.parsers.elements.base import RegexParser


class RegexNullElementParser(RegexParser, NullParser):
    def parse(self, *args, **kwargs):
        return NullParser.parse(self, *args, **kwargs)


class StringParser(NullParser):
    applicable_elements = [NavigableString]
    match_against = []

    def is_applicable(self, element, *args, **kwargs):
        if element in self.match_against:
            return True
        return False

    def parse(self, *args, **kwargs):
        return NullParser.parse(self, *args, **kwargs)


class DateParser(NullParser):
    applicable_elements = [NavigableString]

    def is_applicable(self, element, *args, **kwargs):
        try:
            parse(element)
        except Exception:
            return False
        return True

    def parse(self, *args, **kwargs):
        return NullParser.parse(self, *args, **kwargs)


class PrimaryPageParser(RegexNullElementParser):
    name = "page"
    match_against = r'\[Page[s]? (?P<pages>[\w\-]+)\]'


class SecondaryPageParser(RegexNullElementParser):
    name = "page"
    match_against = r'\[\[Page (?P<page>[\w\-]+)\]\]'


class SourceParser(RegexNullElementParser):
    name = "source"
    match_against = r'^From the Congressional Record Online through the Government (Publishing|Printing) Office \[www.gpo.gov\]'


class HeaderParser(RegexNullElementParser):
    name = "header"
    match_against = r'^\[Congressional Record Volume (?P<vol>[0-9]+), Number (?P<num>[0-9]+)'\
        + r' \((?P<wkday>[A-Za-z]+), (?P<month>[A-Za-z]+) (?P<day>[0-9]+), (?P<year>[0-9]{4})\)\]'


class SeparatorParser(RegexNullElementParser):
    match_against = r'^\s*[_]+\s*$'
