import pytest
from unittest.mock import patch, MagicMock
from briefme.main import summarise_text

@patch('briefme.main.OpenAI')
def test_summarise_text_calls_openai_and_returns_content(mock_openai):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_choice.message.content = '<div>summary</div>'
    mock_response.choices = [mock_choice]
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai.return_value = mock_client

    text = 'Test input text.'
    result = summarise_text(text, max_words=100)
    assert 'summary' in result
