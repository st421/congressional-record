from bs4 import BeautifulSoup, NavigableString
from html2ans.base import BaseHtmlAnsParser
from html2ans.parsers.base import NullParser
from html2ans.parsers.text import ParagraphParser
from congressionalrecord.parsing.base import (RegexElementParser,
                                              RegexNullElementParser,
                                              RegexTopLevelElementParser)


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


class CRBodyParser(BaseHtmlAnsParser):

    DEFAULT_PARSERS = [
        HeaderParser(),
        ChamberParser(),
        PageParser(),
        SourceParser(),
        SpeakerParser(),
        TitleParser(),
        SeparatorParser(),
        RollCallParser(),
        NullParser(),  # comments
    ]

    BACKUP_PARSERS = [
        ParagraphParser()
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, default_parsers=self.DEFAULT_PARSERS, **kwargs)

    def generate_ans(self, html, *args, **kwargs):
        soup = BeautifulSoup(html, self.soup_parse_lib)
        lines = soup.html.body.pre.text.split('\n')
        return self._parse_elements(list(map(NavigableString, lines)))
