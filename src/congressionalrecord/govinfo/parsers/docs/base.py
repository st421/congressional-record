import os
from bs4 import BeautifulSoup, NavigableString
from html2ans.base import BaseHtmlAnsParser
from html2ans.parsers.text import ParagraphParser
from congressionalrecord.govinfo.parsers.elements import (
    HeaderParser,
    PrimaryPageParser,
    SecondaryPageParser,
    SourceParser,
    SpeakerParser,
    TitleParser,
    JournalParser,
    PrayerParser,
    SeparatorParser,
    RollCallParser)


class DocParser(BaseHtmlAnsParser):

    DEFAULT_PARSERS = []
    BACKUP_PARSERS = [
        ParagraphParser()
    ]

    def __init__(self, *args, header_parser=None, terminal_parser=None, **kwargs):
        self.header_parser = header_parser
        self.terminal_parser = terminal_parser
        super().__init__(*args, default_parsers=self.DEFAULT_PARSERS, **kwargs)

    def generate_ans(self, html, *args, **kwargs):
        soup = BeautifulSoup(html, self.soup_parse_lib)
        lines = list(map(
            lambda line: NavigableString(line.strip()),
            soup.html.body.pre.text.split('\n')))
        found_start = False
        if self.header_parser or self.terminal_parser:
            section_lines = []
            for line in lines:
                if self.header_parser.is_applicable(line):
                    found_start = True
                if found_start:
                    section_lines.append(line)
                    if self.terminal_parser and self.terminal_parser.is_applicable(line):
                        break
        else:
            section_lines = lines
        return self._parse_elements(section_lines)

    def parse(self, data, doc_id, **kwargs):
        output = {
            "id": doc_id,
            "content": []
        }
        parsed_item_raw = self.generate_ans(data, start_tag="pre")
        for sub_item in parsed_item_raw:
            if sub_item.get("type") == "top-level":
                sub_item.pop("type")
                output.update(sub_item)
            else:
                output["content"].append(sub_item)
        return output
