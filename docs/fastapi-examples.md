# FastAPI Integration Examples

This guide provides comprehensive examples for integrating Revos with FastAPI applications.

## Basic FastAPI Setup

### Simple FastAPI Application

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from revos import TokenManager, get_langchain_extractor
from pydantic import BaseModel

# Global instances
token_manager: Optional[TokenManager] = None
extractor: Optional[LangChainExtractor] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan with proper cleanup."""
    global token_manager, extractor
    
    # Startup
    try:
        # Initialize token manager with background refresh
        # The refresh interval will be automatically taken from the config
        token_manager = TokenManager(settings_instance=config)
        
        # Create extractors (they get tokens immediately via Observer Pattern)
        # Extractors automatically pick up config from environment variables!
        extractor = get_langchain_extractor("gpt-4")  # Gets token instantly
        
        # Start background token refresh service
        # All extractors will automatically get updated tokens!
        await token_manager.start_background_service()
        
        print("✅ FastAPI services started successfully")
        
    except Exception as e:
        print(f"❌ Failed to start FastAPI services: {e}")
        raise
    
    yield
    
    # Shutdown
    print("🛑 Shutting down FastAPI services...")
    if token_manager:
        await token_manager.stop_background_service()
        print("✅ Background token service stopped")
    print("✅ FastAPI services shutdown completed")

# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Revos FastAPI application is running"}

@app.post("/extract")
async def extract_data(text: str):
    """Extract structured data from text."""
    try:
        result = extractor.extract(text, schema=PersonInfo)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Custom Prefix Configuration

### RUMBA FastAPI Example

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from revos import TokenManager, get_langchain_extractor
from revos.config.factory import create_config_with_prefixes

class RumbaConfig:
    def __init__(self):
        # Create custom configuration with RUMBA_ prefix
        self.revos_config = create_config_with_prefixes(
            revo_prefix="RUMBA_",
            llm_prefix="RUMBA_LLM_",
            logging_prefix="RUMBA_LOG_",
            token_prefix="RUMBA_TOKEN_"
        )

# Global instances
rumba_config: Optional[RumbaConfig] = None
token_manager: Optional[TokenManager] = None
extractor: Optional[LangChainExtractor] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management with RUMBA_ prefix configuration."""
    global rumba_config, token_manager, extractor
    
    print("🚀 Starting RUMBA FastAPI application...")
    
    # Startup
    try:
        # Initialize RUMBA configuration
        rumba_config = RumbaConfig()
        
        # Initialize token manager with background refresh
        token_manager = TokenManager(
            refresh_interval_minutes=rumba_config.revos_config.token_manager.refresh_interval_minutes,
            settings_instance=rumba_config.revos_config
        )
        
        # Start background token refresh service
        await token_manager.start_background_service()
        
        # Initialize extractor with RUMBA configuration (gets token instantly)
        extractor = get_langchain_extractor(
            model_name="gpt-4",  # Gets token instantly via Observer Pattern
            settings_instance=rumba_config.revos_config
        )
        
        print("✅ RUMBA FastAPI services started successfully")
        print(f"🎵 Using RUMBA_ prefix configuration")
        print(f"🤖 LLM Model: {extractor.get_current_model()}")
        print(f"🔄 Background token service: {token_manager.is_background_service_running()}")
        
    except Exception as e:
        print(f"❌ Failed to start RUMBA FastAPI services: {e}")
        raise
    
    yield
    
    # Shutdown
    print("🛑 Shutting down RUMBA FastAPI services...")
    if token_manager:
        await token_manager.stop_background_service()
        print("✅ Background token service stopped")
    print("✅ RUMBA FastAPI services shutdown completed")

# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "RUMBA FastAPI application is running"}

@app.post("/extract")
async def extract_data(text: str):
    """Extract structured data from text using RUMBA configuration."""
    try:
        result = extractor.extract(text, schema=PersonInfo)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Environment Configuration

### .env File for RUMBA Example

```bash
# RUMBA_ prefix configuration
RUMBA_CLIENT_ID=your_client_id
RUMBA_CLIENT_SECRET=your_client_secret
RUMBA_TOKEN_URL=https://api.revos.com/token
RUMBA_BASE_URL=https://api.revos.com
RUMBA_TOKEN_BUFFER_MINUTES=5
RUMBA_TOKEN_REFRESH_INTERVAL_MINUTES=45

# RUMBA_LLM_ prefix configuration
RUMBA_LLM_MODELS_GPT_4_MODEL=gpt-4
RUMBA_LLM_MODELS_GPT_4_TEMPERATURE=0.1
RUMBA_LLM_MODELS_GPT_4_MAX_TOKENS=2000

RUMBA_LLM_MODELS_CLAUDE_4_SONNET_MODEL=claude-4-sonnet
RUMBA_LLM_MODELS_CLAUDE_4_SONNET_TEMPERATURE=0.3
RUMBA_LLM_MODELS_CLAUDE_4_SONNET_MAX_TOKENS=4000

# RUMBA_LOG_ prefix configuration
RUMBA_LOG_LEVEL=INFO
RUMBA_LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# RUMBA_TOKEN_ prefix configuration
RUMBA_TOKEN_REFRESH_INTERVAL_MINUTES=45
RUMBA_TOKEN_MAX_FAILURES_BEFORE_FALLBACK=1
RUMBA_TOKEN_ENABLE_PERIODIC_REFRESH=true
RUMBA_TOKEN_ENABLE_FALLBACK=true
```

## Advanced FastAPI Patterns

### Multiple Model Support

```python
from fastapi import FastAPI
from revos import get_langchain_extractor

# Create extractors for different models
extractors = {
    "gpt-4": get_langchain_extractor("gpt-4"),
    "claude-4-sonnet": get_langchain_extractor("claude-4-sonnet"),
    "gpt-3.5-turbo": get_langchain_extractor("gpt-3.5-turbo")
}

@app.post("/extract/{model}")
async def extract_with_model(model: str, text: str):
    """Extract data using specified model."""
    if model not in extractors:
        return {"error": f"Model {model} not available"}
    
    try:
        result = extractors[model].extract(text, schema=PersonInfo)
        return {"success": True, "model": model, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

### Error Handling and Monitoring

```python
from fastapi import FastAPI, HTTPException
from revos import get_token_info

@app.get("/health")
async def health_check():
    """Health check endpoint with token status."""
    try:
        token_info = get_token_info()
        return {
            "status": "healthy",
            "token_info": token_info,
            "background_service": token_manager.is_background_service_running()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {e}")

@app.get("/token/status")
async def token_status():
    """Get current token status."""
    try:
        token_info = get_token_info()
        return {"success": True, "token_info": token_info}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Production Considerations

### Security

1. **Environment Variables**: Never commit `.env` files to version control
2. **Secrets Management**: Use proper secrets management in production
3. **HTTPS**: Always use HTTPS in production
4. **Rate Limiting**: Implement rate limiting for API endpoints

### Performance

1. **Connection Pooling**: Configure appropriate connection pools
2. **Caching**: Implement caching for frequently accessed data
3. **Background Tasks**: Use background tasks for long-running operations
4. **Monitoring**: Implement proper monitoring and logging

### Deployment

```dockerfile
# Dockerfile example
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Testing

### Unit Tests

```python
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

def test_extract_endpoint():
    with patch('revos.get_langchain_extractor') as mock_extractor:
        mock_extractor.return_value.extract.return_value = {"name": "John Doe"}
        
        response = client.post("/extract", json={"text": "John Doe is 30 years old"})
        
        assert response.status_code == 200
        assert response.json()["success"] is True
```

### Integration Tests

```python
def test_background_service_lifecycle():
    """Test background service startup and shutdown."""
    # Test service startup
    assert token_manager.is_background_service_running() is True
    
    # Test service shutdown
    await token_manager.stop_background_service()
    assert token_manager.is_background_service_running() is False
```

## Troubleshooting

### Common Issues

1. **Token Refresh Failures**: Check environment variables and network connectivity
2. **Model Not Found**: Verify model configuration in environment variables
3. **Background Service Issues**: Check logs for detailed error messages

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Your FastAPI application code
```

This guide provides comprehensive examples for integrating Revos with FastAPI applications, from basic setups to advanced production patterns.
