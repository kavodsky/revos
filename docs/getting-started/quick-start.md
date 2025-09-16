# Quick Start

Get up and running with Revos in just a few minutes! This guide will walk you through the essential steps to start using Revos for authentication and LLM integration.

## Prerequisites

Before starting, ensure you have:

- ✅ Revos installed (see [Installation](installation.md))
- ✅ Valid Revos API credentials
- ✅ Python 3.8+ environment

## Step 1: Set Up Environment Variables

Create a `.env` file in your project directory:

```bash
# Required credentials
REVOS_CLIENT_ID=your_client_id
REVOS_CLIENT_SECRET=your_client_secret

# Optional: Custom endpoints
REVOS_TOKEN_URL=https://your-site.com/revo/oauth/token
REVOS_BASE_URL=https://your-site.com/revo/llm-api

# LLM Configuration
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.1
```

## Step 2: Basic Authentication

Test your authentication setup:

```python
from revos import get_revos_token

# Get a token
token = get_revos_token()
print(f"✅ Token obtained: {token[:20]}...")
```

## Step 3: Simple Data Extraction

Create your first structured data extraction:

```python
from revos import LangChainExtractor
from pydantic import BaseModel

# Define your data model
class PersonInfo(BaseModel):
    name: str
    age: int
    occupation: str
    location: str

# Initialize the extractor
extractor = LangChainExtractor(model_name="gpt-4")

# Extract structured data
result = extractor.extract_structured_data(
    prompt="John is a 30-year-old software engineer living in San Francisco.",
    target_class=PersonInfo
)

print(f"Name: {result.name}")
print(f"Age: {result.age}")
print(f"Occupation: {result.occupation}")
print(f"Location: {result.location}")
```

## Step 4: Token Management

Set up automatic token management:

```python
from revos import TokenManager
import asyncio

async def main():
    # Initialize token manager
    token_manager = TokenManager(refresh_interval_minutes=30)
    
    # Start background refresh service
    await token_manager.start_background_service()
    
    print("✅ Token management started")
    
    # Check token status
    print(f"Should refresh: {token_manager.should_refresh_token()}")
    print(f"Background service running: {token_manager.is_background_service_running()}")
    
    # Stop the service when done
    await token_manager.stop_background_service()

# Run the example
asyncio.run(main())
```

## Step 5: Complete Example

Here's a complete working example:

```python
#!/usr/bin/env python3
"""
Complete Revos Quick Start Example
"""

import asyncio
from pydantic import BaseModel
from revos import (
    LangChainExtractor,
    TokenManager,
    get_revos_token
)

# Define data models
class DocumentSummary(BaseModel):
    title: str
    summary: str
    key_points: list[str]
    confidence: float

class SentimentAnalysis(BaseModel):
    sentiment: str  # positive, negative, neutral
    confidence: float
    reasoning: str

async def main():
    print("🚀 Revos Quick Start Example")
    print("=" * 40)
    
    # Step 1: Test authentication
    print("\n1. Testing authentication...")
    try:
        token = get_revos_token()
        print(f"✅ Authentication successful: {token[:20]}...")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return
    
    # Step 2: Initialize extractor
    print("\n2. Initializing LLM extractor...")
    try:
        extractor = LangChainExtractor(model_name="gpt-4")
        print("✅ Extractor initialized successfully")
    except Exception as e:
        print(f"❌ Extractor initialization failed: {e}")
        return
    
    # Step 3: Document summarization
    print("\n3. Document summarization...")
    document_text = """
    Artificial Intelligence (AI) is transforming industries across the globe. 
    From healthcare to finance, AI technologies are enabling new possibilities 
    and improving efficiency. Machine learning algorithms can now process 
    vast amounts of data to identify patterns and make predictions with 
    unprecedented accuracy.
    """
    
    try:
        summary = extractor.extract_structured_data(
            prompt=f"Summarize this document: {document_text}",
            target_class=DocumentSummary
        )
        
        print(f"📄 Title: {summary.title}")
        print(f"📝 Summary: {summary.summary}")
        print(f"🎯 Key Points: {', '.join(summary.key_points)}")
        print(f"📊 Confidence: {summary.confidence:.2f}")
    except Exception as e:
        print(f"❌ Summarization failed: {e}")
    
    # Step 4: Sentiment analysis
    print("\n4. Sentiment analysis...")
    review_text = "This product is absolutely amazing! I love how easy it is to use and the results are fantastic."
    
    try:
        sentiment = extractor.extract_structured_data(
            prompt=f"Analyze the sentiment of this review: {review_text}",
            target_class=SentimentAnalysis
        )
        
        print(f"😊 Sentiment: {sentiment.sentiment}")
        print(f"📊 Confidence: {sentiment.confidence:.2f}")
        print(f"💭 Reasoning: {sentiment.reasoning}")
    except Exception as e:
        print(f"❌ Sentiment analysis failed: {e}")
    
    # Step 5: Token management
    print("\n5. Setting up token management...")
    try:
        token_manager = TokenManager(refresh_interval_minutes=30)
        await token_manager.start_background_service()
        
        print("✅ Background token management started")
        print(f"🔄 Service running: {token_manager.is_background_service_running()}")
        print(f"⏰ Last refresh: {token_manager.get_last_refresh_time()}")
        
        # Stop the service
        await token_manager.stop_background_service()
        print("🛑 Background service stopped")
    except Exception as e:
        print(f"❌ Token management failed: {e}")
    
    print("\n🎉 Quick start example completed!")

if __name__ == "__main__":
    asyncio.run(main())
```

## Running the Example

Save the code above to `quick_start.py` and run it:

```bash
python quick_start.py
```

Expected output:
```
🚀 Revos Quick Start Example
========================================

1. Testing authentication...
✅ Authentication successful: eyJhbGciOiJIUzI1NiIs...

2. Initializing LLM extractor...
✅ Extractor initialized successfully

3. Document summarization...
📄 Title: AI Transforming Industries
📝 Summary: Artificial Intelligence is revolutionizing various sectors...
🎯 Key Points: Healthcare transformation, Financial efficiency, Data processing
📊 Confidence: 0.95

4. Sentiment analysis...
😊 Sentiment: positive
📊 Confidence: 0.92
💭 Reasoning: The review contains positive language like "amazing" and "fantastic"

5. Setting up token management...
✅ Background token management started
🔄 Service running: True
⏰ Last refresh: 2024-01-15 10:30:00
🛑 Background service stopped

🎉 Quick start example completed!
```

## Next Steps

Now that you have Revos working:

1. [:octicons-arrow-right-24: **Configuration Guide**](configuration.md) – Learn advanced configuration options
2. [:octicons-arrow-right-24: **Authentication**](../user-guide/authentication.md) – Deep dive into authentication
3. [:octicons-arrow-right-24: **LLM Integration**](../user-guide/llm-integration.md) – Explore LLM capabilities
4. [:octicons-arrow-right-24: **FastAPI Integration**](../fastapi/basic-setup.md) – Build web applications

## Troubleshooting

### Common Issues

#### Authentication Errors
```python
# Check your credentials
import os
print(f"Client ID: {os.getenv('REVOS_CLIENT_ID')}")
print(f"Client Secret: {'*' * len(os.getenv('REVOS_CLIENT_SECRET', ''))}")
```

#### Import Errors
```python
# Verify installation
import revos
print(f"Revos version: {revos.__version__}")
```

#### Token Issues
```python
# Test token acquisition
from revos import get_revos_token
try:
    token = get_revos_token(force_refresh=True)
    print("✅ Token refresh successful")
except Exception as e:
    print(f"❌ Token refresh failed: {e}")
```

### Getting Help

If you encounter issues:

1. **Check the logs** for detailed error messages
2. **Verify environment variables** are set correctly
3. **Test with minimal example** to isolate the problem
4. **Check GitHub issues** for similar problems
5. **Create a new issue** if needed

## What's Next?

You're now ready to explore Revos in more detail:

- **Configuration**: Learn about advanced configuration options
- **Multiple Models**: Set up different LLM models
- **FastAPI**: Build web applications with Revos
- **Examples**: Explore more complex use cases
- **API Reference**: Complete API documentation
