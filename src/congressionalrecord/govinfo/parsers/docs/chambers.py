from congressionalrecord.govinfo.parsers.docs.base import DocParser
from congressionalrecord.govinfo.parsers.elements.base import TopLevelRegexParser

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
    RollCallParser,
    PledgeOfAllegianceParser,
    ResignationParser)


class ChamberParser(TopLevelRegexParser):
    content_type = "doc_type"
    regex_el = "chamber"
    match_against = r'\[(?P<chamber>[A-Za-z\s]+)\]'


class ChamberDocParser(DocParser):

    DEFAULT_PARSERS = [
        ChamberParser(),
        HeaderParser(),
        PrimaryPageParser(),
        SecondaryPageParser(),
        SourceParser(),
        SeparatorParser(),
        PrayerParser(),
        JournalParser(),
        PledgeOfAllegianceParser(),
        ResignationParser(),
        TitleParser(),
        SpeakerParser(),
        RollCallParser()
    ]


class HouseParser(ChamberDocParser):
    pass


class SenateParser(ChamberDocParser):
    pass
