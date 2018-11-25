from html2ans.base import BaseHtmlAnsParser
from html2ans.parsers.base import NullParser, BaseElementParser

from congressionalrecord.parsing.base import RegexElementParser


class ChamberParser(RegexElementParser):
    applicable_regex = r'\[(?P<chamber>[A-Za-z\s]+)\]'


class PageParser(RegexElementParser):
    applicable_regex = r'\[Page[s]? (?P<pages>[\w\-]+)\]'


class SourceParser(RegexElementParser):
    applicable_regex = r'From the Congressional Record Online'\
        + r' through the Government (Publishing|Printing) Office \[www.gpo.gov\]$'


class RollCallParser(RegexElementParser):
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
