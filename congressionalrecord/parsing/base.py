import re
from bs4 import BeautifulSoup, NavigableString
from html2ans.base import BaseHtmlAnsParser
from html2ans.parsers.base import NullParser, BaseElementParser
from html2ans.parsers.text import ParagraphParser


class BaseParser(object):

    def __init__(self, in_data, *args, **kwargs):
        self.in_data = in_data

    def parse(self, *args, **kwargs):
        raise NotImplementedError()


class BaseDocParser(BaseParser):

    def __init__(self, cr_file, *args, **kwargs):
        self.filename = cr_file.name
        super().__init__(cr_file.read())


class RegexElementParser(BaseElementParser):
    applicable_elements = [NavigableString]
    applicable_regex = None

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
        return self.regex_result
