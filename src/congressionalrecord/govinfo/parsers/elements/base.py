import re

from bs4 import NavigableString
from html2ans.parsers.base import BaseElementParser, ParseResult


class RegexParser(BaseElementParser):
    applicable_elements = [NavigableString]
    match_against = None
    regex_el = None
    content_type = None
    content_section = None

    def __init__(self, *args, **kwargs):
        self.regex_result = None

    def is_applicable(self, element, *args, **kwargs):
        if super().is_applicable(element, *args, **kwargs):
            regex_output = re.match(self.match_against, element)
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


class StringParser(BaseElementParser):
    applicable_elements = [NavigableString]
    match_against = []
    content_type = "text"

    def is_applicable(self, element, *args, **kwargs):
        if element in self.match_against:
            return True
        return False

    def parse(self, element, *args, **kwargs):
        return ParseResult({
            "type": self.content_type,
            "content": element,
        }, True)


class TopLevelParser(BaseElementParser):
    content_type = "section"
    value = None

    def parse(self, element, *args, **kwargs):
        return ParseResult({
            "type": "top-level",
            self.content_type: self.value if self.value else element
        }, True)


class TopLevelStringParser(StringParser):
    content_type = "section"
    value = None

    def parse(self, element, *args, **kwargs):
        return ParseResult({
            "type": "top-level",
            self.content_type: self.value if self.value else element
        }, True)


class TopLevelRegexParser(RegexParser):
    content_type = "section"
    value = None

    def parse(self, element, *args, **kwargs):
        return ParseResult({
            "type": "top-level",
            self.content_type: self.value if self.value else self.regex_result.group(self.regex_el)
        }, True)
