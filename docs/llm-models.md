# LLM Models Configuration

This guide explains how to configure multiple LLM models using environment variables with the `LLM_MODELS_` prefix.

## Overview

The Revos library supports configuring multiple LLM models through environment variables, allowing you to:

- Configure different models with different settings
- Use custom prefixes to avoid conflicts
- Override default models with your own configurations
- Support different environments with different model sets

## Basic Configuration

### Environment Variables Format

LLM model configurations use the `LLM_MODELS_` prefix followed by the model name and parameter:

```bash
LLM_MODELS_<MODEL_NAME>_<PARAMETER>=<VALUE>
```

### Example Configuration

```bash
# GPT-4 Configuration
LLM_MODELS_GPT_4_MODEL=gpt-4
LLM_MODELS_GPT_4_TEMPERATURE=0.1
LLM_MODELS_GPT_4_MAX_TOKENS=2000
LLM_MODELS_GPT_4_TOP_P=1.0
LLM_MODELS_GPT_4_FREQUENCY_PENALTY=0.0
LLM_MODELS_GPT_4_PRESENCE_PENALTY=0.0
LLM_MODELS_GPT_4_DESCRIPTION="Most capable model for complex tasks"

# Claude 4 Sonnet Configuration
LLM_MODELS_CLAUDE_4_SONNET_MODEL=claude-4-sonnet
LLM_MODELS_CLAUDE_4_SONNET_TEMPERATURE=0.3
LLM_MODELS_CLAUDE_4_SONNET_MAX_TOKENS=4000
LLM_MODELS_CLAUDE_4_SONNET_TOP_P=0.95
LLM_MODELS_CLAUDE_4_SONNET_DESCRIPTION="Anthropic's Claude 4 Sonnet model"

# GPT-3.5 Turbo Configuration
LLM_MODELS_GPT_3_5_TURBO_MODEL=gpt-3.5-turbo
LLM_MODELS_GPT_3_5_TURBO_TEMPERATURE=0.1
LLM_MODELS_GPT_3_5_TURBO_MAX_TOKENS=1000
LLM_MODELS_GPT_3_5_TURBO_DESCRIPTION="Fast and cost-effective model for general tasks"
```

## Supported Parameters

| Parameter | Description | Type | Default |
|-----------|-------------|------|---------|
| `MODEL` | The model identifier | string | Required |
| `TEMPERATURE` | Sampling temperature (0.0 to 2.0) | float | 0.1 |
| `MAX_TOKENS` | Maximum tokens to generate | integer | 1000 |
| `TOP_P` | Nucleus sampling parameter | float | 1.0 |
| `FREQUENCY_PENALTY` | Frequency penalty (-2.0 to 2.0) | float | 0.0 |
| `PRESENCE_PENALTY` | Presence penalty (-2.0 to 2.0) | float | 0.0 |
| `DESCRIPTION` | Human-readable description | string | "" |

## Usage Examples

### Basic Model Usage

```python
from revos import get_langchain_extractor

# Use GPT-4
extractor = get_langchain_extractor("gpt-4")

# Use Claude 4 Sonnet
extractor = get_langchain_extractor("claude-4-sonnet")

# Use GPT-3.5 Turbo
extractor = get_langchain_extractor("gpt-3.5-turbo")
```

### Working with Multiple Models

```python
from revos import get_langchain_extractor

# Create extractors for different models
gpt4_extractor = get_langchain_extractor("gpt-4")
claude_extractor = get_langchain_extractor("claude-4-sonnet")
gpt35_extractor = get_langchain_extractor("gpt-3.5-turbo")

# Use different models for different tasks
complex_task_result = gpt4_extractor.extract(text, schema)
simple_task_result = gpt35_extractor.extract(text, schema)
creative_task_result = claude_extractor.extract(text, schema)
```

### Custom Model Configuration

```python
from revos import create_config_with_prefixes, get_langchain_extractor

# Create custom configuration with different prefix
config = create_config_with_prefixes(
    llm_prefix="MYAPP_LLM_"
)

# Use with custom settings
extractor = get_langchain_extractor("gpt-4", settings_instance=config)
```

## Advanced Configuration

### Custom Model Parameters

You can add custom parameters to your models:

```bash
# Custom parameters
LLM_MODELS_GPT_4_CUSTOM_PARAM_1=value1
LLM_MODELS_GPT_4_CUSTOM_PARAM_2=value2
```

### Environment-Specific Configurations

```bash
# Development environment
LLM_MODELS_GPT_4_MODEL=gpt-4
LLM_MODELS_GPT_4_TEMPERATURE=0.7

# Production environment
LLM_MODELS_GPT_4_MODEL=gpt-4
LLM_MODELS_GPT_4_TEMPERATURE=0.1
```

## Troubleshooting

### Common Issues

1. **Model not found**: Ensure the model name matches exactly in your environment variables
2. **Invalid parameters**: Check that parameter values are within valid ranges
3. **Missing required parameters**: Ensure `MODEL` parameter is set for each model

### Debugging

Enable debug logging to see model configurations:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Your code here
```

## Best Practices

1. **Use descriptive model names**: Choose clear, consistent naming for your models
2. **Set appropriate defaults**: Configure sensible defaults for your use case
3. **Document your models**: Use the `DESCRIPTION` parameter to document model purposes
4. **Test configurations**: Verify your configurations work in your environment
5. **Use environment-specific configs**: Different settings for dev/staging/production
