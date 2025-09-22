"""
Pytest configuration and fixtures.
"""

import pytest
import os
import tempfile
from unittest.mock import Mock, patch


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    settings = Mock()
    settings.revos.client_id = "test-client-id"
    settings.revos.client_secret = "test-client-secret"
    settings.revos.token_url = "https://test.com/oauth/token"
    settings.revos.base_url = "https://test.com/api"
    settings.revos.token_buffer_minutes = 5
    settings.revos.max_retries = 3
    settings.revos.request_timeout = 30
    
    settings.llm.model = "gpt-3.5-turbo"
    settings.llm.temperature = 0.1
    settings.llm.max_tokens = 1000
    settings.llm.top_p = 1.0
    settings.llm.frequency_penalty = 0.0
    settings.llm.presence_penalty = 0.0
    
    return settings


@pytest.fixture
def mock_llm_models_config():
    """Mock LLM models configuration for testing."""
    from revos.config.llm_models import LLMModelConfig, LLMModelsConfig
    
    models_config = LLMModelsConfig()
    
    # Add test models
    models_config.add_model("test-model-1", LLMModelConfig(
        model="gpt-3.5-turbo",
        description="Test model 1"
    ))
    
    models_config.add_model("test-model-2", LLMModelConfig(
        model="gpt-4",
        description="Test model 2"
    ))
    
    return models_config


@pytest.fixture
def temp_config_file():
    """Create a temporary configuration file for testing."""
    config_data = {
        "revo": {
            "client_id": "temp-client-id",
            "client_secret": "temp-client-secret"
        },
        "llm": {
            "model": "gpt-4",
            "temperature": 0.8
        }
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        import yaml
        yaml.dump(config_data, f)
        temp_file = f.name
    
    yield temp_file
    
    # Cleanup
    try:
        os.unlink(temp_file)
    except OSError:
        pass


@pytest.fixture
def mock_token_response():
    """Mock token response for testing."""
    return {
        "access_token": "test-access-token",
        "expires_in": 3600,
        "token_type": "Bearer"
    }


@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing."""
    response = Mock()
    response.content = '{"task": "test", "result": "success", "confidence": 0.95}'
    return response


@pytest.fixture(autouse=True)
def clean_environment():
    """Clean environment variables and global state before each test."""
    # Store original environment
    original_env = os.environ.copy()
    
    # Clear Revos-specific environment variables
    revo_vars = [key for key in os.environ.keys() if key.startswith('REVOS_')]
    for var in revo_vars:
        del os.environ[var]
    
    # Clear global state
    try:
        from revos.tokens.observer import set_global_config, get_global_notifier
        from revos.llm.tools import _langchain_extractors
        set_global_config(None)
        notifier = get_global_notifier()
        notifier.clear_observers()
        _langchain_extractors.clear()
    except ImportError:
        # Ignore import errors during test collection
        pass
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)
    
    # Clear global state again
    try:
        from revos.tokens.observer import set_global_config, get_global_notifier
        from revos.llm.tools import _langchain_extractors
        set_global_config(None)
        notifier = get_global_notifier()
        notifier.clear_observers()
        _langchain_extractors.clear()
    except ImportError:
        # Ignore import errors during test collection
        pass


@pytest.fixture
def mock_chat_openai():
    """Mock ChatOpenAI for testing."""
    with patch('revos.llm.tools.ChatOpenAI') as mock_chat:
        mock_llm = Mock()
        mock_chat.return_value = mock_llm
        yield mock_chat, mock_llm


@pytest.fixture
def mock_requests():
    """Mock requests for testing."""
    with patch('requests.post') as mock_post:
        yield mock_post


@pytest.fixture
def mock_httpx():
    """Mock httpx for testing."""
    with patch('httpx.post') as mock_post:
        yield mock_post


@pytest.fixture
def mock_get_revos_token():
    """Mock get_revos_token for testing."""
    with patch('revos.auth.tokens.get_revos_token') as mock_token:
        mock_token.return_value = "test-token"
        yield mock_token


@pytest.fixture
def mock_invalidate_revos_token():
    """Mock invalidate_revos_token for testing."""
    with patch('revos.auth.tokens.invalidate_revos_token') as mock_invalidate:
        yield mock_invalidate


@pytest.fixture
def mock_get_settings():
    """Mock get_settings for testing."""
    with patch('revos.config.main.get_settings') as mock_settings:
        yield mock_settings


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Pytest configuration
def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection."""
    for item in items:
        # Add unit marker to tests that don't have any marker
        if not any(marker.name in ['slow', 'integration', 'unit'] for marker in item.iter_markers()):
            item.add_marker(pytest.mark.unit)
