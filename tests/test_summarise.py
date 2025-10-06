from unittest.mock import MagicMock, patch

from briefme.main import RSSItem, summarise_text


@patch("briefme.main.OpenAI")
def test_summarise_text_calls_openai_and_returns_content(mock_openai):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.output_text = "<div>summary</div>"
    mock_client.responses.create.return_value = mock_response
    mock_openai.return_value = mock_client

    items = [
        RSSItem(
            title="Test Title",
            summary="Test Summary",
            link="http://example.com",
        )
    ]
    result = summarise_text(items, max_words=100)
    assert "summary" in result

    # Verify the correct API was called with proper parameters
    mock_client.responses.create.assert_called_once()
    call_args = mock_client.responses.create.call_args
    assert call_args.kwargs["model"] == "gpt-4o-mini"
    assert "instructions" in call_args.kwargs
    assert "input" in call_args.kwargs
