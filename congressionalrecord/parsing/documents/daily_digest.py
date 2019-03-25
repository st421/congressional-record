from congressionalrecord.parsing.documents.base import DocParser
from congressionalrecord.parsing.sections import SectionParser
from congressionalrecord.parsing.elements import DateElementParser, StringMatchingParser


class BodyTitleParser(StringMatchingParser):
    applicable_strings = ["Daily Digest"]


class HighlightsSectionParser(SectionParser):
    def __init__(self, *args, **kwargs):
        self.DEFAULT_PARSERS.insert(0, DateElementParser())
        self.DEFAULT_PARSERS.insert(0, BodyTitleParser())
        super().__init__(*args, **kwargs)


class DDBodyParser(SectionParser):
    def __init__(self, *args, **kwargs):
        self.DEFAULT_PARSERS.insert(0, DateElementParser())
        self.DEFAULT_PARSERS.insert(0, BodyTitleParser())
        super().__init__(*args, **kwargs)


class DailyDigestParser(DocParser):
    def __init__(self, cr_file, *args, **kwargs):
        super().__init__(cr_file, DDBodyParser(), *args, **kwargs)
