import pytest
from unittest.mock import patch, MagicMock
from briefme.main import fetch_rss_content

@patch('feedparser.parse')
def test_fetch_rss_content_returns_titles_and_summaries(mock_parse):
    mock_feed = MagicMock()
    mock_feed.entries = [
        {'title': 'Title 1', 'summary': 'Summary 1'},
        {'title': 'Title 2', 'summary': 'Summary 2'}
    ]
    mock_parse.return_value = mock_feed
    feeds = ['http://example.com/feed']
    result = fetch_rss_content(feeds, max_items=2)
    assert 'Title 1' in result
    assert 'Summary 2' in result
    assert result.count('Title') == 2
