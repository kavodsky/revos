# FastAPI Basic Setup

Learn how to integrate Revos with FastAPI applications using modern patterns and best practices.

## Prerequisites

Before starting, ensure you have:

- ✅ Revos installed and configured
- ✅ FastAPI and uvicorn installed
- ✅ Basic understanding of FastAPI

## Installation

Install the required dependencies:

```bash
pip install fastapi uvicorn revos
```

## Basic Integration

### 1. Simple FastAPI App

Create a basic FastAPI application with Revos:

```python
from fastapi import FastAPI, HTTPException
from revos import LangChainExtractor, get_revos_token, RevosTokenError
from contextlib import asynccontextmanager
from typing import Optional

# Global extractor instance
extractor: Optional[LangChainExtractor] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the Revos extractor on startup."""
    global extractor
    try:
        # Initialize with your preferred model
        extractor = LangChainExtractor(model_name="gpt-4")
        print("✅ Revos extractor initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize Revos extractor: {e}")
        raise
    
    yield
    
    # Cleanup (if needed)
    print("🔄 Revos extractor cleanup completed")

app = FastAPI(title="Revos FastAPI Integration", lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Revos FastAPI Integration"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    if extractor is None:
        raise HTTPException(status_code=503, detail="Revos extractor not initialized")
    
    try:
        # Test token availability
        token = get_revos_token()
        return {
            "status": "healthy",
            "revos_connected": True,
            "token_available": bool(token)
        }
    except RevosTokenError:
        return {
            "status": "degraded", 
            "revos_connected": False,
            "token_available": False
        }
```

### 2. Data Extraction Endpoint

Add structured data extraction:

```python
from pydantic import BaseModel

class DocumentSummary(BaseModel):
    title: str
    summary: str
    key_points: list[str]
    confidence: float

@app.post("/summarize")
async def summarize_document(text: str):
    """Summarize a document using Revos."""
    if extractor is None:
        raise HTTPException(status_code=503, detail="Extractor not initialized")
    
    try:
        result = extractor.extract_structured_data(
            prompt=f"Summarize this document: {text}",
            target_class=DocumentSummary
        )
        return {"summary": result.dict()}
    except RevosTokenError:
        raise HTTPException(status_code=401, detail="Authentication failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")
```

## Running the Application

### Development Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Testing the API

### Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "revos_connected": true,
  "token_available": true
}
```

### Document Summarization

```bash
curl -X POST "http://localhost:8000/summarize" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your document text here..."}'
```

Response:
```json
{
  "summary": {
    "title": "Document Title",
    "summary": "Brief summary...",
    "key_points": ["Point 1", "Point 2"],
    "confidence": 0.95
  }
}
```

## Complete Example

Here's a complete FastAPI application:

```python
#!/usr/bin/env python3
"""
Complete FastAPI + Revos Integration Example
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from revos import (
    LangChainExtractor, 
    TokenManager,
    get_revos_token,
    RevosTokenError
)
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing import Optional, List
import asyncio

# Data models
class DocumentSummary(BaseModel):
    title: str
    summary: str
    key_points: List[str]
    confidence: float

class SentimentAnalysis(BaseModel):
    sentiment: str  # positive, negative, neutral
    confidence: float
    reasoning: str

class TextAnalysis(BaseModel):
    language: str
    word_count: int
    readability_score: float
    topics: List[str]

# Global instances
token_manager: Optional[TokenManager] = None
extractor: Optional[LangChainExtractor] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    global token_manager, extractor
    
    # Startup
    try:
        # Initialize token manager with background refresh
        token_manager = TokenManager(refresh_interval_minutes=30)
        
        # Start background token refresh service
        await token_manager.start_background_service()
        
        # Initialize extractor
        extractor = LangChainExtractor(model_name="gpt-4")
        
        print("✅ Revos services started successfully")
        
    except Exception as e:
        print(f"❌ Failed to start Revos services: {e}")
        raise
    
    yield
    
    # Shutdown
    if token_manager:
        await token_manager.stop_background_service()
        print("✅ Revos services stopped")

app = FastAPI(
    title="Revos FastAPI Integration",
    description="FastAPI application with Revos LLM integration",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {
        "message": "Revos FastAPI Integration", 
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Comprehensive health check."""
    try:
        token = get_revos_token()
        return {
            "status": "healthy",
            "revos_connected": True,
            "token_available": bool(token),
            "background_service_running": token_manager.is_background_service_running() if token_manager else False,
            "extractor_ready": extractor is not None
        }
    except Exception:
        return {
            "status": "degraded",
            "revos_connected": False,
            "token_available": False,
            "background_service_running": False,
            "extractor_ready": False
        }

@app.post("/summarize")
async def summarize_document(
    text: str,
    background_tasks: BackgroundTasks
):
    """Summarize a document using Revos."""
    if extractor is None:
        raise HTTPException(status_code=503, detail="Extractor not initialized")
    
    try:
        result = extractor.extract_structured_data(
            prompt=f"Summarize this document: {text}",
            target_class=DocumentSummary
        )
        
        # Log the operation in background
        background_tasks.add_task(log_operation, "summarize", len(text))
        
        return {"summary": result.dict()}
    except RevosTokenError:
        raise HTTPException(status_code=401, detail="Authentication failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")

@app.post("/analyze-sentiment")
async def analyze_sentiment(text: str):
    """Analyze sentiment of text using Revos."""
    if extractor is None:
        raise HTTPException(status_code=503, detail="Extractor not initialized")
    
    try:
        result = extractor.extract_structured_data(
            prompt=f"Analyze the sentiment of this text: {text}",
            target_class=SentimentAnalysis
        )
        return {"analysis": result.dict()}
    except RevosTokenError:
        raise HTTPException(status_code=401, detail="Authentication failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")

@app.post("/analyze-text")
async def analyze_text(text: str):
    """Perform comprehensive text analysis."""
    if extractor is None:
        raise HTTPException(status_code=503, detail="Extractor not initialized")
    
    try:
        result = extractor.extract_structured_data(
            prompt=f"Analyze this text comprehensively: {text}",
            target_class=TextAnalysis
        )
        return {"analysis": result.dict()}
    except RevosTokenError:
        raise HTTPException(status_code=401, detail="Authentication failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")

@app.get("/token-status")
async def get_token_status():
    """Get current token status and refresh information."""
    if not token_manager:
        raise HTTPException(status_code=503, detail="Token manager not initialized")
    
    return {
        "background_service_running": token_manager.is_background_service_running(),
        "last_refresh_time": token_manager.get_last_refresh_time(),
        "should_refresh": token_manager.should_refresh_token(),
        "current_token_available": bool(get_revos_token())
    }

@app.post("/force-refresh")
async def force_token_refresh():
    """Force a token refresh."""
    if not token_manager:
        raise HTTPException(status_code=503, detail="Token manager not initialized")
    
    success = token_manager.force_refresh()
    return {"refresh_successful": success}

async def log_operation(operation: str, data_size: int):
    """Background task to log operations."""
    print(f"Operation '{operation}' completed on {data_size} characters")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Environment Configuration

Create a `.env` file for your FastAPI app:

```bash
# .env
REVOS_CLIENT_ID=your_client_id
REVOS_CLIENT_SECRET=your_client_secret
REVOS_TOKEN_URL=https://your-site.com/revo/oauth/token
REVOS_BASE_URL=https://your-site.com/revo/llm-api

# LLM Configuration
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=1000

# Token Management
TOKEN_MANAGER_REFRESH_INTERVAL_MINUTES=30
TOKEN_MANAGER_MAX_FAILURES_BEFORE_FALLBACK=3
```

## API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Next Steps

Now that you have a basic FastAPI + Revos setup:

1. [:octicons-arrow-right-24: **Advanced Patterns**](advanced-patterns.md) – Learn dependency injection and advanced patterns
2. [:octicons-arrow-right-24: **Error Handling**](error-handling.md) – Implement comprehensive error handling
3. [:octicons-arrow-right-24: **Complete Example**](complete-example.md) – See a production-ready application

## Key Benefits

- **🔄 Automatic Token Management**: Background refresh keeps tokens valid
- **🛡️ Error Handling**: Proper HTTP status codes for different error types
- **⚡ Background Tasks**: Non-blocking operations
- **📊 Health Monitoring**: Endpoints to check system status
- **🔒 Thread Safety**: Safe for concurrent requests
- **📚 Modern FastAPI**: Uses `lifespan` instead of deprecated `on_event`
