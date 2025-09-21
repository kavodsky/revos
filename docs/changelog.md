# Changelog

All notable changes to the Revos library will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive MkDocs documentation
- FastAPI integration examples
- Multiple LLM model support
- Background token management
- Comprehensive test suite

### Changed
- Renamed from `revo` to `revos` for consistency
- Updated all configuration classes and methods
- Improved error handling with traceback output

### Fixed
- Token refresh logic without LLM calls
- Async test configuration issues
- Mock configuration in test suite

## [0.1.6] - 2024-12-19

### Added
- **Enhanced TokenManager Environment Variable Support**: Full support for loading custom environment variables from `.env` files
- **Flexible Prefix Support**: Support for any custom prefix (TOKEN_, AUTH_, CUSTOM_, etc.) for token management configuration
- **Comprehensive Test Suite**: Added 7 new test cases specifically for TokenManager environment variable loading
- **Type Conversion**: Smart conversion of string environment variables to appropriate Python types (booleans, integers)
- **Configuration Validation**: Enhanced validation for all TokenManager configuration fields with proper range checking

### Changed
- **TokenManager Configuration**: Enhanced default values and field constraints for all settings
- **Configuration Factory**: Improved `create_config_with_prefixes()` function to support custom token management prefixes
- **Environment File Loading**: Better handling of custom `.env` files with proper encoding and error handling
- **Error Messages**: More descriptive error messages for configuration issues

### Fixed
- **Configuration Loading Issues**: Fixed environment variables not being properly loaded from `.env` files
- **Missing Import**: Fixed missing `LLMConfig` import in `RevosMainConfig`
- **Prefix Conflicts**: Resolved conflicts between different configuration prefixes
- **Type Conversion**: Fixed string-to-type conversion issues for boolean and numeric values
- **Environment File Handling**: Improved handling of environment files in main configuration

### Technical Details
- **Test Coverage**: 58 token-related tests passing with comprehensive coverage
- **Environment Variables**: Support for TOKEN_, AUTH_, CUSTOM_TOKEN_, and any custom prefix
- **Validation**: Proper min/max constraints for numeric fields and boolean parsing
- **Integration**: Seamless integration with RevosMainConfig system

## [1.0.0] - 2024-01-15

### Added
- Initial release of Revos library
- Revos API authentication with dual methods
- LangChain-based structured data extraction
- Token management with automatic refresh
- Multiple configuration methods (env vars, YAML, JSON, programmatic)
- Support for multiple LLM models
- Comprehensive error handling and retry logic
- Full test suite with pytest
- Rich examples and documentation

### Features
- **Authentication**: Dual authentication methods with automatic fallback
- **LLM Integration**: Structured data extraction using LangChain
- **Token Management**: Automatic refresh with configurable intervals
- **Configuration**: Flexible configuration management with pydantic-settings
- **Multiple Models**: Support for different LLM models and configurations
- **Error Handling**: Comprehensive retry logic and fallback mechanisms
- **Testing**: Full test suite with 97 passing tests
- **Documentation**: Comprehensive documentation with examples

### Technical Details
- **Python**: 3.8+ support (3.11+ recommended)
- **Dependencies**: requests, httpx, langchain-core, pydantic, pydantic-settings
- **Testing**: pytest with async support
- **Documentation**: MkDocs with Material theme
- **Build System**: Modern Python packaging with pyproject.toml

## [0.9.0] - 2024-01-10

### Added
- Initial development version
- Basic authentication functionality
- Simple LLM integration
- Basic configuration system

### Changed
- Package structure and organization
- Configuration management approach

### Fixed
- Initial authentication issues
- Configuration loading problems

## [0.8.0] - 2024-01-05

### Added
- First working prototype
- Basic API integration
- Simple token management

### Known Issues
- Limited error handling
- Basic configuration only
- No test coverage

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2024-01-15 | First stable release with full feature set |
| 0.9.0 | 2024-01-10 | Development version with core features |
| 0.8.0 | 2024-01-05 | Initial prototype |

## Migration Guide

### From 0.9.0 to 1.0.0

#### Breaking Changes
- Package renamed from `revo` to `revos`
- Configuration classes renamed:
  - `RevoConfig` → `RevosConfig`
  - `RevoMainConfig` → `RevosMainConfig`
  - `RevoTokenManager` → `RevosTokenManager`
- Function names updated:
  - `get_revo_token()` → `get_revos_token()`
  - `invalidate_revo_token()` → `invalidate_revos_token()`

#### Migration Steps
1. Update imports:
   ```python
   # Old
   from revo import RevoConfig, get_revo_token
   
   # New
   from revos import RevosConfig, get_revos_token
   ```

2. Update environment variables:
   ```bash
   # Old
   REVO_CLIENT_ID=your_client_id
   REVO_CLIENT_SECRET=your_client_secret
   
   # New
   REVOS_CLIENT_ID=your_client_id
   REVOS_CLIENT_SECRET=your_client_secret
   ```

3. Update configuration files:
   ```yaml
   # Old
   revo:
     client_id: your_client_id
   
   # New
   revos:
     client_id: your_client_id
   ```

### From 0.8.0 to 0.9.0

#### Breaking Changes
- Configuration system completely rewritten
- Authentication flow updated
- Token management restructured

#### Migration Steps
1. Update configuration approach
2. Review authentication setup
3. Test token management functionality

## Contributing

We welcome contributions! Please see our [Contributing Guide](development/contributing.md) for details.

## Support

- **Documentation**: [https://yourusername.github.io/revos](https://yourusername.github.io/revos)
- **GitHub Issues**: [https://github.com/yourusername/revos/issues](https://github.com/yourusername/revos/issues)
- **Discussions**: [https://github.com/yourusername/revos/discussions](https://github.com/yourusername/revos/discussions)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
