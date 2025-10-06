import pytest
from unittest.mock import patch, MagicMock
from briefme.main import send_email


@patch('briefme.main.smtplib.SMTP_SSL')
def test_send_email_success(mock_smtp):
    """Test successful email sending"""
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server
    
    with patch('briefme.main.EMAIL_FROM', 'from@example.com'), \
         patch('briefme.main.EMAIL_TO', 'to@example.com'), \
         patch('briefme.main.EMAIL_PASSWORD', 'password'), \
         patch('briefme.main.SMTP_SERVER', 'smtp.example.com'), \
         patch('briefme.main.SMTP_PORT', 465):
        
        send_email('Test Subject', '<div>Test Body</div>')
        
        mock_server.login.assert_called_once_with('from@example.com', 'password')
        mock_server.sendmail.assert_called_once()


@patch('briefme.main.smtplib.SMTP_SSL')
def test_send_email_handles_smtp_failure(mock_smtp):
    """Test email sending handles SMTP failures"""
    mock_smtp.side_effect = Exception("SMTP connection failed")
    
    with patch('briefme.main.EMAIL_FROM', 'from@example.com'), \
         patch('briefme.main.EMAIL_TO', 'to@example.com'), \
         patch('briefme.main.EMAIL_PASSWORD', 'password'), \
         patch('briefme.main.SMTP_SERVER', 'smtp.example.com'), \
         patch('briefme.main.SMTP_PORT', 465):
        
        with pytest.raises(Exception, match="SMTP connection failed"):
            send_email('Test Subject', '<div>Test Body</div>')
