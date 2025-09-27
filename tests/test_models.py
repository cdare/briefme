import pytest
from briefme.main import RSSItem

class TestRSSItem:
    def test_rss_item_creation(self):
        """Test RSSItem creation with all fields"""
        item = RSSItem(
            title="Test Title",
            summary="Test Summary", 
            link="https://example.com"
        )
        
        assert item.title == "Test Title"
        assert item.summary == "Test Summary"
        assert item.link == "https://example.com"
    
    def test_rss_item_dict_conversion(self):
        """Test RSSItem converts to dict properly for JSON serialization"""
        item = RSSItem(
            title="Test Title",
            summary="Test Summary",
            link="https://example.com"
        )
        
        item_dict = item.__dict__
        
        assert item_dict == {
            'title': 'Test Title',
            'summary': 'Test Summary', 
            'link': 'https://example.com'
        }