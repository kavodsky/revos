# Release Notes - Revos 0.1.7

**Release Date:** December 2024  
**Version:** 0.1.7

## 🎉 Major Improvements

### 🔄 Observer Pattern for Automatic Token Updates
- **Automatic Extractor Updates**: LangChainExtractor instances automatically get updated tokens when TokenManager refreshes them
- **No Manual Intervention**: Extractors update themselves without additional API calls
- **Background-Safe**: Perfect for FastAPI background token management scenarios
- **Efficient Architecture**: Uses Observer Pattern for clean, scalable token management

**New Capability:**
```python
# Extractors automatically register for token updates
extractor1 = get_langchain_extractor("gpt_4", settings_instance=config)
extractor2 = get_langchain_extractor("claude_4", settings_instance=config)

# When TokenManager refreshes tokens, ALL extractors get updated automatically!
token_manager = TokenManager(settings_instance=config)
await token_manager.start_background_service()
```

### 🔧 Enhanced TokenManager Configuration
- **Automatic Config Reading**: `TokenManager` now automatically uses `refresh_interval_minutes` from custom settings
- **Simplified API**: No need to manually pass refresh interval when using custom configurations
- **Backward Compatibility**: All existing code continues to work without changes

**Before:**
```python
token_manager = TokenManager(
    refresh_interval_minutes=config.token_manager.refresh_interval_minutes,
    settings_instance=config
)
```

**After:**
```python
token_manager = TokenManager(settings_instance=config)
```

### 🛠️ Fixed Background Token Refresh with Custom Settings
- **Critical Bug Fix**: Background token refresh process now properly uses custom settings
- **Resolved Validation Errors**: Fixed "Field required" errors when using custom environment variable prefixes
- **Improved Reliability**: Background services now work correctly with custom configurations

### 📚 Comprehensive Documentation Restructure
- **Shorter README**: Reduced from ~1800 lines to ~150 lines for better readability
- **Organized Documentation**: Moved detailed examples to separate documentation files
- **Better Navigation**: Clear links to specific guides and examples

## 🆕 New Features

### 📖 New Documentation Files
- **[docs/llm-models.md](docs/llm-models.md)** - Comprehensive LLM models configuration guide
- **[docs/fastapi-examples.md](docs/fastapi-examples.md)** - FastAPI integration examples and patterns
- **[docs/custom-prefixes.md](docs/custom-prefixes.md)** - Custom environment variable prefixes guide
- **[docs/token-management.md](docs/token-management.md)** - Advanced token management and background services

### 🧪 Enhanced Testing
- **New Test Suite**: Added comprehensive tests for background token refresh with custom settings
- **13 New Tests**: Covering all aspects of custom settings integration
- **Better Coverage**: Tests ensure the background process works correctly with custom configurations

## 🔧 Technical Improvements

### Token Management
- **Smart Configuration**: `TokenManager` automatically reads refresh interval from custom settings
- **Explicit Override**: Can still explicitly pass `refresh_interval_minutes` to override config
- **Fallback Behavior**: Gracefully falls back to defaults when no config is provided

### Background Services
- **Custom Settings Support**: Background token refresh now properly uses custom settings
- **Error Resolution**: Fixed validation errors when using custom environment variable prefixes
- **Improved Reliability**: Background services work consistently across different configurations

### Configuration Management
- **Enhanced Factory Functions**: Improved `create_config_with_prefixes()` functionality
- **Better Error Handling**: More descriptive error messages for configuration issues
- **Flexible Settings**: Support for complex custom prefix configurations

## 🐛 Bug Fixes

### Critical Fixes
- **Background Token Refresh**: Fixed critical issue where background process wasn't using custom settings
- **Validation Errors**: Resolved "Field required" errors for `client_id` and `client_secret` in background processes
- **Custom Prefix Support**: Fixed background services to work correctly with custom environment variable prefixes

### Minor Fixes
- **Documentation Links**: Fixed internal documentation links
- **Example Code**: Updated examples to use simplified API
- **Test Coverage**: Improved test coverage for edge cases

## 📈 Performance Improvements

### Token Management
- **Reduced Boilerplate**: Less code required for common use cases
- **Faster Configuration**: Automatic config reading reduces setup time
- **Better Error Handling**: More efficient error detection and reporting

### Documentation
- **Faster Navigation**: Shorter README loads faster and is easier to scan
- **Better Organization**: Related content grouped for easier maintenance
- **Improved User Experience**: Clear separation between quick start and detailed guides

## 🔄 API Changes

### TokenManager Constructor
```python
# New simplified API
TokenManager(settings_instance=config)  # Automatically uses config refresh interval

# Explicit override still works
TokenManager(refresh_interval_minutes=60, settings_instance=config)

# Backward compatible
TokenManager(refresh_interval_minutes=45)  # Uses default settings
```

### Background Services
- **Custom Settings**: Background services now properly use custom settings
- **Error Handling**: Better error messages for configuration issues
- **Reliability**: More consistent behavior across different configurations

## 📋 Migration Guide

### For Existing Users
- **No Breaking Changes**: All existing code continues to work
- **Optional Improvements**: Can optionally simplify code using new API
- **Gradual Migration**: Can update code incrementally

### Recommended Updates
1. **Simplify TokenManager Usage**:
   ```python
   # Old way (still works)
   token_manager = TokenManager(
       refresh_interval_minutes=config.token_manager.refresh_interval_minutes,
       settings_instance=config
   )
   
   # New way (recommended)
   token_manager = TokenManager(settings_instance=config)
   ```

2. **Update Documentation References**:
   - Use new documentation structure
   - Reference specific guides for detailed information
   - Follow new examples for best practices

## 🧪 Testing

### New Test Coverage
- **Background Custom Settings**: 13 new tests covering background token refresh with custom settings
- **Configuration Validation**: Tests for various custom prefix configurations
- **Error Scenarios**: Tests for edge cases and error conditions
- **Integration Tests**: End-to-end testing of complete workflows

### Test Results
- ✅ **All 36 existing tests pass** - No regressions
- ✅ **13 new tests pass** - New functionality verified
- ✅ **100% backward compatibility** - Existing code unchanged

## 📦 Installation

### From Source
```bash
git clone https://github.com/yourusername/revo.git
cd revo
git checkout v0.1.7
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/yourusername/revo.git
cd revo
git checkout v0.1.7
pip install -e ".[dev]"
```

## 🔗 Documentation

- **[README.md](README.md)** - Quick start and overview
- **[docs/llm-models.md](docs/llm-models.md)** - LLM models configuration
- **[docs/fastapi-examples.md](docs/fastapi-examples.md)** - FastAPI integration
- **[docs/custom-prefixes.md](docs/custom-prefixes.md)** - Custom environment variable prefixes
- **[docs/token-management.md](docs/token-management.md)** - Advanced token management

## 🎯 What's Next

### Planned Features
- **Enhanced Monitoring**: Better token health monitoring and alerting
- **Performance Metrics**: Detailed performance tracking for token operations
- **Advanced Configuration**: More flexible configuration options
- **Additional Examples**: More real-world usage examples

### Community Feedback
- **Bug Reports**: Please report any issues on GitHub
- **Feature Requests**: Suggest new features and improvements
- **Documentation**: Help improve documentation and examples

## 🙏 Acknowledgments

Thanks to all contributors and users who provided feedback and helped identify the issues fixed in this release.

---

**Full Changelog**: [v0.1.6...v0.1.7](https://github.com/yourusername/revo/compare/v0.1.6...v0.1.7)

