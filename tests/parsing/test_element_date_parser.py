import pytest
from html2ans.parsers.base import ParseResult
from congressionalrecord.parsing.elements import DateElementParser


@pytest.mark.parametrize('date_string', [
    "\n          Thursday, March 14, 2019",
    "Thursday, March 14, 2019",
    "      Thursday, March 14, 2019"
])
def test_date_parsing(date_string):
    assert DateElementParser().is_applicable(date_string)
    assert DateElementParser().parse(date_string) == ParseResult(None, True)
