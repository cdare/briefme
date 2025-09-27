import pytest
import os
import tempfile
import yaml
from unittest.mock import patch, mock_open, MagicMock
from briefme import config


class TestConfigLoading:
    """Test configuration loading and validation"""
    
    def test_default_values(self):
        """Test that default values are set correctly"""
        with patch.dict(os.environ, {}, clear=True):
            # Mock the required env vars to avoid validation error
            with patch.dict(os.environ, {
                'OPENAI_API_KEY': 'test-key',
                'EMAIL_FROM': 'test@example.com',
                'EMAIL_TO': 'recipient@example.com', 
                'EMAIL_PASSWORD': 'test-password'
            }):
                import importlib
                importlib.reload(config)
                
                assert config.SMTP_SERVER == "smtp.gmail.com"
                assert config.SMTP_PORT == 465
                assert config.TITLE == "Your Security News Digest"
                assert config.LOG_LEVEL == "INFO"
                assert config.MAX_ITEMS_PER_FEED == 5
                assert config.MAX_AGE_HOURS == 24
                assert config.OPENAI_MAX_TOKENS == 800

    def test_environment_variable_loading(self):
        """Test that environment variables override defaults"""
        env_vars = {
            'OPENAI_API_KEY': 'custom-api-key',
            'EMAIL_FROM': 'custom@example.com',
            'EMAIL_TO': 'custom-recipient@example.com',
            'EMAIL_PASSWORD': 'custom-password',
            'SMTP_SERVER': 'custom.smtp.com',
            'SMTP_PORT': '587',
            'TITLE': 'Custom Security Digest',
            'LOG_LEVEL': 'DEBUG',
            'MAX_ITEMS_PER_FEED': '10',
            'MAX_AGE_HOURS': '48',
            'OPENAI_MAX_TOKENS': '1000'
        }
        
        with patch.dict(os.environ, env_vars):
            import importlib
            importlib.reload(config)
            
            assert config.OPENAI_API_KEY == 'custom-api-key'
            assert config.EMAIL_FROM == 'custom@example.com'
            assert config.EMAIL_TO == 'custom-recipient@example.com'
            assert config.EMAIL_PASSWORD == 'custom-password'
            assert config.SMTP_SERVER == 'custom.smtp.com'
            assert config.SMTP_PORT == 587
            assert config.TITLE == 'Custom Security Digest'
            assert config.LOG_LEVEL == 'DEBUG'
            assert config.MAX_ITEMS_PER_FEED == 10
            assert config.MAX_AGE_HOURS == 48
            assert config.OPENAI_MAX_TOKENS == 1000

    def test_required_environment_variables_validation(self):
        """Test that missing required environment variables raise ValueError"""
        # Test with no environment variables
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="Missing required environment variables"):
                import importlib
                importlib.reload(config)
        
        # Test with some missing variables
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test-key',
            'EMAIL_FROM': 'test@example.com'
            # Missing EMAIL_TO and EMAIL_PASSWORD
        }, clear=True):
            with pytest.raises(ValueError, match="Missing required environment variables"):
                import importlib
                importlib.reload(config)

    def test_integer_conversion(self):
        """Test that string environment variables are properly converted to integers"""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test-key',
            'EMAIL_FROM': 'test@example.com',
            'EMAIL_TO': 'recipient@example.com',
            'EMAIL_PASSWORD': 'test-password',
            'SMTP_PORT': '465',
            'MAX_ITEMS_PER_FEED': '15',
            'MAX_AGE_HOURS': '72',
            'OPENAI_MAX_TOKENS': '1200'
        }):
            import importlib
            importlib.reload(config)
            
            assert isinstance(config.SMTP_PORT, int)
            assert isinstance(config.MAX_ITEMS_PER_FEED, int)
            assert isinstance(config.MAX_AGE_HOURS, int)
            assert isinstance(config.OPENAI_MAX_TOKENS, int)
            
            assert config.SMTP_PORT == 465
            assert config.MAX_ITEMS_PER_FEED == 15
            assert config.MAX_AGE_HOURS == 72
            assert config.OPENAI_MAX_TOKENS == 1200


class TestFeedsYamlLoading:
    """Test RSS feeds YAML file loading"""
    
    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_feeds_yaml_loading_success(self, mock_file, mock_exists):
        """Test successful loading of feeds.yaml"""
        mock_exists.return_value = True
        yaml_content = {
            'feeds': [
                'https://example.com/feed1',
                'https://example.com/feed2',
                'https://example.com/feed3'
            ]
        }
        mock_file.return_value.read.return_value = yaml.dump(yaml_content)
        
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test-key',
            'EMAIL_FROM': 'test@example.com',
            'EMAIL_TO': 'recipient@example.com',
            'EMAIL_PASSWORD': 'test-password'
        }):
            with patch('yaml.safe_load', return_value=yaml_content):
                import importlib
                importlib.reload(config)
                
                assert config.RSS_FEEDS == [
                    'https://example.com/feed1',
                    'https://example.com/feed2', 
                    'https://example.com/feed3'
                ]

    @patch("os.path.exists")
    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_feeds_yaml_file_not_found(self, mock_file, mock_exists):
        """Test handling when feeds.yaml file is not found"""
        mock_exists.return_value = False
        
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test-key',
            'EMAIL_FROM': 'test@example.com',
            'EMAIL_TO': 'recipient@example.com',
            'EMAIL_PASSWORD': 'test-password'
        }):
            import importlib
            importlib.reload(config)
            
            assert config.RSS_FEEDS == []

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_feeds_yaml_invalid_format(self, mock_file, mock_exists):
        """Test handling of invalid YAML format"""
        mock_exists.return_value = True
        
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test-key',
            'EMAIL_FROM': 'test@example.com',
            'EMAIL_TO': 'recipient@example.com',
            'EMAIL_PASSWORD': 'test-password'
        }):
            with patch('yaml.safe_load', side_effect=yaml.YAMLError("Invalid YAML")):
                import importlib
                importlib.reload(config)
                
                assert config.RSS_FEEDS == []

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_feeds_yaml_missing_feeds_key(self, mock_file, mock_exists):
        """Test handling when feeds.yaml doesn't have 'feeds' key"""
        mock_exists.return_value = True
        yaml_content = {'other_key': 'value'}
        
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test-key',
            'EMAIL_FROM': 'test@example.com',
            'EMAIL_TO': 'recipient@example.com',
            'EMAIL_PASSWORD': 'test-password'
        }):
            with patch('yaml.safe_load', return_value=yaml_content):
                import importlib
                importlib.reload(config)
                
                assert config.RSS_FEEDS == []


class TestTemplatesAndPrompts:
    """Test email template and agent prompt configuration"""
    
    def test_email_template_exists(self):
        """Test that email template is properly defined"""
        assert config.EMAIL_TEMPLATE is not None
        assert isinstance(config.EMAIL_TEMPLATE, str)
        assert len(config.EMAIL_TEMPLATE) > 0
        
        # Check for required template placeholders
        assert '{title}' in config.EMAIL_TEMPLATE
        assert '{summary}' in config.EMAIL_TEMPLATE
        
        # Check for basic HTML structure
        assert '<!DOCTYPE html>' in config.EMAIL_TEMPLATE
        assert '<html' in config.EMAIL_TEMPLATE
        assert '</html>' in config.EMAIL_TEMPLATE

    def test_agent_prompt_exists(self):
        """Test that agent prompt is properly defined"""
        assert config.AGENT_PROMPT is not None
        assert isinstance(config.AGENT_PROMPT, str)
        assert len(config.AGENT_PROMPT) > 0
        
        # Check for key instructions
        assert 'cybersecurity' in config.AGENT_PROMPT.lower()
        assert 'json' in config.AGENT_PROMPT.lower()
        assert 'html' in config.AGENT_PROMPT.lower()

    def test_agent_prompt_includes_max_age_hours(self):
        """Test that agent prompt includes the configurable MAX_AGE_HOURS"""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test-key',
            'EMAIL_FROM': 'test@example.com',
            'EMAIL_TO': 'recipient@example.com',
            'EMAIL_PASSWORD': 'test-password',
            'MAX_AGE_HOURS': '48'
        }):
            import importlib
            importlib.reload(config)
            
            assert '48 hours' in config.AGENT_PROMPT


class TestConfigIntegration:
    """Test overall configuration integration"""
    
    def test_all_configs_load_without_error(self):
        """Test that all configurations can be loaded without errors"""
        with patch.dict(os.environ, {
            'OPENAI_API_KEY': 'test-key',
            'EMAIL_FROM': 'test@example.com',
            'EMAIL_TO': 'recipient@example.com',
            'EMAIL_PASSWORD': 'test-password'
        }):
            with patch("os.path.exists", return_value=True):
                with patch("builtins.open", mock_open(read_data="feeds:\n  - https://example.com")):
                    with patch('yaml.safe_load', return_value={'feeds': ['https://example.com']}):
                        import importlib
                        importlib.reload(config)
                        
                        # Verify all major config items exist
                        assert hasattr(config, 'OPENAI_API_KEY')
                        assert hasattr(config, 'EMAIL_FROM')
                        assert hasattr(config, 'EMAIL_TO')
                        assert hasattr(config, 'EMAIL_PASSWORD')
                        assert hasattr(config, 'RSS_FEEDS')
                        assert hasattr(config, 'EMAIL_TEMPLATE')
                        assert hasattr(config, 'AGENT_PROMPT')
                        assert hasattr(config, 'MAX_ITEMS_PER_FEED')
                        assert hasattr(config, 'MAX_AGE_HOURS')
                        assert hasattr(config, 'OPENAI_MAX_TOKENS')
