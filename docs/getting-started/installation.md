# Installation

## Prerequisites

Before installing Revos, ensure you have:

- **Python 3.8+** (Python 3.11+ recommended)
- **pip** or **uv** package manager
- **Git** (for source installation)

## Installation Methods

### From Source (Recommended)

Clone the repository and install in development mode:

```bash
git clone https://github.com/yourusername/revos.git
cd revos
pip install -e .
```

### Development Installation

For development with all dependencies:

```bash
git clone https://github.com/yourusername/revos.git
cd revos
pip install -e ".[dev]"
```

### Using uv (Fast)

If you have `uv` installed:

```bash
git clone https://github.com/yourusername/revos.git
cd revos
uv pip install -e .
```

## Verify Installation

Test your installation:

```python
import revos
print(f"Revos version: {revos.__version__}")

# Test basic functionality
from revos import get_revos_token
print("✅ Revos installed successfully!")
```

## Dependencies

Revos automatically installs the following dependencies:

### Core Dependencies
- `requests>=2.31.0` - HTTP client for API requests
- `httpx>=0.25.0` - Modern async HTTP client
- `httpx-auth>=0.20.0` - Authentication for httpx
- `langchain-core>=0.1.0` - LangChain core functionality
- `langchain-openai>=0.1.0` - OpenAI integration
- `pydantic>=2.0.0` - Data validation and settings
- `pydantic-settings>=2.0.0` - Settings management
- `python-dotenv>=1.0.0` - Environment variable loading

### Development Dependencies
- `pytest>=7.0.0` - Testing framework
- `pytest-asyncio>=1.2.0` - Async testing support
- `black>=23.0.0` - Code formatting
- `isort>=5.12.0` - Import sorting
- `mypy>=1.0.0` - Type checking

## Environment Setup

### 1. Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Using uv (recommended)
uv venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
# Using pip
pip install -e ".[dev]"

# Using uv
uv pip install -e ".[dev]"
```

### 3. Set Environment Variables

Create a `.env` file:

```bash
# Required
REVOS_CLIENT_ID=your_client_id
REVOS_CLIENT_SECRET=your_client_secret

# Optional
REVOS_TOKEN_URL=https://your-site.com/revo/oauth/token
REVOS_BASE_URL=https://your-site.com/revo/llm-api
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.1
```

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# If you get import errors, ensure you're in the right environment
which python
pip list | grep revos
```

#### Permission Errors
```bash
# Use --user flag if you don't have admin rights
pip install --user -e .
```

#### Version Conflicts
```bash
# Check for conflicting packages
pip check
pip list --outdated
```

### Getting Help

If you encounter issues:

1. **Check the logs** for detailed error messages
2. **Verify your environment** variables are set correctly
3. **Update dependencies** to the latest versions
4. **Check GitHub issues** for known problems
5. **Create a new issue** if the problem persists

## Next Steps

Now that Revos is installed:

1. [:octicons-arrow-right-24: **Configure Revos**](configuration.md) – Set up your configuration
2. [:octicons-arrow-right-24: **Quick Start**](quick-start.md) – Run your first example
3. [:octicons-arrow-right-24: **Authentication**](../user-guide/authentication.md) – Learn about authentication

## System Requirements

### Minimum Requirements
- **Python**: 3.8+
- **Memory**: 512MB RAM
- **Storage**: 100MB free space
- **Network**: Internet connection for API calls

### Recommended Requirements
- **Python**: 3.11+
- **Memory**: 2GB+ RAM
- **Storage**: 1GB+ free space
- **Network**: Stable internet connection

### Supported Platforms
- ✅ **Linux** (Ubuntu, CentOS, Debian, etc.)
- ✅ **macOS** (10.15+)
- ✅ **Windows** (10+)
- ✅ **Docker** containers
- ✅ **Cloud platforms** (AWS, GCP, Azure)
