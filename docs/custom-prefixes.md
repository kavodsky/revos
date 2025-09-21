# Custom Environment Variable Prefixes

This guide explains how to use custom environment variable prefixes to avoid conflicts with other applications.

## Overview

The Revos library supports custom environment variable prefixes, allowing you to:

- Avoid conflicts with other applications using the same environment variables
- Use organization-specific naming conventions
- Support multiple Revos instances in the same environment
- Maintain clean separation between different applications

## Basic Usage

### Creating Custom Configuration

```python
from revos import create_config_with_prefixes

# Create configuration with custom prefixes
config = create_config_with_prefixes(
    revo_prefix="MYAPP_",
    llm_prefix="MYAPP_LLM_",
    logging_prefix="MYAPP_LOG_",
    token_prefix="MYAPP_TOKEN_"
)
```

### Using Custom Configuration

```python
from revos import TokenManager, get_langchain_extractor

# Use with custom settings
token_manager = TokenManager(settings_instance=config)
extractor = get_langchain_extractor("gpt-4", settings_instance=config)
```

## Environment Variable Mapping

### Default Prefixes

| Component | Default Prefix | Example Variables |
|-----------|----------------|-------------------|
| Revos API | `REVOS_` | `REVOS_CLIENT_ID`, `REVOS_CLIENT_SECRET` |
| LLM Models | `LLM_MODELS_` | `LLM_MODELS_GPT_4_MODEL` |
| Logging | `LOG_` | `LOG_LEVEL`, `LOG_FORMAT` |
| Token Management | `TOKEN_` | `TOKEN_REFRESH_INTERVAL_MINUTES` |

### Custom Prefixes

| Component | Custom Prefix | Example Variables |
|-----------|---------------|-------------------|
| Revos API | `MYAPP_` | `MYAPP_CLIENT_ID`, `MYAPP_CLIENT_SECRET` |
| LLM Models | `MYAPP_LLM_` | `MYAPP_LLM_GPT_4_MODEL` |
| Logging | `MYAPP_LOG_` | `MYAPP_LOG_LEVEL`, `MYAPP_LOG_FORMAT` |
| Token Management | `MYAPP_TOKEN_` | `MYAPP_TOKEN_REFRESH_INTERVAL_MINUTES` |

## Complete Example

### Environment Variables

```bash
# MYAPP_ prefix configuration
MYAPP_CLIENT_ID=your_client_id
MYAPP_CLIENT_SECRET=your_client_secret
MYAPP_TOKEN_URL=https://api.revos.com/token
MYAPP_BASE_URL=https://api.revos.com
MYAPP_TOKEN_BUFFER_MINUTES=5
MYAPP_TOKEN_REFRESH_INTERVAL_MINUTES=45

# MYAPP_LLM_ prefix configuration
MYAPP_LLM_MODELS_GPT_4_MODEL=gpt-4
MYAPP_LLM_MODELS_GPT_4_TEMPERATURE=0.1
MYAPP_LLM_MODELS_GPT_4_MAX_TOKENS=2000

MYAPP_LLM_MODELS_CLAUDE_4_SONNET_MODEL=claude-4-sonnet
MYAPP_LLM_MODELS_CLAUDE_4_SONNET_TEMPERATURE=0.3
MYAPP_LLM_MODELS_CLAUDE_4_SONNET_MAX_TOKENS=4000

# MYAPP_LOG_ prefix configuration
MYAPP_LOG_LEVEL=INFO
MYAPP_LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# MYAPP_TOKEN_ prefix configuration
MYAPP_TOKEN_REFRESH_INTERVAL_MINUTES=45
MYAPP_TOKEN_MAX_FAILURES_BEFORE_FALLBACK=1
MYAPP_TOKEN_ENABLE_PERIODIC_REFRESH=true
MYAPP_TOKEN_ENABLE_FALLBACK=true
```

### Python Code

```python
from revos import create_config_with_prefixes, TokenManager, get_langchain_extractor
import asyncio

async def main():
    # Create custom configuration
    config = create_config_with_prefixes(
        revo_prefix="MYAPP_",
        llm_prefix="MYAPP_LLM_",
        logging_prefix="MYAPP_LOG_",
        token_prefix="MYAPP_TOKEN_"
    )
    
    # Initialize token manager with custom settings
    token_manager = TokenManager(
        refresh_interval_minutes=45,
        settings_instance=config
    )
    
    # Start background token refresh service
    await token_manager.start_background_service()
    
    # Initialize extractor with custom settings
    extractor = get_langchain_extractor(
        model_name="gpt-4",
        settings_instance=config
    )
    
    # Use the extractor
    result = extractor.extract(
        text="John Doe is 30 years old and works as a software engineer.",
        schema=PersonInfo
    )
    
    print(f"Extracted data: {result}")
    
    # Stop background service
    await token_manager.stop_background_service()

if __name__ == "__main__":
    asyncio.run(main())
```

## FastAPI Integration

### Custom Prefix FastAPI Application

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
from revos import create_config_with_prefixes, TokenManager, get_langchain_extractor

# Global instances
config = None
token_manager = None
extractor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global config, token_manager, extractor
    
    # Startup
    try:
        # Create custom configuration
        config = create_config_with_prefixes(
            revo_prefix="MYAPP_",
            llm_prefix="MYAPP_LLM_",
            logging_prefix="MYAPP_LOG_",
            token_prefix="MYAPP_TOKEN_"
        )
        
        # Initialize token manager
        token_manager = TokenManager(
            refresh_interval_minutes=45,
            settings_instance=config
        )
        
        # Start background service
        await token_manager.start_background_service()
        
        # Initialize extractor
        extractor = get_langchain_extractor(
            model_name="gpt-4",
            settings_instance=config
        )
        
        print("✅ MYAPP FastAPI services started successfully")
        
    except Exception as e:
        print(f"❌ Failed to start MYAPP FastAPI services: {e}")
        raise
    
    yield
    
    # Shutdown
    if token_manager:
        await token_manager.stop_background_service()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "MYAPP FastAPI application is running"}

@app.post("/extract")
async def extract_data(text: str):
    """Extract structured data using custom configuration."""
    try:
        result = extractor.extract(text, schema=PersonInfo)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
```

## Multiple Applications

### Running Multiple Revos Instances

You can run multiple Revos applications with different prefixes in the same environment:

```bash
# Application 1 - RUMBA_
RUMBA_CLIENT_ID=client1
RUMBA_CLIENT_SECRET=secret1
RUMBA_TOKEN_URL=https://api1.revos.com/token

# Application 2 - MYAPP_
MYAPP_CLIENT_ID=client2
MYAPP_CLIENT_SECRET=secret2
MYAPP_TOKEN_URL=https://api2.revos.com/token

# Application 3 - PROD_
PROD_CLIENT_ID=client3
PROD_CLIENT_SECRET=secret3
PROD_TOKEN_URL=https://api3.revos.com/token
```

### Python Code for Multiple Applications

```python
# Application 1
rumba_config = create_config_with_prefixes(
    revo_prefix="RUMBA_",
    llm_prefix="RUMBA_LLM_",
    logging_prefix="RUMBA_LOG_",
    token_prefix="RUMBA_TOKEN_"
)

# Application 2
myapp_config = create_config_with_prefixes(
    revo_prefix="MYAPP_",
    llm_prefix="MYAPP_LLM_",
    logging_prefix="MYAPP_LOG_",
    token_prefix="MYAPP_TOKEN_"
)

# Application 3
prod_config = create_config_with_prefixes(
    revo_prefix="PROD_",
    llm_prefix="PROD_LLM_",
    logging_prefix="PROD_LOG_",
    token_prefix="PROD_TOKEN_"
)
```

## Best Practices

### Naming Conventions

1. **Use descriptive prefixes**: Choose prefixes that clearly identify your application
2. **Be consistent**: Use the same prefix pattern across all components
3. **Avoid conflicts**: Ensure prefixes don't conflict with other applications
4. **Document your prefixes**: Keep a record of which prefixes your application uses

### Environment Management

1. **Separate environments**: Use different prefixes for dev/staging/production
2. **Environment files**: Create separate `.env` files for different environments
3. **Validation**: Validate that all required environment variables are set
4. **Documentation**: Document the required environment variables for your application

### Example Environment Files

#### Development (.env.dev)
```bash
DEV_CLIENT_ID=dev_client_id
DEV_CLIENT_SECRET=dev_client_secret
DEV_TOKEN_URL=https://dev-api.revos.com/token
```

#### Staging (.env.staging)
```bash
STAGING_CLIENT_ID=staging_client_id
STAGING_CLIENT_SECRET=staging_client_secret
STAGING_TOKEN_URL=https://staging-api.revos.com/token
```

#### Production (.env.prod)
```bash
PROD_CLIENT_ID=prod_client_id
PROD_CLIENT_SECRET=prod_client_secret
PROD_TOKEN_URL=https://api.revos.com/token
```

## Troubleshooting

### Common Issues

1. **Missing environment variables**: Ensure all required variables are set with the correct prefix
2. **Prefix conflicts**: Verify that your prefixes don't conflict with other applications
3. **Configuration not loaded**: Check that the custom configuration is passed to all components

### Debugging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your code with custom configuration
config = create_config_with_prefixes(
    revo_prefix="MYAPP_",
    llm_prefix="MYAPP_LLM_",
    logging_prefix="MYAPP_LOG_",
    token_prefix="MYAPP_TOKEN_"
)

# Check configuration values
print(f"Client ID: {config.revos.client_id}")
print(f"Token URL: {config.revos.token_url}")
print(f"LLM Models: {config.llm_models.models}")
```

This guide provides comprehensive information about using custom environment variable prefixes with the Revos library.
