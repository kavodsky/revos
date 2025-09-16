# Revos

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **Quick Start**

    ---

    Get up and running with Revos in minutes

    [:octicons-arrow-right-24: Quick Start](getting-started/quick-start.md)

-   :material-cog:{ .lg .middle } **Configuration**

    ---

    Learn how to configure Revos for your needs

    [:octicons-arrow-right-24: Configuration](getting-started/configuration.md)

-   :material-api:{ .lg .middle } **API Reference**

    ---

    Complete API documentation and examples

    [:octicons-arrow-right-24: API Reference](api/configuration.md)

-   :material-lightning-bolt:{ .lg .middle } **FastAPI Integration**

    ---

    Integrate Revos with FastAPI applications

    [:octicons-arrow-right-24: FastAPI Guide](fastapi/basic-setup.md)

</div>

## What is Revos?

Revos is a powerful Python library that provides seamless integration between your applications and Revos API services. It offers robust authentication, LangChain-based LLM tools, and comprehensive token management with support for multiple LLM models.

## Key Features

<div class="grid cards" markdown>

-   :material-shield-check:{ .lg .middle } **Robust Authentication**

    ---

    Dual authentication methods with automatic fallback and comprehensive error handling

-   :material-brain:{ .lg .middle } **LangChain Integration**

    ---

    Structured data extraction using LLMs with OpenAI-compatible APIs

-   :material-cogs:{ .lg .middle } **Multiple LLM Models**

    ---

    Support for multiple models with different configurations and easy switching

-   :material-refresh:{ .lg .middle } **Token Management**

    ---

    Automatic token refresh with configurable intervals and background services

-   :material-settings:{ .lg .middle } **Flexible Configuration**

    ---

    Environment variables, YAML, JSON, and programmatic configuration options

-   :material-test-tube:{ .lg .middle } **Comprehensive Testing**

    ---

    Full test suite with pytest and extensive error handling

</div>

## Quick Example

```python
from revos import LangChainExtractor, get_revos_token
from pydantic import BaseModel

# Define your data model
class DocumentSummary(BaseModel):
    title: str
    summary: str
    key_points: list[str]
    confidence: float

# Initialize the extractor
extractor = LangChainExtractor(model_name="gpt-4")

# Extract structured data
result = extractor.extract_structured_data(
    prompt="Summarize this document: Your document text here...",
    target_class=DocumentSummary
)

print(f"Title: {result.title}")
print(f"Summary: {result.summary}")
print(f"Key Points: {result.key_points}")
```

## Installation

```bash
# From source
git clone https://github.com/yourusername/revos.git
cd revos
pip install -e .

# Development installation
pip install -e ".[dev]"
```

## Configuration

Set up your environment variables:

```bash
export REVOS_CLIENT_ID="your_client_id"
export REVOS_CLIENT_SECRET="your_client_secret"
export REVOS_TOKEN_URL="https://your-site.com/revo/oauth/token"
export REVOS_BASE_URL="https://your-site.com/revo/llm-api"
```

## FastAPI Integration

Revos integrates seamlessly with FastAPI applications:

```python
from fastapi import FastAPI
from revos import LangChainExtractor
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    global extractor
    extractor = LangChainExtractor(model_name="gpt-4")
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/summarize")
async def summarize(text: str):
    result = extractor.extract_structured_data(
        prompt=f"Summarize: {text}",
        target_class=DocumentSummary
    )
    return {"summary": result.dict()}
```

## What's Next?

- [:octicons-arrow-right-24: **Getting Started**](getting-started/installation.md) – Install and configure Revos
- [:octicons-arrow-right-24: **User Guide**](user-guide/authentication.md) – Learn the core concepts
- [:octicons-arrow-right-24: **FastAPI Integration**](fastapi/basic-setup.md) – Build web applications
- [:octicons-arrow-right-24: **Examples**](examples/basic-usage.md) – Explore practical examples
- [:octicons-arrow-right-24: **API Reference**](api/configuration.md) – Complete API documentation

---

<div class="grid cards" markdown>

-   :material-github:{ .lg .middle } **GitHub**

    ---

    View source code, report issues, and contribute

    [:octicons-arrow-right-24: GitHub](https://github.com/yourusername/revos)

-   :material-package:{ .lg .middle } **PyPI**

    ---

    Install Revos from PyPI

    [:octicons-arrow-right-24: PyPI](https://pypi.org/project/revos/)

-   :material-book:{ .lg .middle } **Documentation**

    ---

    Read the complete documentation

    [:octicons-arrow-right-24: Documentation](https://yourusername.github.io/revos)

</div>
