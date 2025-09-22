# Token Management

This guide covers advanced token management features including background refresh, custom settings, and error handling.

## Overview

The Revos library provides comprehensive token management with:

- **Automatic token refresh** with configurable intervals
- **Background token refresh** for continuous operation
- **Automatic extractor updates** via Observer Pattern
- **Custom settings support** for different environments
- **Robust error handling** with retry logic and fallback mechanisms
- **Token lifecycle management** with expiration tracking

## Basic Token Management

### Simple Token Usage

```python
from revos import get_revos_token

# Get current token (refresh if needed)
token = get_revos_token()

# Force refresh token
token = get_revos_token(force_refresh=True)

# Use fallback authentication method
token = get_revos_token(use_fallback=True)
```

### Token Manager

```python
from revos import TokenManager
import asyncio

# Create token manager
token_manager = TokenManager(refresh_interval_minutes=45)

# Start background refresh service
async def main():
    await token_manager.start_background_service()
    
    # Your application code here
    
    # Stop background service
    await token_manager.stop_background_service()

asyncio.run(main())
```

## Background Token Refresh

### Automatic Background Refresh

```python
from revos import TokenManager
import asyncio

async def main():
    # Create token manager with custom refresh interval
    token_manager = TokenManager(refresh_interval_minutes=30)
    
    # Start background refresh service
    await token_manager.start_background_service()
    
    print(f"Background service running: {token_manager.is_background_service_running()}")
    
    # Let it run for a while
    await asyncio.sleep(300)  # 5 minutes
    
    # Stop the service
    await token_manager.stop_background_service()
    print("Background service stopped")

asyncio.run(main())
```

### Custom Settings with Background Refresh

```python
from revos import create_config_with_prefixes, TokenManager
import asyncio

async def main():
    # Create custom configuration
    config = create_config_with_prefixes(
        revo_prefix="MYAPP_",
        llm_prefix="MYAPP_LLM_",
        logging_prefix="MYAPP_LOG_",
        token_prefix="MYAPP_TOKEN_"
    )
    
# Create token manager with custom settings
# The refresh interval will be automatically taken from the config
token_manager = TokenManager(settings_instance=config)
    
    # Start background service
    await token_manager.start_background_service()
    
    # Your application code here
    
    # Stop background service
    await token_manager.stop_background_service()

asyncio.run(main())
```

## Automatic Extractor Updates (Observer Pattern)

The Revos library implements a **perfect Observer Pattern** that automatically updates all extractors when tokens are refreshed. This ensures that your LangChain extractors always use the latest authentication tokens with **zero duplicate requests**.

### How It Works

1. **Immediate Token Provision**: When extractors register as observers, they get tokens instantly
2. **Zero Duplicate Requests**: Extractors never make their own token requests when TokenManager is running
3. **Automatic Registration**: Extractors automatically register as observers upon creation
4. **Token Refresh Notification**: When TokenManager refreshes tokens, all registered extractors are notified
5. **Efficient Updates**: Extractors update their LLM instances with the new tokens without additional API calls

### Basic Usage

```python
from revos import TokenManager, get_langchain_extractor
import asyncio

async def main():
    # Create token manager
    token_manager = TokenManager(settings_instance=config)
    
    # Create extractors (they get tokens immediately via Observer Pattern)
    # Extractors automatically pick up config from environment variables!
    extractor1 = get_langchain_extractor("gpt-4")  # Gets token instantly
    extractor2 = get_langchain_extractor("claude-4")  # Gets token instantly
    
    # Start background token refresh
    await token_manager.start_background_service()
    
    # Your application code here
    # All extractors automatically use fresh tokens!
    
    # Stop background service
    await token_manager.stop_background_service()

asyncio.run(main())
```

### FastAPI Integration

```python
from fastapi import FastAPI
from revos import TokenManager, get_langchain_extractor

app = FastAPI()

# Global variables for token manager and extractors
token_manager = None
extractors = {}

@app.on_event("startup")
async def startup_event():
    global token_manager, extractors
    
    # Create token manager
    token_manager = TokenManager(settings_instance=config)
    
    # Create extractors (they get tokens immediately via Observer Pattern)
    # Extractors automatically pick up config from environment variables!
    extractors["gpt-4"] = get_langchain_extractor("gpt-4")  # Gets token instantly
    extractors["claude-4"] = get_langchain_extractor("claude-4")  # Gets token instantly
    
    # Start background token refresh
    await token_manager.start_background_service()

@app.on_event("shutdown")
async def shutdown_event():
    global token_manager
    if token_manager:
        await token_manager.stop_background_service()

@app.post("/extract")
async def extract_data(data: dict):
    # Use extractors - they automatically have fresh tokens!
    result = await extractors["gpt_4"].extract(PersonInfo, prompt_template, **data)
    return result
```

### Key Benefits

- **⚡ Zero Duplicate Requests**: Extractors never make their own token requests
- **🚀 Immediate Availability**: Extractors get tokens instantly upon registration
- **🔄 Automatic Updates**: Extractors get new tokens without manual intervention
- **🛡️ Background-Safe**: Perfect for FastAPI background token management
- **📈 Multiple Extractors**: All get updated simultaneously
- **🎯 Efficient Architecture**: Single TokenManager serves all extractors
- **🏗️ Clean Architecture**: Observer pattern is elegant and scalable

### Manual Token Refresh

If you need to manually refresh tokens and update extractors:

```python
from revos import TokenManager, get_langchain_extractor

# Create token manager and extractors
token_manager = TokenManager(settings_instance=config)
extractor = get_langchain_extractor("gpt_4", settings_instance=config)

# Manually refresh tokens (this will notify all extractors)
success = token_manager.refresh_extractor()

if success:
    print("Tokens refreshed and all extractors updated!")
else:
    print("Token refresh failed")
```

## Token Lifecycle Management

### Token Information

```python
from revos import get_token_info, get_consecutive_failures

# Get token information
token_info = get_token_info()
print(f"Has token: {token_info['has_token']}")
print(f"Expires at: {token_info.get('expires_at')}")
print(f"Time until expiry: {token_info.get('time_until_expiry')} seconds")

# Get consecutive failures count
failures = get_consecutive_failures()
print(f"Consecutive failures: {failures}")
```

### Token Invalidation

```python
from revos import invalidate_revos_token, reset_token_manager

# Invalidate current token
invalidate_revos_token()

# Reset token manager (useful for testing)
reset_token_manager()
```

## Advanced Configuration

### Custom Token Manager Settings

```python
from revos import create_config_with_prefixes, TokenManager

# Create custom configuration
config = create_config_with_prefixes(
    revo_prefix="MYAPP_",
    token_prefix="MYAPP_TOKEN_"
)

# Create token manager with custom settings
token_manager = TokenManager(
    refresh_interval_minutes=30,
    settings_instance=config
)

# The background service will use the custom settings
await token_manager.start_background_service()
```

### Environment Variables for Token Management

```bash
# Token management settings
TOKEN_REFRESH_INTERVAL_MINUTES=45
TOKEN_MAX_FAILURES_BEFORE_FALLBACK=1
TOKEN_ENABLE_PERIODIC_REFRESH=true
TOKEN_ENABLE_FALLBACK=true

# Custom prefix example
MYAPP_TOKEN_REFRESH_INTERVAL_MINUTES=30
MYAPP_TOKEN_MAX_FAILURES_BEFORE_FALLBACK=2
MYAPP_TOKEN_ENABLE_PERIODIC_REFRESH=true
MYAPP_TOKEN_ENABLE_FALLBACK=true
```

## Error Handling and Recovery

### Retry Logic

```python
from revos import get_revos_token
import time

def get_token_with_retry(max_retries=3, delay=1):
    """Get token with retry logic."""
    for attempt in range(max_retries):
        try:
            token = get_revos_token(force_refresh=True)
            return token
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay * (2 ** attempt))  # Exponential backoff
            else:
                raise

# Use with retry logic
try:
    token = get_token_with_retry()
    print(f"Token obtained: {token[:20]}...")
except Exception as e:
    print(f"Failed to get token after retries: {e}")
```

### Fallback Authentication

```python
from revos import get_revos_token

def get_token_with_fallback():
    """Get token with fallback authentication."""
    try:
        # Try original method first
        token = get_revos_token(use_fallback=False)
        return token
    except Exception as e:
        print(f"Original method failed: {e}")
        try:
            # Try fallback method
            token = get_revos_token(use_fallback=True)
            return token
        except Exception as e2:
            print(f"Fallback method also failed: {e2}")
            raise

# Use with fallback
try:
    token = get_token_with_fallback()
    print(f"Token obtained: {token[:20]}...")
except Exception as e:
    print(f"Both authentication methods failed: {e}")
```

## Monitoring and Health Checks

### Health Check Endpoint

```python
from fastapi import FastAPI, HTTPException
from revos import get_token_info

app = FastAPI()

@app.get("/health")
async def health_check():
    """Health check with token status."""
    try:
        token_info = get_token_info()
        failures = get_consecutive_failures()
        
        if failures > 5:
            raise HTTPException(
                status_code=503, 
                detail=f"Too many consecutive failures: {failures}"
            )
        
        return {
            "status": "healthy",
            "token_info": token_info,
            "consecutive_failures": failures
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Token Status Monitoring

```python
import asyncio
from revos import get_token_info, get_consecutive_failures

async def monitor_tokens():
    """Monitor token status periodically."""
    while True:
        try:
            token_info = get_token_info()
            failures = get_consecutive_failures()
            
            print(f"Token status: {token_info}")
            print(f"Consecutive failures: {failures}")
            
            if failures > 3:
                print("WARNING: High failure count detected")
            
            await asyncio.sleep(60)  # Check every minute
        except Exception as e:
            print(f"Monitoring error: {e}")
            await asyncio.sleep(30)

# Run monitoring in background
asyncio.create_task(monitor_tokens())
```

## Production Considerations

### Security Best Practices

1. **Environment Variables**: Store credentials in secure environment variables
2. **Token Rotation**: Implement token rotation for enhanced security
3. **Access Logging**: Log token access for audit purposes
4. **Network Security**: Use HTTPS for all API communications

### Performance Optimization

1. **Connection Pooling**: Configure appropriate connection pools
2. **Token Caching**: Implement token caching to reduce API calls
3. **Background Processing**: Use background tasks for token refresh
4. **Monitoring**: Implement comprehensive monitoring and alerting

### Deployment Configuration

```python
# Production configuration
config = create_config_with_prefixes(
    revo_prefix="PROD_",
    llm_prefix="PROD_LLM_",
    logging_prefix="PROD_LOG_",
    token_prefix="PROD_TOKEN_"
)

# Production token manager
token_manager = TokenManager(
    refresh_interval_minutes=45,  # Conservative refresh interval
    settings_instance=config
)
```

## Troubleshooting

### Common Issues

1. **Token Refresh Failures**: Check network connectivity and credentials
2. **Background Service Issues**: Verify custom settings are properly configured
3. **Authentication Errors**: Ensure all required environment variables are set
4. **Performance Issues**: Monitor token refresh frequency and adjust intervals

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Your token management code
token_manager = TokenManager(refresh_interval_minutes=45)
await token_manager.start_background_service()
```

### Testing Token Management

```python
import pytest
from unittest.mock import patch
from revos import TokenManager

@pytest.mark.asyncio
async def test_token_manager():
    """Test token manager functionality."""
    token_manager = TokenManager(refresh_interval_minutes=5)
    
    # Test background service
    await token_manager.start_background_service()
    assert token_manager.is_background_service_running()
    
    await token_manager.stop_background_service()
    assert not token_manager.is_background_service_running()
```

This guide provides comprehensive information about token management in the Revos library, from basic usage to advanced production scenarios.
