from bs4 import BeautifulSoup, NavigableString
from html2ans.base import BaseHtmlAnsParser
from html2ans.parsers.base import NullParser
from html2ans.parsers.text import ParagraphParser
from congressionalrecord.congress.parsers.elements import TableRowParser


class SenateRecordParser(BaseHtmlAnsParser):
    DEFAULT_PARSERS = [
        TableRowParser(),
        NullParser(),  # comments
    ]

    BACKUP_PARSERS = [
        ParagraphParser()
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, default_parsers=self.DEFAULT_PARSERS, **kwargs)

