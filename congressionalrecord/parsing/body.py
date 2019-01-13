from bs4 import BeautifulSoup, NavigableString
from html2ans.base import BaseHtmlAnsParser
from html2ans.parsers.base import NullParser
from html2ans.parsers.text import ParagraphParser

from congressionalrecord.parsing.elements import (
    HeaderParser,
    ChamberParser,
    PageParser,
    TitleParser,
    SeparatorParser,
    RollCallParser,
    SpeakerParser,
    SourceParser)


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
