# Custom Prefixes

Learn how to use Revos with custom environment variable prefixes like `RUMBA_` instead of the default `REVOS_` prefix.

## Why Use Custom Prefixes?

Custom prefixes are useful when you want to:

- **🔧 Avoid Conflicts**: Prevent naming conflicts with other libraries
- **🏗️ Maintain Consistency**: Keep consistent naming conventions in your project
- **🌍 Support Multiple Environments**: Use different prefixes for different environments
- **🐳 Container Integration**: Easily integrate with Docker, Kubernetes, or other containerized environments
- **🔒 Security**: Use environment-specific configurations

## Basic Custom Prefix Example

### Using RUMBA_ Prefix

```python
from revos import create_config_with_prefixes

# Set environment variables with RUMBA_ prefix
import os
os.environ.update({
    "RUMBA_CLIENT_ID": "your_rumba_client_id",
    "RUMBA_CLIENT_SECRET": "your_rumba_client_secret",
    "RUMBA_TOKEN_URL": "https://your-site.com/revo/oauth/token",
    "RUMBA_BASE_URL": "https://your-site.com/revo/llm-api",
    "RUMBA_LLM_MODEL": "gpt-4",
    "RUMBA_LLM_TEMPERATURE": "0.1",
    "RUMBA_LLM_MAX_TOKENS": "1000"
})

# Create configuration with custom RUMBA_ prefix
config = create_config_with_prefixes(
    revo_prefix="RUMBA_",  # Use RUMBA_ prefix instead of REVOS_
    llm_prefix="RUMBA_LLM_",  # Use RUMBA_LLM_ prefix for LLM settings
    logging_prefix="RUMBA_LOG_",  # Use RUMBA_LOG_ prefix for logging
    token_prefix="RUMBA_TOKEN_"  # Use RUMBA_TOKEN_ prefix for token management
)

print(f"Client ID: {config.revos.client_id}")
print(f"LLM Model: {config.llm.model}")
print(f"Temperature: {config.llm.temperature}")
```

### Complete RUMBA_ Example

```python
#!/usr/bin/env python3
"""
Complete RUMBA_ Prefix Example
"""

import os
from revos import create_config_with_prefixes

def main():
    """Complete RUMBA_ prefix example."""
    print("🎵 RUMBA_ Prefix Example")
    
    # Set environment variables with RUMBA_ prefix
    os.environ.update({
        "RUMBA_CLIENT_ID": "your_rumba_client_id",
        "RUMBA_CLIENT_SECRET": "your_rumba_client_secret",
        "RUMBA_TOKEN_URL": "https://your-site.com/revo/oauth/token",
        "RUMBA_BASE_URL": "https://your-site.com/revo/llm-api",
        "RUMBA_LLM_MODEL": "gpt-4",
        "RUMBA_LLM_TEMPERATURE": "0.1",
        "RUMBA_LLM_MAX_TOKENS": "1000",
        "RUMBA_TOKEN_MANAGER_REFRESH_INTERVAL_MINUTES": "45",
        "RUMBA_LOGGING_LEVEL": "INFO"
    })
    
    # Create configuration with custom RUMBA_ prefix
    config = create_config_with_prefixes(
        revo_prefix="RUMBA_",  # Use RUMBA_ prefix instead of REVOS_
        llm_prefix="RUMBA_LLM_",  # Use RUMBA_LLM_ prefix for LLM settings
        logging_prefix="RUMBA_LOG_",  # Use RUMBA_LOG_ prefix for logging
        token_prefix="RUMBA_TOKEN_"  # Use RUMBA_TOKEN_ prefix for token management
    )
    
    print("✅ Configuration created with RUMBA_ prefix")
    print(f"📊 Client ID: {config.revos.client_id}")
    print(f"🔗 Token URL: {config.revos.token_url}")
    print(f"🌐 Base URL: {config.revos.base_url}")
    print(f"🤖 LLM Model: {config.llm.model}")
    print(f"🌡️  Temperature: {config.llm.temperature}")
    print(f"📝 Max Tokens: {config.llm.max_tokens}")
    print(f"🔄 Refresh Interval: {config.token_manager.refresh_interval_minutes} minutes")
    print(f"📝 Logging Level: {config.logging.level}")

if __name__ == "__main__":
    main()
```

## Environment-Specific Prefixes

### Development vs Production

```python
# Development environment with RUMBA_DEV_ prefix
dev_config = create_config_with_prefixes(
    revo_prefix="RUMBA_DEV_",  # Use RUMBA_DEV_ prefix for development
    llm_prefix="RUMBA_DEV_LLM_",
    logging_prefix="RUMBA_DEV_LOG_",
    token_prefix="RUMBA_DEV_TOKEN_"
)

# Production environment with RUMBA_PROD_ prefix
prod_config = create_config_with_prefixes(
    revo_prefix="RUMBA_PROD_",  # Use RUMBA_PROD_ prefix for production
    llm_prefix="RUMBA_PROD_LLM_",
    logging_prefix="RUMBA_PROD_LOG_",
    token_prefix="RUMBA_PROD_TOKEN_"
)

print(f"Development Client ID: {dev_config.revos.client_id}")
print(f"Production Client ID: {prod_config.revos.client_id}")
```

## Multiple Models with Custom Prefix

```python
# Set environment variables for multiple models
os.environ.update({
    "RUMBA_CLIENT_ID": "your_rumba_client_id",
    "RUMBA_CLIENT_SECRET": "your_rumba_client_secret",
    
    # Multiple LLM models with RUMBA_ prefix
    "RUMBA_LLM_MODELS_0_MODEL": "gpt-3.5-turbo",
    "RUMBA_LLM_MODELS_0_TEMPERATURE": "0.0",
    "RUMBA_LLM_MODELS_0_MAX_TOKENS": "500",
    "RUMBA_LLM_MODELS_0_DESCRIPTION": "Fast model for simple tasks",
    
    "RUMBA_LLM_MODELS_1_MODEL": "gpt-4",
    "RUMBA_LLM_MODELS_1_TEMPERATURE": "0.0",
    "RUMBA_LLM_MODELS_1_MAX_TOKENS": "2000",
    "RUMBA_LLM_MODELS_1_DESCRIPTION": "Accurate model for complex tasks"
})

# Create configuration with multiple models
config = create_config_with_prefixes(
    revo_prefix="RUMBA_",  # Use RUMBA_ prefix
    llm_prefix="RUMBA_LLM_",  # Use RUMBA_LLM_ prefix for LLM settings
    logging_prefix="RUMBA_LOG_",  # Use RUMBA_LOG_ prefix for logging
    token_prefix="RUMBA_TOKEN_"  # Use RUMBA_TOKEN_ prefix for token management
)

# Use the models
from revos import LangChainExtractor

fast_extractor = LangChainExtractor(
    model_name="fast",
    settings_instance=config
)

accurate_extractor = LangChainExtractor(
    model_name="accurate", 
    settings_instance=config
)
```

## Docker Integration

### Docker Compose Example

```yaml
# docker-compose.yml
version: '3.8'
services:
  rumba-app:
    image: your-app:latest
    environment:
      - RUMBA_CLIENT_ID=your_rumba_client_id
      - RUMBA_CLIENT_SECRET=your_rumba_client_secret
      - RUMBA_TOKEN_URL=https://your-site.com/revo/oauth/token
      - RUMBA_BASE_URL=https://your-site.com/revo/llm-api
      - RUMBA_LLM_MODEL=gpt-4
      - RUMBA_LLM_TEMPERATURE=0.0
      - RUMBA_LLM_MAX_TOKENS=1500
      - RUMBA_TOKEN_MANAGER_REFRESH_INTERVAL_MINUTES=30
      - RUMBA_LOGGING_LEVEL=INFO
    ports:
      - "8000:8000"
```

### Dockerfile Example

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Set default RUMBA_ environment variables
ENV RUMBA_LLM_MODEL=gpt-4
ENV RUMBA_LLM_TEMPERATURE=0.0
ENV RUMBA_LOGGING_LEVEL=INFO

CMD ["python", "app.py"]
```

## Kubernetes Integration

### ConfigMap Example

```yaml
# rumba-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: rumba-config
  namespace: default
data:
  RUMBA_CLIENT_ID: "your_rumba_client_id"
  RUMBA_CLIENT_SECRET: "your_rumba_client_secret"
  RUMBA_TOKEN_URL: "https://your-site.com/revo/oauth/token"
  RUMBA_BASE_URL: "https://your-site.com/revo/llm-api"
  RUMBA_LLM_MODEL: "gpt-4"
  RUMBA_LLM_TEMPERATURE: "0.0"
  RUMBA_LLM_MAX_TOKENS: "2000"
  RUMBA_TOKEN_MANAGER_REFRESH_INTERVAL_MINUTES: "45"
  RUMBA_LOGGING_LEVEL: "INFO"
```

### Deployment Example

```yaml
# rumba-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rumba-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rumba-app
  template:
    metadata:
      labels:
        app: rumba-app
    spec:
      containers:
      - name: rumba-app
        image: your-app:latest
        envFrom:
        - configMapRef:
            name: rumba-config
        ports:
        - containerPort: 8000
```

## FastAPI Integration with Custom Prefix

```python
from fastapi import FastAPI
from revos import create_config_with_prefixes, LangChainExtractor
from contextlib import asynccontextmanager

# Create configuration with RUMBA_ prefix
config = create_config_with_prefixes(
    revo_prefix="RUMBA_",  # Use RUMBA_ prefix instead of REVOS_
    llm_prefix="RUMBA_LLM_",  # Use RUMBA_LLM_ prefix for LLM settings
    logging_prefix="RUMBA_LOG_",  # Use RUMBA_LOG_ prefix for logging
    token_prefix="RUMBA_TOKEN_"  # Use RUMBA_TOKEN_ prefix for token management
)

# Global extractor instance
extractor: LangChainExtractor = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the RUMBA extractor on startup."""
    global extractor
    try:
        extractor = LangChainExtractor(
            model_name="gpt-4",
            settings_instance=config
        )
        print("✅ RUMBA extractor initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize RUMBA extractor: {e}")
        raise
    
    yield
    
    print("🔄 RUMBA extractor cleanup completed")

app = FastAPI(title="RUMBA FastAPI Integration", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "RUMBA FastAPI Integration"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    if extractor is None:
        return {"status": "unhealthy", "rumba_connected": False}
    
    return {
        "status": "healthy",
        "rumba_connected": True,
        "model": extractor.get_current_model()
    }
```

## Environment Variable Mapping

### Complete RUMBA_ Prefix Mapping

| Default Prefix | RUMBA_ Prefix | Description |
|----------------|---------------|-------------|
| `REVOS_CLIENT_ID` | `RUMBA_CLIENT_ID` | Client ID for authentication |
| `REVOS_CLIENT_SECRET` | `RUMBA_CLIENT_SECRET` | Client secret for authentication |
| `REVOS_TOKEN_URL` | `RUMBA_TOKEN_URL` | OAuth token endpoint |
| `REVOS_BASE_URL` | `RUMBA_BASE_URL` | Base URL for API calls |
| `REVOS_TOKEN_BUFFER_MINUTES` | `RUMBA_TOKEN_BUFFER_MINUTES` | Token buffer time |
| `REVOS_MAX_RETRIES` | `RUMBA_MAX_RETRIES` | Maximum retry attempts |
| `REVOS_REQUEST_TIMEOUT` | `RUMBA_REQUEST_TIMEOUT` | Request timeout in seconds |
| `LLM_MODEL` | `RUMBA_LLM_MODEL` | Default LLM model |
| `LLM_TEMPERATURE` | `RUMBA_LLM_TEMPERATURE` | LLM temperature setting |
| `LLM_MAX_TOKENS` | `RUMBA_LLM_MAX_TOKENS` | Maximum tokens per request |
| `LLM_TOP_P` | `RUMBA_LLM_TOP_P` | Top-p sampling parameter |
| `LLM_FREQUENCY_PENALTY` | `RUMBA_LLM_FREQUENCY_PENALTY` | Frequency penalty |
| `LLM_PRESENCE_PENALTY` | `RUMBA_LLM_PRESENCE_PENALTY` | Presence penalty |
| `TOKEN_MANAGER_REFRESH_INTERVAL_MINUTES` | `RUMBA_TOKEN_MANAGER_REFRESH_INTERVAL_MINUTES` | Token refresh interval |
| `TOKEN_MANAGER_MAX_FAILURES_BEFORE_FALLBACK` | `RUMBA_TOKEN_MANAGER_MAX_FAILURES_BEFORE_FALLBACK` | Max failures before fallback |
| `TOKEN_MANAGER_ENABLE_PERIODIC_REFRESH` | `RUMBA_TOKEN_MANAGER_ENABLE_PERIODIC_REFRESH` | Enable periodic refresh |
| `TOKEN_MANAGER_ENABLE_FALLBACK` | `RUMBA_TOKEN_MANAGER_ENABLE_FALLBACK` | Enable fallback authentication |
| `LOGGING_LEVEL` | `RUMBA_LOGGING_LEVEL` | Logging level |
| `LOGGING_FORMAT` | `RUMBA_LOGGING_FORMAT` | Logging format string |

## Best Practices

### 1. Choose Meaningful Prefixes

```python
# Good: Meaningful and descriptive
MYAPP_CLIENT_ID = "myapp_client_id"
COMPANY_REVOS_CLIENT_ID = "company_revos_client_id"

# Avoid: Too generic or confusing
X_CLIENT_ID = "x_client_id"
ABC_CLIENT_ID = "abc_client_id"
```

### 2. Use Environment-Specific Prefixes

```python
# Development
DEV_RUMBA_CLIENT_ID = "dev_client_id"

# Staging
STAGING_RUMBA_CLIENT_ID = "staging_client_id"

# Production
PROD_RUMBA_CLIENT_ID = "prod_client_id"
```

### 3. Document Your Prefixes

```python
# Document the prefix choice and reasoning
"""
RUMBA_ prefix is used to:
- Avoid conflicts with other Revos instances
- Maintain consistency with our RUMBA project naming
- Support multiple environments (DEV_RUMBA_, PROD_RUMBA_)
"""
```

### 4. Use Configuration Files for Complex Setups

```yaml
# config/rumba.yaml
rumba:
  client_id: "your_rumba_client_id"
  client_secret: "your_rumba_client_secret"
  token_url: "https://your-site.com/revo/oauth/token"
  base_url: "https://your-site.com/revo/llm-api"

rumba_llm:
  model: "gpt-4"
  temperature: 0.1
  max_tokens: 1000

rumba_token_manager:
  refresh_interval_minutes: 45
  max_failures_before_fallback: 3
```

## Troubleshooting

### Common Issues

#### 1. Environment Variables Not Found

```python
# Check if environment variables are set
import os
print(f"RUMBA_CLIENT_ID: {os.getenv('RUMBA_CLIENT_ID')}")
print(f"RUMBA_CLIENT_SECRET: {'*' * len(os.getenv('RUMBA_CLIENT_SECRET', ''))}")
```

#### 2. Configuration Not Loading

```python
# Verify configuration creation
try:
    config = create_config_with_prefixes(
        revos={
            "client_id": "your_rumba_client_id",
            "client_secret": "your_rumba_client_secret"
        }
    )
    print("✅ Configuration created successfully")
except Exception as e:
    print(f"❌ Configuration error: {e}")
```

#### 3. Extractor Initialization Fails

```python
# Check extractor initialization
try:
    extractor = LangChainExtractor(
        model_name="gpt-4",
        settings_instance=config
    )
    print("✅ Extractor initialized successfully")
except Exception as e:
    print(f"❌ Extractor initialization failed: {e}")
```

## Complete Examples

See the complete examples for comprehensive demonstrations of using RUMBA_ prefixes:

- [`examples/simple_rumba_example.py`](../../examples/simple_rumba_example.py) - Simple RUMBA_ prefix example
- [`examples/custom_rumba_prefix.py`](../../examples/custom_rumba_prefix.py) - Comprehensive RUMBA_ prefix examples
- [`examples/custom_prefixes.py`](../../examples/custom_prefixes.py) - Multiple custom prefix examples including RUMBA_

## Next Steps

Now that you understand custom prefixes:

1. [:octicons-arrow-right-24: **Multiple Models**](multiple-models.md) – Learn about multiple LLM model configurations
2. [:octicons-arrow-right-24: **FastAPI Integration**](../fastapi/basic-setup.md) – Build web applications with custom prefixes
3. [:octicons-arrow-right-24: **Configuration Guide**](../getting-started/configuration.md) – Explore advanced configuration options
