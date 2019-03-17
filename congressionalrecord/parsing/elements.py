import re
from dateutil.parser import parse

from bs4 import NavigableString
from html2ans.parsers.base import NullParser, BaseElementParser, ParseResult


class RegexElementParser(BaseElementParser):
    applicable_elements = [NavigableString]
    applicable_regex = None
    regex_el = None
    content_type = None

    def __init__(self, *args, **kwargs):
        self.regex_result = None

    def is_applicable(self, element, *args, **kwargs):
        if super().is_applicable(element, *args, **kwargs):
            regex_output = re.match(self.applicable_regex, element)
            if regex_output:
                self.regex_result = regex_output
                return True
        return False

    def parse(self, element, *args, **kwargs):
        if self.regex_el:
            content = self.regex_result.group(self.regex_el)
        else:
            content = None
        return ParseResult({
            "type": self.content_type,
            "content": content,
        }, True)


class DateElementParser(NullParser):
    def is_applicable(self, element, *args, **kwargs):
        try:
            parse(element)
        except Exception:
            return False
        return True

    def parse(self, *args, **kwargs):
        return NullParser.parse(self, *args, **kwargs)


class RegexNullElementParser(RegexElementParser, NullParser):
    def parse(self, *args, **kwargs):
        return NullParser.parse(self, *args, **kwargs)


class RegexTopLevelElementParser(RegexElementParser):
    name = None

    def parse(self, element, *args, **kwargs):
        return ParseResult({
            self.name: self.regex_result.group(self.regex_el),
            "type": "top-level"
        }, True)


class ChamberParser(RegexTopLevelElementParser):
    name = "doc_type"
    regex_el = "chamber"
    applicable_regex = r'\[(?P<chamber>[A-Za-z\s]+)\]'


class PageParser(RegexTopLevelElementParser):
    name = "page"
    regex_el = "pages"
    applicable_regex = r'\[Page[s]? (?P<pages>[\w\-]+)\]'


class SourceParser(RegexNullElementParser):
    name = "source"
    applicable_regex = r'^From the Congressional Record Online through the Government (Publishing|Printing) Office \[www.gpo.gov\]'


class HeaderParser(RegexNullElementParser):
    name = "header"
    applicable_regex = r'^\[Congressional Record Volume (?P<vol>[0-9]+), Number (?P<num>[0-9]+)'\
        + r' \((?P<wkday>[A-Za-z]+), (?P<month>[A-Za-z]+) (?P<day>[0-9]+), (?P<year>[0-9]{4})\)\]'


class RollCallParser(RegexElementParser):
    content_type = "rollcall"
    applicable_regex = r'\[Roll(call)?( Vote)? No. \d+.*\]'


class TitleParser(RegexElementParser):
    content_type = "title"
    regex_el = "title"
    applicable_regex = r'^ \s*(?P<title>([A-Z0-9.,]+[^a-z]+))$'


class SpeakerParser(RegexElementParser):
    content_type = "speaker"
    regex_el = "speaker"
    applicable_regex = r'\s*(HON|Mr|Ms|The)?(.)? (?P<speaker>([A-Z.,]+))$'


class SeparatorParser(RegexNullElementParser):
    applicable_regex = r'^\s*[_]+\s*$'