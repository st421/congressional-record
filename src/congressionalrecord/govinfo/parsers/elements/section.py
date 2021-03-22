from congressionalrecord.govinfo.parsers.elements.base import (
    TopLevelRegexParser,
    TopLevelStringParser,
    RegexParser,
    StringParser
)


class RollCallParser(RegexParser):
    content_type = "rollcall"
    match_against = r'\[Roll(call)?( Vote)? No. \d+.*\]'


class JournalParser(TopLevelStringParser):
    value = "journal"
    match_against = [
        "THE JOURNAL"
    ]


class PrayerParser(TopLevelStringParser):
    value = "prayer"
    match_against = [
        "PRAYER"
    ]


class PledgeOfAllegianceParser(TopLevelStringParser):
    value = "pledge_of_allegiance"
    match_against = [
        "PLEDGE OF ALLEGIANCE"
    ]


class ResignationParser(TopLevelRegexParser):
    regex_el = "committee"
    match_against = r'^RESIGNATION AS MEMBER OF (?P<committee>([A-Za-z]+))$'


class TitleParser(TopLevelRegexParser):
    regex_el = "title"
    match_against = r'^(?P<title>([A-Z\s]+))$'


class SpeakerParser(RegexParser):
    regex_el = "speaker"
    match_against = r'\s*(HON|Mr|Ms|The)?(.)? (?P<speaker>([A-Z.,]+))$'
