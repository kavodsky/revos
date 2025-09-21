# Release Notes - Revos 0.1.6

## 🚀 New Features

### 🔧 Enhanced TokenManager Environment Variable Support
- **Comprehensive .env File Support**: TokenManager now fully supports loading custom environment variables from `.env` files
- **Flexible Prefix Support**: Support for any custom prefix (TOKEN_, AUTH_, CUSTOM_, etc.) for token management configuration
- **Examples**:
  ```bash
  # Default TOKEN_ prefix
  TOKEN_REFRESH_INTERVAL_MINUTES=30
  TOKEN_MAX_FAILURES_BEFORE_FALLBACK=3
  TOKEN_ENABLE_PERIODIC_REFRESH=false
  TOKEN_ENABLE_FALLBACK=false
  
  # Custom AUTH_ prefix
  AUTH_REFRESH_INTERVAL_MINUTES=60
  AUTH_MAX_FAILURES_BEFORE_FALLBACK=5
  AUTH_ENABLE_PERIODIC_REFRESH=true
  AUTH_ENABLE_FALLBACK=true
  
  # Custom CUSTOM_TOKEN_ prefix
  CUSTOM_TOKEN_REFRESH_INTERVAL_MINUTES=90
  CUSTOM_TOKEN_MAX_FAILURES_BEFORE_FALLBACK=7
  ```

### 🎯 Improved Configuration Integration
- **RevosMainConfig Integration**: TokenManager settings now seamlessly integrate with the full RevosMainConfig system
- **Environment File Loading**: Automatic loading of `.env` files with proper encoding and error handling
- **Type Conversion**: Smart conversion of string environment variables to appropriate Python types (booleans, integers)

### 🛡️ Enhanced Configuration Validation
- **Field Validation**: Comprehensive validation for all TokenManager configuration fields
- **Range Checking**: Proper validation for numeric fields (refresh intervals, failure counts)
- **Error Messages**: Clear, descriptive error messages for invalid configuration values

## 🔧 Improvements

### TokenManager Configuration
- **Default Values**: Well-defined default values for all TokenManager settings
- **Field Constraints**: Proper min/max constraints for numeric fields
- **Boolean Handling**: Improved boolean value parsing from environment variables

### Configuration Factory
- **Custom Prefix Support**: Enhanced `create_config_with_prefixes()` function to support custom token management prefixes
- **Environment File Support**: Proper handling of custom `.env` files in configuration factory
- **Validation**: Added validation to prevent configuration conflicts

### Better Error Handling
- **Configuration Errors**: Improved error messages for missing required fields
- **Validation Errors**: Clear error messages for invalid configuration values
- **Environment Loading**: Better error handling for `.env` file loading issues

## 🐛 Bug Fixes

### Fixed Configuration Loading Issues
- **Environment Variable Loading**: Fixed issues with environment variables not being properly loaded from `.env` files
- **Prefix Conflicts**: Resolved conflicts between different configuration prefixes
- **Type Conversion**: Fixed string-to-type conversion issues for boolean and numeric values

### Improved Main Configuration
- **Missing Import**: Fixed missing `LLMConfig` import in `RevosMainConfig`
- **Environment File Handling**: Improved handling of environment files in main configuration
- **Nested Configuration**: Fixed issues with nested configuration loading

## 📚 Documentation Updates

### Enhanced Test Coverage
- **Comprehensive Test Suite**: Added 7 new test cases specifically for TokenManager environment variable loading
- **Test Categories**:
  - Default TOKEN_ prefix configuration
  - Custom prefix configuration (AUTH_, CUSTOM_TOKEN_, etc.)
  - RevosMainConfig integration
  - Environment file loading
  - Configuration defaults validation
  - Input validation testing
  - Multiple environment files support

### Updated Examples
- **Environment Variable Examples**: Added comprehensive examples for different prefix formats
- **Configuration Scenarios**: Documented various TokenManager configuration approaches
- **Best Practices**: Added guidance on environment variable naming conventions

## 🧪 Testing

### New Test Suite: `test_token_env_vars.py`
- **✅ 7 comprehensive test cases**
- **✅ 100% coverage of TokenManager environment variable functionality**
- **✅ Tests for default and custom prefixes**
- **✅ Integration testing with RevosMainConfig**
- **✅ Validation and error handling tests**
- **✅ Multiple environment file support tests**

### Test Results
- **✅ All 58 token-related tests passing**
- **✅ No regressions in existing functionality**
- **✅ Comprehensive coverage of new features**

## 🔄 API Changes

### Enhanced TokenManagerConfig
- **Environment File Support**: Automatic `.env` file loading with `env_file=".env"`
- **Custom Prefixes**: Support for any prefix via `env_prefix` parameter
- **Type Safety**: Proper type conversion and validation for all fields

### Improved Configuration Factory
- **Custom Prefix Support**: Enhanced `create_config_with_prefixes()` for token management
- **Environment File Integration**: Proper handling of custom `.env` files
- **Validation**: Added validation for prefix conflicts

## 🚀 Migration Guide

### For Existing Users
1. **Environment Variables**: You can now use custom prefixes for TokenManager configuration
2. **Configuration Files**: Enhanced support for `.env` files with TokenManager settings
3. **Validation**: New validation ensures configuration values are within acceptable ranges

### Example Migration
```bash
# Before (0.1.5) - limited environment variable support
# TokenManager settings were not fully configurable via .env

# After (0.1.6) - full .env support
# Default TOKEN_ prefix
TOKEN_REFRESH_INTERVAL_MINUTES=45
TOKEN_MAX_FAILURES_BEFORE_FALLBACK=1
TOKEN_ENABLE_PERIODIC_REFRESH=true
TOKEN_ENABLE_FALLBACK=true

# Or with custom AUTH_ prefix
AUTH_REFRESH_INTERVAL_MINUTES=30
AUTH_MAX_FAILURES_BEFORE_FALLBACK=3
AUTH_ENABLE_PERIODIC_REFRESH=false
AUTH_ENABLE_FALLBACK=false
```

## 📦 Installation

```bash
pip install revos==0.1.6
```

## 🎯 Key Benefits

### For Developers
- **Flexible Configuration**: Use any prefix for TokenManager environment variables
- **Better Integration**: Seamless integration with existing RevosMainConfig system
- **Type Safety**: Proper validation and type conversion for all configuration values
- **Comprehensive Testing**: Extensive test coverage ensures reliability

### For Operations
- **Environment Management**: Easy configuration via `.env` files
- **Prefix Customization**: Use organization-specific prefixes to avoid conflicts
- **Validation**: Built-in validation prevents configuration errors
- **Error Handling**: Clear error messages for troubleshooting

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for more information.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Full Changelog**: https://github.com/kavodsky/revos/compare/0.1.5...0.1.6
