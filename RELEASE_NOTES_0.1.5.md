# Release Notes - Revos 0.1.5

## 🚀 New Features

### 🔧 Custom Prefix Support for LLM Models
- **Flexible Environment Variable Prefixes**: You can now use any custom prefix for LLM model configuration instead of being locked to `LLM_MODELS_`
- **Examples**:
  ```bash
  # Using AI_ prefix
  AI_GPT_4_MODEL=gpt-4
  AI_GPT_4_TEMPERATURE=0.1
  AI_CLAUDE_MODEL=claude-3-sonnet
  
  # Using MODELS_ prefix  
  MODELS_GPT_4_MODEL=gpt-4
  MODELS_GPT_4_TEMPERATURE=0.1
  
  # Using short M_ prefix
  M_GPT_4_MODEL=gpt-4
  M_GPT_4_TEMPERATURE=0.1
  ```

### 🎯 Environment Variable Override Behavior
- **Smart Model Loading**: When you specify models in your `.env` file, the library now uses ONLY those models instead of mixing them with hardcoded defaults
- **Complete Control**: Users get exactly the models they configure, nothing more
- **Cleaner Configuration**: No unexpected default models appearing

### 🛡️ Prefix Validation
- **Conflict Prevention**: Added validation to prevent duplicate prefixes that could cause variable name conflicts
- **Clear Error Messages**: Helpful error messages when prefixes are duplicated
- **Better Debugging**: Easy to identify which prefixes are causing issues

## 🔧 Improvements

### Enhanced Configuration Factory
- **Custom Prefix Support**: `create_config_with_prefixes()` now properly handles custom LLM prefixes
- **Validation**: Prevents configuration conflicts with clear error messages
- **Flexibility**: Support for any prefix format (AI_, MODELS_, M_, etc.)

### Better Environment Variable Parsing
- **Custom Parser**: New `env_parser.py` module for flexible environment variable parsing
- **Model Grouping**: Automatically groups environment variables by model name
- **Type Conversion**: Smart conversion of string values to appropriate Python types

## 🐛 Bug Fixes

### Fixed Model Name Format Issues
- **Consistent Naming**: Fixed inconsistencies between model names in configuration and API calls
- **Environment Variable Parsing**: Corrected parsing of custom prefix environment variables
- **Test Coverage**: Updated tests to use correct environment variable formats

### Improved Error Handling
- **Better Error Messages**: More descriptive error messages for configuration issues
- **Validation**: Added comprehensive validation for all configuration scenarios

## 📚 Documentation Updates

### Updated README
- **Multiple Models Configuration**: Added comprehensive section on configuring multiple LLM models
- **Custom Prefixes**: Updated examples to show custom prefix usage
- **Environment Variables**: Clarified the new environment variable format
- **API Reference**: Updated to reflect new configuration options

### Examples and Guides
- **Environment Variable Examples**: Added examples for different prefix formats
- **Configuration Scenarios**: Documented various configuration approaches
- **Best Practices**: Added guidance on prefix naming conventions

## 🧪 Testing

### Comprehensive Test Suite
- **Prefix Validation Tests**: 17 comprehensive test cases covering all edge cases
- **Environment Variable Tests**: Tests for different prefix formats and scenarios
- **Error Handling Tests**: Tests for validation and error conditions
- **Edge Case Coverage**: Tests for special characters, unicode, and edge cases

### Test Results
- **✅ 104 tests passing**
- **✅ 100% test coverage for new features**
- **✅ No regressions**

## 🔄 Breaking Changes

### Environment Variable Format
- **Old Format**: `LLM_MODELS_CLAUDE_4_SONNET_MODEL=claude_4_sonnet`
- **New Format**: `LLM_CLAUDE_4_SONNET_MODEL=claude_4_sonnet` (when using `llm_prefix="LLM_"`)

### Configuration Behavior
- **Environment Override**: When environment variables are found, hardcoded defaults are no longer used
- **Prefix Validation**: Duplicate prefixes now raise `ValueError` instead of being silently ignored

## 🚀 Migration Guide

### For Existing Users
1. **Update Environment Variables**: Change from `LLM_MODELS_*` to your chosen prefix format
2. **Review Configuration**: Ensure your custom prefixes don't conflict
3. **Test Configuration**: Verify your models are loaded correctly

### Example Migration
```bash
# Before (0.1.4)
LLM_MODELS_CLAUDE_4_SONNET_MODEL=claude_4_sonnet
LLM_MODELS_CLAUDE_4_SONNET_TEMPERATURE=0.3

# After (0.1.5) - using LLM_ prefix
LLM_CLAUDE_4_SONNET_MODEL=claude_4_sonnet
LLM_CLAUDE_4_SONNET_TEMPERATURE=0.3

# Or using custom AI_ prefix
AI_CLAUDE_4_SONNET_MODEL=claude_4_sonnet
AI_CLAUDE_4_SONNET_TEMPERATURE=0.3
```

## 📦 Installation

```bash
pip install revos==0.1.5
```

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for more information.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Full Changelog**: https://github.com/your-org/revos/compare/0.1.4...0.1.5
