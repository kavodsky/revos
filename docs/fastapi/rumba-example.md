# FastAPI with RUMBA_ Prefix

Learn how to integrate Revos with FastAPI using a custom RUMBA_ prefix loaded from a `.env` file.

## Overview

This example demonstrates a complete FastAPI application that uses Revos with a custom RUMBA_ prefix for all configuration. The application loads environment variables from a `.env` file using `python-dotenv` and provides multiple endpoints for LLM-powered text analysis.

## Features

- **🎵 Custom RUMBA_ Prefix**: All configuration uses RUMBA_ prefix instead of default REVOS_
- **📁 .env File Support**: Loads configuration from `.env` file using `python-dotenv`
- **🔄 Background Token Management**: Automatic token refresh with configurable intervals
- **🛡️ Error Handling**: Comprehensive error handling with custom exception handlers
- **📊 Health Monitoring**: Multiple endpoints to check system status
- **⚡ Background Tasks**: Non-blocking operations for logging and monitoring
- **🔒 Dependency Injection**: Clean separation of concerns with FastAPI dependencies

## Setup

### 1. Install Dependencies

```bash
pip install fastapi uvicorn python-dotenv revos
```

### 2. Create .env File

Create a `.env` file in your project root:

```bash
# Copy the example file
cp examples/env.rumba.example .env

# Edit with your actual values
nano .env
```

### 3. Configure RUMBA_ Environment Variables

```bash
# .env
# Required RUMBA credentials
RUMBA_CLIENT_ID=your_rumba_client_id
RUMBA_CLIENT_SECRET=your_rumba_client_secret

# RUMBA API endpoints
RUMBA_TOKEN_URL=https://your-site.com/revo/oauth/token
RUMBA_BASE_URL=https://your-site.com/revo/llm-api

# RUMBA LLM configuration
RUMBA_LLM_MODEL=gpt-4
RUMBA_LLM_TEMPERATURE=0.1
RUMBA_LLM_MAX_TOKENS=1000

# RUMBA token manager settings
RUMBA_TOKEN_MANAGER_REFRESH_INTERVAL_MINUTES=45
RUMBA_TOKEN_MANAGER_MAX_FAILURES_BEFORE_FALLBACK=3
RUMBA_TOKEN_MANAGER_ENABLE_PERIODIC_REFRESH=true
RUMBA_TOKEN_MANAGER_ENABLE_FALLBACK=true

# RUMBA logging configuration
RUMBA_LOGGING_LEVEL=INFO
RUMBA_LOGGING_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

## Running the Application

### Development Server

```bash
# Run the FastAPI server
python examples/fastapi_rumba_example.py

# Or with uvicorn directly
uvicorn examples.fastapi_rumba_example:app --reload --host 0.0.0.0 --port 8000
```

### Production Server

```bash
uvicorn examples.fastapi_rumba_example:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Root Endpoint

```bash
GET /
```

Returns basic information about the RUMBA FastAPI application.

**Response:**
```json
{
  "message": "RUMBA FastAPI Integration",
  "status": "running",
  "version": "1.0.0",
  "prefix": "RUMBA_",
  "description": "FastAPI application with Revos LLM integration using custom RUMBA_ prefix"
}
```

### Health Check

```bash
GET /health
```

Comprehensive health check for RUMBA services.

**Response:**
```json
{
  "status": "healthy",
  "rumba_connected": true,
  "token_available": true,
  "background_service_running": true,
  "extractor_ready": true,
  "prefix": "RUMBA_",
  "model": "gpt-4"
}
```

### Configuration Information

```bash
GET /config
```

Get RUMBA configuration information.

**Response:**
```json
{
  "prefix": "RUMBA_",
  "client_id": "your_rumba_client_id",
  "token_url": "https://your-site.com/revo/oauth/token",
  "base_url": "https://your-site.com/revo/llm-api",
  "llm_model": "gpt-4",
  "llm_temperature": 0.1,
  "llm_max_tokens": 1000,
  "refresh_interval_minutes": 45,
  "logging_level": "INFO"
}
```

### Document Summarization

```bash
POST /summarize
```

Summarize a document using RUMBA LLM integration.

**Request:**
```json
{
  "text": "Your document text here..."
}
```

**Response:**
```json
{
  "summary": {
    "title": "Document Title",
    "summary": "Brief summary...",
    "key_points": ["Point 1", "Point 2"],
    "confidence": 0.95
  },
  "prefix": "RUMBA_",
  "model": "gpt-4"
}
```

### Sentiment Analysis

```bash
POST /analyze-sentiment
```

Analyze sentiment of text using RUMBA LLM integration.

**Request:**
```json
{
  "text": "This product is amazing!"
}
```

**Response:**
```json
{
  "analysis": {
    "sentiment": "positive",
    "confidence": 0.92,
    "reasoning": "The text contains positive language..."
  },
  "prefix": "RUMBA_",
  "model": "gpt-4"
}
```

### Text Analysis

```bash
POST /analyze-text
```

Perform comprehensive text analysis using RUMBA LLM integration.

**Request:**
```json
{
  "text": "Your text to analyze..."
}
```

**Response:**
```json
{
  "analysis": {
    "language": "en",
    "word_count": 150,
    "readability_score": 8.5,
    "topics": ["technology", "innovation"]
  },
  "prefix": "RUMBA_",
  "model": "gpt-4"
}
```

### Token Status

```bash
GET /token-status
```

Get current RUMBA token status and refresh information.

**Response:**
```json
{
  "prefix": "RUMBA_",
  "background_service_running": true,
  "last_refresh_time": "2024-01-15T10:30:00",
  "should_refresh": false,
  "current_token_available": true
}
```

### Force Token Refresh

```bash
POST /force-refresh
```

Force a RUMBA token refresh.

**Response:**
```json
{
  "refresh_successful": true,
  "prefix": "RUMBA_",
  "message": "RUMBA token refresh completed"
}
```

## Testing the Application

### Using the Test Script

```bash
# Run the test script
python examples/test_fastapi_rumba.py
```

### Manual Testing with curl

```bash
# Test root endpoint
curl http://localhost:8000/

# Test health check
curl http://localhost:8000/health

# Test document summarization
curl -X POST "http://localhost:8000/summarize" \
     -H "Content-Type: application/json" \
     -d '{"text": "Your document text here..."}'

# Test sentiment analysis
curl -X POST "http://localhost:8000/analyze-sentiment" \
     -H "Content-Type: application/json" \
     -d '{"text": "This product is amazing!"}'
```

### Using the Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Key Features Explained

### RUMBA_ Prefix Configuration

```python
# Create Revos configuration with RUMBA_ prefix
self.revos_config = create_config_with_prefixes(
    revo_prefix="RUMBA_",  # Use RUMBA_ prefix instead of REVOS_
    llm_prefix="RUMBA_LLM_",  # Use RUMBA_LLM_ prefix for LLM settings
    logging_prefix="RUMBA_LOG_",  # Use RUMBA_LOG_ prefix for logging
    token_prefix="RUMBA_TOKEN_"  # Use RUMBA_TOKEN_ prefix for token management
)
```

### Environment Variable Loading with python-dotenv

```python
def load_env_file(self):
    """Load environment variables from .env file using python-dotenv."""
    env_file = ".env"
    
    # Try to load from .env file
    if os.path.exists(env_file):
        print(f"📁 Loading environment variables from {env_file}")
        load_dotenv(env_file, override=True)  # override=True to override existing env vars
        print(f"✅ Environment variables loaded from {env_file}")
    else:
        print(f"⚠️  {env_file} file not found, using system environment variables")
```

### FastAPI Lifespan Management

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management with RUMBA_ prefix configuration."""
    global rumba_config, token_manager, extractor
    
    # Startup
    try:
        # Initialize RUMBA configuration
        rumba_config = RumbaConfig()
        
        # Initialize token manager with background refresh
        token_manager = TokenManager(
            refresh_interval_minutes=rumba_config.revos_config.token_manager.refresh_interval_minutes
        )
        
        # Start background token refresh service
        await token_manager.start_background_service()
        
        # Initialize extractor with RUMBA configuration
        extractor = LangChainExtractor(
            model_name=rumba_config.revos_config.llm.model,
            settings_instance=rumba_config.revos_config
        )
        
        print("✅ RUMBA FastAPI services started successfully")
        
    except Exception as e:
        print(f"❌ Failed to start RUMBA FastAPI services: {e}")
        raise
    
    yield
    
    # Shutdown
    if token_manager:
        await token_manager.stop_background_service()
```

### Custom Exception Handlers

```python
@app.exception_handler(RevosTokenError)
async def rumba_token_error_handler(request, exc: RevosTokenError):
    """Handle RUMBA token errors."""
    return JSONResponse(
        status_code=401,
        content={
            "error": "RUMBA Token Error",
            "message": str(exc),
            "type": "RUMBA_TOKEN_ERROR",
            "prefix": "RUMBA_"
        }
    )
```

## Docker Integration

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Set default RUMBA_ environment variables
ENV RUMBA_LLM_MODEL=gpt-4
ENV RUMBA_LLM_TEMPERATURE=0.1
ENV RUMBA_LOGGING_LEVEL=INFO

CMD ["python", "examples/fastapi_rumba_example.py"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  rumba-fastapi:
    build: .
    ports:
      - "8000:8000"
    environment:
      - RUMBA_CLIENT_ID=your_rumba_client_id
      - RUMBA_CLIENT_SECRET=your_rumba_client_secret
      - RUMBA_TOKEN_URL=https://your-site.com/revo/oauth/token
      - RUMBA_BASE_URL=https://your-site.com/revo/llm-api
      - RUMBA_LLM_MODEL=gpt-4
      - RUMBA_LLM_TEMPERATURE=0.1
      - RUMBA_LLM_MAX_TOKENS=1000
      - RUMBA_TOKEN_MANAGER_REFRESH_INTERVAL_MINUTES=45
      - RUMBA_LOGGING_LEVEL=INFO
    volumes:
      - ./.env:/app/.env
```

## Kubernetes Integration

### ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: rumba-config
data:
  RUMBA_CLIENT_ID: "your_rumba_client_id"
  RUMBA_CLIENT_SECRET: "your_rumba_client_secret"
  RUMBA_TOKEN_URL: "https://your-site.com/revo/oauth/token"
  RUMBA_BASE_URL: "https://your-site.com/revo/llm-api"
  RUMBA_LLM_MODEL: "gpt-4"
  RUMBA_LLM_TEMPERATURE: "0.1"
  RUMBA_LLM_MAX_TOKENS: "1000"
  RUMBA_TOKEN_MANAGER_REFRESH_INTERVAL_MINUTES: "45"
  RUMBA_LOGGING_LEVEL: "INFO"
```

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rumba-fastapi
spec:
  replicas: 3
  selector:
    matchLabels:
      app: rumba-fastapi
  template:
    metadata:
      labels:
        app: rumba-fastapi
    spec:
      containers:
      - name: rumba-fastapi
        image: your-registry/rumba-fastapi:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: rumba-config
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Troubleshooting

### Common Issues

#### 1. Environment Variables Not Loaded

```bash
# Check if .env file exists
ls -la .env

# Check if python-dotenv is installed
pip list | grep python-dotenv

# Verify environment variables are set
python -c "import os; print('RUMBA_CLIENT_ID:', os.getenv('RUMBA_CLIENT_ID'))"
```

#### 2. FastAPI Server Not Starting

```bash
# Check for import errors
python -c "from examples.fastapi_rumba_example import app"

# Check for configuration errors
python -c "from examples.fastapi_rumba_example import RumbaConfig; RumbaConfig()"
```

#### 3. Token Authentication Issues

```bash
# Test token acquisition
python -c "from revos import get_revos_token; print(get_revos_token())"

# Check token status endpoint
curl http://localhost:8000/token-status
```

### Debug Mode

Enable debug mode by setting the logging level:

```bash
# In your .env file
RUMBA_LOGGING_LEVEL=DEBUG
```

## Next Steps

Now that you have a working FastAPI application with RUMBA_ prefix:

1. [:octicons-arrow-right-24: **Custom Prefixes**](../examples/custom-prefixes.md) – Learn more about custom prefixes
2. [:octicons-arrow-right-24: **Basic Setup**](basic-setup.md) – Explore other FastAPI integration patterns
3. [:octicons-arrow-right-24: **Configuration**](../getting-started/configuration.md) – Learn about advanced configuration options

## Complete Example Files

- [`examples/fastapi_rumba_example.py`](../../examples/fastapi_rumba_example.py) - Complete FastAPI application
- [`examples/test_fastapi_rumba.py`](../../examples/test_fastapi_rumba.py) - Test script for the application
- [`examples/env.rumba.example`](../../examples/env.rumba.example) - Example environment file
