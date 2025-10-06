import datetime
from typing import List
from unittest.mock import MagicMock, patch

import pytest

from briefme.main import RSSItem, fetch_rss_content


@pytest.fixture
def in_scope_time():
    # get the current time
    dt_now = datetime.datetime.now(datetime.timezone.utc)
    dt_minus_12 = dt_now - datetime.timedelta(hours=12)

    # Step 2: Convert to 9-tuple (struct_time in UTC)
    return dt_minus_12.timetuple()  # returns a 9-tuple


@pytest.fixture
def too_old_time():
    # get the current time
    dt_now = datetime.datetime.now(datetime.timezone.utc)
    dt_minus_36 = dt_now - datetime.timedelta(hours=36)

    # Step 2: Convert to 9-tuple (struct_time in UTC)
    return dt_minus_36.timetuple()  # returns a 9-tuple


@patch("feedparser.parse")
def test_fetch_rss_content_returns_titles_and_summaries(
    mock_parse, in_scope_time, too_old_time
):
    mock_feed = MagicMock()
    entry1 = MagicMock()
    entry1.title = "Title 1"
    entry1.summary = "Summary 1"
    entry1.link = "http://example.com/1"
    entry1.published_parsed = in_scope_time

    # entry2 has no published date
    entry2 = MagicMock()
    entry2.title = "Title 2"
    entry2.summary = "Summary 2"
    entry2.link = "http://example.com/2"
    entry2.published_parsed = None

    # entry3 has a date from > 24h ago
    entry3 = MagicMock()
    entry3.title = "Title 3"
    entry3.summary = "Summary 3"
    entry3.link = "http://example.com/3"
    entry3.published_parsed = too_old_time

    mock_feed.entries = [entry1, entry2, entry3]
    mock_parse.return_value = mock_feed
    feeds = ["http://example.com/feed"]
    result: List[RSSItem] = fetch_rss_content(feeds, max_items=2)
    assert "Title 1" in [item.title for item in result]
    assert "Summary 2" not in [item.summary for item in result]
    assert "Summary 3" not in [item.summary for item in result]
    assert "http://example.com/1" in [item.link for item in result]
    assert len([item.title for item in result]) == 1
