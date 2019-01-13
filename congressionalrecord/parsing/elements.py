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
    applicable_regex = r'^ \s*(?P<title>[A-Z]+[0-9.,]*)$'


class SpeakerParser(RegexElementParser):
    content_type = "speaker"
    regex_el = "speaker"
    applicable_regex = r'\s*(HON|Mr|Ms|The)?(.)? (?P<speaker>([A-Z.,]+))$'


class SeparatorParser(RegexNullElementParser):
    applicable_regex = r'^\s*[_]+\s*$'
