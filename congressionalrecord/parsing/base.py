import re
import os
from bs4 import NavigableString
from html2ans.parsers.base import NullParser, BaseElementParser, ParseResult


class BaseParser(object):

    def __init__(self, in_data, *args, **kwargs):
        self.in_data = in_data

    def parse(self, *args, **kwargs):
        raise NotImplementedError()


class BaseDocParser(BaseParser):

    def __init__(self, cr_file, *args, **kwargs):
        self.doc_id = os.path.basename(cr_file.name.split(".htm")[0])
        super().__init__(cr_file.read())


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
