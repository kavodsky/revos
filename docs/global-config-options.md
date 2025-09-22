# Global Config Options and Key Benefits

This document describes the different configuration options available for TokenManager and extractors, along with their key benefits and use cases.

## Overview

The Revos library supports multiple configuration approaches to handle different deployment scenarios. The global config approach provides automatic configuration sharing between TokenManager and extractors, while maintaining backward compatibility for standalone usage.

## Configuration Options

### 1. TokenManager with Global Config (Recommended)

**Use Case**: Production applications with automatic token management

```python
from revos.config.factory import create_config_with_prefixes
from revos.tokens.manager import TokenManager
from revos.llm.tools import get_langchain_extractor

# Create custom configuration
rumba_config = create_config_with_prefixes(
    revo_prefix="RUMBA_",
    llm_prefix="RUMBA_LLM_",
    logging_prefix="RUMBA_LOG_",
    token_prefix="RUMBA_TOKEN_"
)

# Initialize TokenManager with custom settings
token_manager = TokenManager(settings_instance=rumba_config)

# Extractors automatically use the same configuration
extractor = get_langchain_extractor("gpt-4")
# ✅ Uses RUMBA config automatically
# ✅ Gets automatic token refresh notifications
```

**Key Benefits**:
- ✅ **Zero Duplicate Requests**: Extractors never make their own token requests
- ✅ **Immediate Token Provision**: Extractors get tokens instantly upon registration
- ✅ **Automatic Configuration Sharing**: All extractors use the same config as TokenManager
- ✅ **Automatic Token Updates**: Extractors receive token refresh notifications automatically
- ✅ **Consistent Settings**: No configuration drift between components
- ✅ **Background Refresh**: Periodic token refresh without manual intervention
- ✅ **Observer Pattern**: Real-time updates when tokens are refreshed

### 2. Standalone Extractors with Custom Settings

**Use Case**: Simple scripts or applications without background token management

```python
from revos.config.factory import create_config_with_prefixes
from revos.llm.tools import get_langchain_extractor

# Create custom configuration
custom_config = create_config_with_prefixes(
    revo_prefix="CUSTOM_",
    llm_prefix="CUSTOM_LLM_",
    logging_prefix="CUSTOM_LOG_",
    token_prefix="CUSTOM_TOKEN_"
)

# Pass custom settings explicitly
extractor = get_langchain_extractor("gpt-4", settings_instance=custom_config)
# ✅ Uses CUSTOM config
# ❌ No automatic token updates
```

**Key Benefits**:
- ✅ **Custom Configuration**: Use any prefix or settings you want
- ✅ **Simple Setup**: No need for TokenManager
- ✅ **Lightweight**: No background processes
- ✅ **Direct Control**: Full control over token management
- ❌ **Manual Token Management**: No automatic refresh

### 3. Standalone Extractors with Environment Variables

**Use Case**: Quick scripts using default REVOS_ prefix

```python
from revos.llm.tools import get_langchain_extractor

# Uses environment variables with REVOS_ prefix
extractor = get_langchain_extractor("gpt-4")
# ✅ Uses default REVOS_ config from environment
# ❌ No automatic token updates
```

**Key Benefits**:
- ✅ **Zero Configuration**: Works out of the box
- ✅ **Environment-Based**: Uses standard REVOS_ environment variables
- ✅ **Simple**: No custom configuration needed
- ❌ **Limited Customization**: Only REVOS_ prefix supported
- ❌ **Manual Token Management**: No automatic refresh

## Configuration Priority

The system follows a clear priority order:

1. **Global Config** (highest priority) - Set by TokenManager
2. **Explicit Settings** - Passed to extractor constructor
3. **Environment Variables** - Default REVOS_ prefix

```python
# Priority example
token_manager = TokenManager(settings_instance=rumba_config)  # Sets global config

# Even with explicit settings, global config wins
extractor = get_langchain_extractor("gpt-4", settings_instance=other_config)
# Result: Uses rumba_config (global config overrides explicit settings)
```

## Key Benefits by Scenario

### Production Applications

| Feature | TokenManager + Global | Standalone + Custom | Standalone + Env |
|---------|----------------------|-------------------|------------------|
| **Automatic Token Refresh** | ✅ Yes | ❌ No | ❌ No |
| **Background Management** | ✅ Yes | ❌ No | ❌ No |
| **Observer Pattern** | ✅ Zero Duplicate Requests | ❌ No | ❌ No |
| **Configuration Consistency** | ✅ Yes | ⚠️ Manual | ⚠️ Manual |
| **Custom Prefixes** | ✅ Yes | ✅ Yes | ❌ No |
| **Zero Configuration** | ❌ No | ❌ No | ✅ Yes |

### Development and Testing

| Feature | TokenManager + Global | Standalone + Custom | Standalone + Env |
|---------|----------------------|-------------------|------------------|
| **Quick Setup** | ⚠️ Medium | ✅ Yes | ✅ Yes |
| **Testing Flexibility** | ⚠️ Medium | ✅ Yes | ✅ Yes |
| **Debugging** | ⚠️ Complex | ✅ Simple | ✅ Simple |
| **Isolation** | ❌ No | ✅ Yes | ✅ Yes |

## Use Case Recommendations

### 🏢 **Production Applications**
**Recommended**: TokenManager with Global Config
- Automatic token management
- Consistent configuration across all components
- Real-time token updates
- Background refresh capabilities

### 🧪 **Development and Testing**
**Recommended**: Standalone with Custom Settings
- Quick setup and teardown
- Isolated testing
- Custom configuration per test
- No background processes

### 📝 **Simple Scripts**
**Recommended**: Standalone with Environment Variables
- Zero configuration
- Quick execution
- No complex setup
- Uses standard environment variables

### 🔄 **Mixed Environments**
**Recommended**: TokenManager with Global Config
- Consistent behavior across environments
- Automatic configuration sharing
- Reduced configuration management
- Centralized token management

## Migration Guide

### From Standalone to Global Config

**Before (Standalone)**:
```python
# Each extractor needs explicit configuration
extractor1 = get_langchain_extractor("gpt-4", settings_instance=config1)
extractor2 = get_langchain_extractor("gpt-3.5-turbo", settings_instance=config2)
# Manual token management
```

**After (Global Config)**:
```python
# Set global configuration once
token_manager = TokenManager(settings_instance=config)
# All extractors automatically use the same config
extractor1 = get_langchain_extractor("gpt-4")
extractor2 = get_langchain_extractor("gpt-3.5-turbo")
# Automatic token management
```

### From Environment Variables to Custom Prefixes

**Before (Environment Variables)**:
```bash
export REVOS_CLIENT_ID="your-client-id"
export REVOS_CLIENT_SECRET="your-client-secret"
export REVOS_BASE_URL="https://api.example.com"
```

**After (Custom Prefixes)**:
```bash
export RUMBA_CLIENT_ID="your-client-id"
export RUMBA_CLIENT_SECRET="your-client-secret"
export RUMBA_BASE_URL="https://api.example.com"
```

## Best Practices

### ✅ **Do**
- Use TokenManager with global config for production applications
- Use standalone extractors for simple scripts and testing
- Set up proper environment variables for your chosen prefix
- Test both scenarios to ensure compatibility

### ❌ **Don't**
- Mix global config and explicit settings (global config always wins)
- Use TokenManager for simple one-off scripts
- Forget to set up environment variables for your chosen prefix
- Assume all extractors will automatically get updates without TokenManager

## Troubleshooting

### Common Issues

**Issue**: Extractor not using custom settings
**Cause**: TokenManager is running and global config overrides explicit settings
**Solution**: Either remove TokenManager or use the global config approach

**Issue**: No automatic token updates
**Cause**: Extractor is running standalone without TokenManager
**Solution**: Initialize TokenManager with your configuration

**Issue**: Configuration mismatch between components
**Cause**: Not using global config approach
**Solution**: Use TokenManager to set global configuration

### Debug Tips

1. **Check Global Config**: Use `get_global_config()` to see if TokenManager is running
2. **Verify Observer Registration**: Check if extractors are registered as observers
3. **Monitor Token Updates**: Look for log messages about token refresh notifications
4. **Test Both Scenarios**: Ensure your code works with and without TokenManager

## Conclusion

The global config approach provides a powerful and flexible way to manage configuration and token refresh across your Revos application. Choose the approach that best fits your use case:

- **Production**: TokenManager with global config
- **Development**: Standalone with custom settings
- **Simple Scripts**: Standalone with environment variables

The system is designed to "just work" in all scenarios while providing the flexibility to customize behavior as needed.
