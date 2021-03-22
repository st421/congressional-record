from congressionalrecord.govinfo.parsers.docs.base import DocParser
from congressionalrecord.govinfo.parsers.elements import (
    DateParser,
    StringParser,
    HeaderParser,
    PrimaryPageParser,
    SecondaryPageParser,
    SourceParser,
    SpeakerParser,
    TitleParser,
    SeparatorParser)


class BodyTitleParser(StringParser):
    match_against = ["Daily Digest"]


class DailyDigestParser(DocParser):

    DEFAULT_PARSERS = [
        DateParser(),
        BodyTitleParser(),
        HeaderParser(),
        SourceParser(),
        PrimaryPageParser(),
        SecondaryPageParser(),
        SeparatorParser()
    ]
