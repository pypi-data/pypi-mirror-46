"""Utility module"""
from __future__ import absolute_import
from six.moves import range


def parse_fid(fid):
    """
    Parse the folder id argument
    """
    # Use hyphen to indicate a range
    if "-" in fid:
        first, second = fid.split("-")
        second = first[:-len(second)] + second
        ids = tuple(range(int(first), int(second) + 1))
    else:
        ids = (int(fid), )

    return ids


def test_parse_fid():
    """
    Test the parsing of the folder ids
    """
    assert parse_fid("100-10") == tuple(range(100, 111))
    assert parse_fid("12345-500") == tuple(range(12345, 12501))
    assert parse_fid("87873-900") == tuple(range(87873, 87901))
