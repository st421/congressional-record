from bs4 import BeautifulSoup, NavigableString
from html2ans.base import BaseHtmlAnsParser
from html2ans.parsers.base import NullParser, BaseElementParser, ParseResult

from congressionalrecord.parsing.base import RegexTopLevelElementParser, RegexParagraphParser


class ChamberParser(RegexTopLevelElementParser):
    name = "doc_type"
    applicable_regex = r'\[(?P<chamber>[A-Za-z\s]+)\]'


class PageParser(RegexTopLevelElementParser):
    name = "page"
    applicable_regex = r'\[Page[s]? (?P<pages>[\w\-]+)\]'


class SourceParser(RegexTopLevelElementParser):
    name = "source"
    applicable_regex = r'From the Congressional Record Online'\
        + r' through the Government (Publishing|Printing) Office \[www.gpo.gov\]$'

    def parse(self, element, *args, **kwargs):
        return ParseResult(None, True)


class RollCallParser(RegexTopLevelElementParser):
    name = "rollcall"
    applicable_regex = r'\[Roll(call)?( Vote)? No. \d+.*\]'



class CRBodyParser(BaseHtmlAnsParser):

    DEFAULT_PARSERS = [
        ChamberParser(),
        PageParser(),
        SourceParser(),
        RollCallParser(),
        NullParser(),  # comments
    ]

    BACKUP_PARSERS = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, default_parsers=self.DEFAULT_PARSERS, **kwargs)

    def generate_ans(self, html, *args, **kwargs):
        soup = BeautifulSoup(html, self.soup_parse_lib)
        lines = soup.html.body.pre.text.split('\n')
        return self._parse_elements(list(map(NavigableString, lines)))
