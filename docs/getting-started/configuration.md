# Configuration

Learn how to configure Revos for your specific needs using various configuration methods.

## Configuration Methods

Revos supports multiple configuration methods, allowing you to choose the approach that best fits your project:

1. **Environment Variables** (Recommended for deployment)
2. **Configuration Files** (YAML, JSON)
3. **Programmatic Configuration** (Python code)
4. **Custom Prefixes** (For multiple environments)

## Environment Variables

### Required Variables

```bash
# Required Revos credentials
export REVOS_CLIENT_ID="your_client_id"
export REVOS_CLIENT_SECRET="your_client_secret"
```

### Optional Variables

```bash
# Revos API endpoints
export REVOS_TOKEN_URL="https://your-site.com/revo/oauth/token"
export REVOS_BASE_URL="https://your-site.com/revo/llm-api"

# Token management
export REVOS_TOKEN_BUFFER_MINUTES="5"
export REVOS_MAX_RETRIES="3"
export REVOS_REQUEST_TIMEOUT="30"

# LLM configuration
export LLM_MODEL="gpt-4"
export LLM_TEMPERATURE="0.1"
export LLM_MAX_TOKENS="1000"
export LLM_TOP_P="1.0"
export LLM_FREQUENCY_PENALTY="0.0"
export LLM_PRESENCE_PENALTY="0.0"

# Token manager settings
export TOKEN_MANAGER_REFRESH_INTERVAL_MINUTES="45"
export TOKEN_MANAGER_MAX_FAILURES_BEFORE_FALLBACK="3"
export TOKEN_MANAGER_ENABLE_PERIODIC_REFRESH="true"
export TOKEN_MANAGER_ENABLE_FALLBACK="true"

# Logging configuration
export LOGGING_LEVEL="INFO"
export LOGGING_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

## Configuration Files

### YAML Configuration

Create a `config.yaml` file:

```yaml
revos:
  client_id: "your_client_id"
  client_secret: "your_client_secret"
  token_url: "https://your-site.com/revo/oauth/token"
  base_url: "https://your-site.com/revo/llm-api"
  token_buffer_minutes: 5
  max_retries: 3
  request_timeout: 30

llm:
  model: "gpt-4"
  temperature: 0.1
  max_tokens: 1000
  top_p: 1.0
  frequency_penalty: 0.0
  presence_penalty: 0.0

llm_models:
  models:
    fast:
      model: "gpt-3.5-turbo"
      temperature: 0.0
      max_tokens: 500
      description: "Fast model for simple tasks"
    
    accurate:
      model: "gpt-4"
      temperature: 0.0
      max_tokens: 2000
      description: "Accurate model for complex tasks"
    
    creative:
      model: "gpt-4"
      temperature: 0.8
      max_tokens: 1500
      description: "Creative model for brainstorming"

token_manager:
  refresh_interval_minutes: 45
  max_failures_before_fallback: 3
  enable_periodic_refresh: true
  enable_fallback: true

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

Load the configuration:

```python
from revos import load_config_from_file, RevosMainConfig

# Load from YAML file
config = load_config_from_file("config.yaml")
print(f"Model: {config.llm.model}")
```

### JSON Configuration

Create a `config.json` file:

```json
{
  "revos": {
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "token_url": "https://your-site.com/revo/oauth/token",
    "base_url": "https://your-site.com/revo/llm-api",
    "token_buffer_minutes": 5,
    "max_retries": 3,
    "request_timeout": 30
  },
  "llm": {
    "model": "gpt-4",
    "temperature": 0.1,
    "max_tokens": 1000,
    "top_p": 1.0,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0
  },
  "token_manager": {
    "refresh_interval_minutes": 45,
    "max_failures_before_fallback": 3,
    "enable_periodic_refresh": true,
    "enable_fallback": true
  },
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  }
}
```

## Programmatic Configuration

### Basic Configuration

```python
from revos import RevosMainConfig, RevosConfig, LLMConfig, TokenManagerConfig

# Create configuration programmatically
config = RevosMainConfig(
    revos=RevosConfig(
        client_id="your_client_id",
        client_secret="your_client_secret",
        token_url="https://your-site.com/revo/oauth/token",
        base_url="https://your-site.com/revo/llm-api"
    ),
    llm=LLMConfig(
        model="gpt-4",
        temperature=0.1,
        max_tokens=1000
    ),
    token_manager=TokenManagerConfig(
        refresh_interval_minutes=45,
        max_failures_before_fallback=3
    )
)

# Use the configuration
from revos import LangChainExtractor
extractor = LangChainExtractor(model_name="gpt-4", settings_instance=config)
```

### Multiple Models Configuration

```python
from revos import RevosMainConfig, LLMModelConfig, LLMModelsConfig

config = RevosMainConfig(
    llm_models=LLMModelsConfig(
        models={
            "fast": LLMModelConfig(
                model="gpt-3.5-turbo",
                temperature=0.0,
                max_tokens=500,
                description="Fast model for simple tasks"
            ),
            "accurate": LLMModelConfig(
                model="gpt-4",
                temperature=0.0,
                max_tokens=2000,
                description="Accurate model for complex tasks"
            ),
            "creative": LLMModelConfig(
                model="gpt-4",
                temperature=0.8,
                max_tokens=1500,
                description="Creative model for brainstorming"
            )
        }
    )
)
```

## Custom Environment Variable Prefixes

Use custom prefixes for different environments:

```python
from revos import create_config_with_prefixes

# Development environment
dev_config = create_config_with_prefixes(
    revos={
        "client_id": "dev_client_id",
        "client_secret": "dev_client_secret"
    },
    llm={
        "model": "gpt-3.5-turbo",
        "temperature": 0.1
    }
)

# Production environment
prod_config = create_config_with_prefixes(
    revos={
        "client_id": "prod_client_id", 
        "client_secret": "prod_client_secret"
    },
    llm={
        "model": "gpt-4",
        "temperature": 0.0
    }
)
```

## Environment-Specific Configuration

### Development Environment

```bash
# .env.development
REVOS_CLIENT_ID=dev_client_id
REVOS_CLIENT_SECRET=dev_client_secret
REVOS_TOKEN_URL=https://dev-api.example.com/oauth/token
LLM_MODEL=gpt-3.5-turbo
LLM_TEMPERATURE=0.1
LOGGING_LEVEL=DEBUG
```

### Production Environment

```bash
# .env.production
REVOS_CLIENT_ID=prod_client_id
REVOS_CLIENT_SECRET=prod_client_secret
REVOS_TOKEN_URL=https://api.example.com/oauth/token
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.0
LOGGING_LEVEL=INFO
```

### Testing Environment

```bash
# .env.testing
REVOS_CLIENT_ID=test_client_id
REVOS_CLIENT_SECRET=test_client_secret
REVOS_TOKEN_URL=https://test-api.example.com/oauth/token
LLM_MODEL=gpt-3.5-turbo
LLM_TEMPERATURE=0.0
LOGGING_LEVEL=WARNING
```

## Configuration Validation

Revos automatically validates your configuration:

```python
from revos import RevosMainConfig

try:
    config = RevosMainConfig(
        revos=RevosConfig(
            client_id="invalid",  # This will be validated
            client_secret=""
        )
    )
except ValidationError as e:
    print(f"Configuration error: {e}")
```

## Configuration Best Practices

### 1. Use Environment Variables for Secrets

```python
import os
from revos import RevosMainConfig

# Never hardcode secrets in code
config = RevosMainConfig(
    revos=RevosConfig(
        client_id=os.getenv("REVOS_CLIENT_ID"),
        client_secret=os.getenv("REVOS_CLIENT_SECRET")
    )
)
```

### 2. Use Configuration Files for Complex Settings

```python
# For complex configurations, use YAML/JSON files
config = load_config_from_file("config/production.yaml")
```

### 3. Validate Configuration Early

```python
from revos import get_settings

# Validate configuration on startup
try:
    settings = get_settings()
    print("✅ Configuration is valid")
except Exception as e:
    print(f"❌ Configuration error: {e}")
    exit(1)
```

### 4. Use Different Configurations for Different Environments

```python
import os

# Load environment-specific configuration
env = os.getenv("ENVIRONMENT", "development")
config_file = f"config/{env}.yaml"
config = load_config_from_file(config_file)
```

## Configuration Examples

### Minimal Configuration

```python
from revos import RevosMainConfig

# Minimal configuration with defaults
config = RevosMainConfig(
    revos=RevosConfig(
        client_id="your_client_id",
        client_secret="your_client_secret"
    )
)
```

### Full Configuration

```python
from revos import RevosMainConfig, RevosConfig, LLMConfig, LLMModelsConfig, LLMModelConfig, TokenManagerConfig, LoggingConfig

config = RevosMainConfig(
    revos=RevosConfig(
        client_id="your_client_id",
        client_secret="your_client_secret",
        token_url="https://your-site.com/revo/oauth/token",
        base_url="https://your-site.com/revo/llm-api",
        token_buffer_minutes=5,
        max_retries=3,
        request_timeout=30
    ),
    llm=LLMConfig(
        model="gpt-4",
        temperature=0.1,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    ),
    llm_models=LLMModelsConfig(
        models={
            "fast": LLMModelConfig(
                model="gpt-3.5-turbo",
                temperature=0.0,
                max_tokens=500
            ),
            "accurate": LLMModelConfig(
                model="gpt-4",
                temperature=0.0,
                max_tokens=2000
            )
        }
    ),
    token_manager=TokenManagerConfig(
        refresh_interval_minutes=45,
        max_failures_before_fallback=3,
        enable_periodic_refresh=True,
        enable_fallback=True
    ),
    logging=LoggingConfig(
        level="INFO",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
)
```

## Next Steps

Now that you understand configuration:

1. [:octicons-arrow-right-24: **Quick Start**](quick-start.md) – Run your first example
2. [:octicons-arrow-right-24: **Authentication**](../user-guide/authentication.md) – Learn about authentication
3. [:octicons-arrow-right-24: **Multiple Models**](../user-guide/multiple-models.md) – Configure multiple LLM models
