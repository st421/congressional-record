import pytest
from congressionalrecord.parsing.elements import DateElementParser


def test_date_parsing():
    assert DateElementParser().is_applicable("          Thursday, March 14, 2019")
