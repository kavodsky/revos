#!/usr/bin/env python3
"""
FastAPI Example with RUMBA_ Prefix

This example demonstrates how to integrate Revos with FastAPI using
a custom RUMBA_ prefix loaded from a .env file.

Features:
- Custom RUMBA_ prefix configuration
- Environment variables from .env file
- FastAPI lifespan management
- Background token management
- Error handling and health checks
- Multiple endpoints with different LLM models
"""

import os
import asyncio
from typing import Optional, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from revos import (
    create_config_with_prefixes,
    LangChainExtractor,
    TokenManager,
    get_revos_token,
    RevosTokenError,
    RevosAuthenticationError,
    RevosAPIError
)

# Data models for API endpoints
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

class RumbaConfig:
    """Configuration class for RUMBA_ prefix settings."""
    
    def __init__(self):
        # Load environment variables from .env file
        self.load_env_file()
        
        # Create Revos configuration with RUMBA_ prefix
        self.revos_config = create_config_with_prefixes(
            revo_prefix="RUMBA_",  # Use RUMBA_ prefix instead of REVOS_
            llm_prefix="RUMBA_LLM_",  # Use RUMBA_LLM_ prefix for LLM settings
            logging_prefix="RUMBA_LOG_",  # Use RUMBA_LOG_ prefix for logging
            token_prefix="RUMBA_TOKEN_"  # Use RUMBA_TOKEN_ prefix for token management
        )
        
        print("🎵 RUMBA_ prefix configuration loaded successfully")
        print(f"📊 Client ID: {self.revos_config.revo.client_id}")
        print(f"🔗 Token URL: {self.revos_config.revo.token_url}")
        print(f"🌐 Base URL: {self.revos_config.revo.base_url}")
        print(f"🤖 LLM Model: {self.revos_config.llm.model}")
        print(f"🌡️  Temperature: {self.revos_config.llm.temperature}")
        print(f"📝 Max Tokens: {self.revos_config.llm.max_tokens}")
        print(f"🔄 Refresh Interval: {self.revos_config.token_manager.refresh_interval_minutes} minutes")
        print(f"📝 Logging Level: {self.revos_config.logging.level}")
    
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
            
        # Also try to load from examples/.env if we're running from the examples directory
        examples_env_file = "examples/.env"
        if os.path.exists(examples_env_file):
            print(f"📁 Also loading environment variables from {examples_env_file}")
            load_dotenv(examples_env_file, override=False)  # Don't override existing vars
            print(f"✅ Additional environment variables loaded from {examples_env_file}")

# Global instances
rumba_config: Optional[RumbaConfig] = None
token_manager: Optional[TokenManager] = None
extractor: Optional[LangChainExtractor] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management with RUMBA_ prefix configuration."""
    global rumba_config, token_manager, extractor
    
    print("🚀 Starting RUMBA FastAPI application...")
    
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
        print(f"🎵 Using RUMBA_ prefix configuration")
        print(f"🤖 LLM Model: {extractor.get_current_model()}")
        print(f"🔄 Background token service: {token_manager.is_background_service_running()}")
        
    except Exception as e:
        print(f"❌ Failed to start RUMBA FastAPI services: {e}")
        raise
    
    yield
    
    # Shutdown
    print("🛑 Shutting down RUMBA FastAPI services...")
    if token_manager:
        await token_manager.stop_background_service()
        print("✅ Background token service stopped")
    print("✅ RUMBA FastAPI services shutdown completed")

# Create FastAPI app with lifespan
app = FastAPI(
    title="RUMBA FastAPI Integration",
    description="FastAPI application with Revos LLM integration using RUMBA_ prefix",
    version="1.0.0",
    lifespan=lifespan
)

# Exception handlers for RUMBA-specific errors
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

@app.exception_handler(RevosAuthenticationError)
async def rumba_auth_error_handler(request, exc: RevosAuthenticationError):
    """Handle RUMBA authentication errors."""
    return JSONResponse(
        status_code=401,
        content={
            "error": "RUMBA Authentication Error",
            "message": str(exc),
            "type": "RUMBA_AUTH_ERROR",
            "prefix": "RUMBA_"
        }
    )

@app.exception_handler(RevosAPIError)
async def rumba_api_error_handler(request, exc: RevosAPIError):
    """Handle RUMBA API errors."""
    return JSONResponse(
        status_code=502,
        content={
            "error": "RUMBA API Error",
            "message": str(exc),
            "type": "RUMBA_API_ERROR",
            "prefix": "RUMBA_"
        }
    )

# Dependency to get RUMBA configuration
def get_rumba_config() -> RumbaConfig:
    """Dependency to get RUMBA configuration."""
    if rumba_config is None:
        raise HTTPException(status_code=503, detail="RUMBA configuration not initialized")
    return rumba_config

# Dependency to get RUMBA extractor
def get_rumba_extractor() -> LangChainExtractor:
    """Dependency to get RUMBA extractor."""
    if extractor is None:
        raise HTTPException(status_code=503, detail="RUMBA extractor not initialized")
    return extractor

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with RUMBA information."""
    return {
        "message": "RUMBA FastAPI Integration",
        "status": "running",
        "version": "1.0.0",
        "prefix": "RUMBA_",
        "description": "FastAPI application with Revos LLM integration using custom RUMBA_ prefix"
    }

@app.get("/health")
async def health_check():
    """Comprehensive health check for RUMBA services."""
    try:
        token = get_revos_token()
        return {
            "status": "healthy",
            "rumba_connected": True,
            "token_available": bool(token),
            "background_service_running": token_manager.is_background_service_running() if token_manager else False,
            "extractor_ready": extractor is not None,
            "prefix": "RUMBA_",
            "model": extractor.get_current_model() if extractor else None
        }
    except Exception:
        return {
            "status": "degraded",
            "rumba_connected": False,
            "token_available": False,
            "background_service_running": False,
            "extractor_ready": False,
            "prefix": "RUMBA_"
        }

@app.get("/config")
async def get_rumba_config_info(config: RumbaConfig = Depends(get_rumba_config)):
    """Get RUMBA configuration information."""
    return {
        "prefix": "RUMBA_",
        "client_id": config.revos_config.revo.client_id,
        "token_url": config.revos_config.revo.token_url,
        "base_url": config.revos_config.revo.base_url,
        "llm_model": config.revos_config.llm.model,
        "llm_temperature": config.revos_config.llm.temperature,
        "llm_max_tokens": config.revos_config.llm.max_tokens,
        "refresh_interval_minutes": config.revos_config.token_manager.refresh_interval_minutes,
        "logging_level": config.revos_config.logging.level
    }

@app.post("/summarize")
async def summarize_document(
    text: str,
    background_tasks: BackgroundTasks,
    rumba_extractor: LangChainExtractor = Depends(get_rumba_extractor)
):
    """Summarize a document using RUMBA LLM integration."""
    try:
        result = rumba_extractor.extract_structured_data(
            prompt=f"Summarize this document: {text}",
            target_class=DocumentSummary
        )
        
        # Log the operation in background
        background_tasks.add_task(log_rumba_operation, "summarize", len(text))
        
        return {
            "summary": result.dict(),
            "prefix": "RUMBA_",
            "model": rumba_extractor.get_current_model()
        }
    except RevosTokenError:
        raise HTTPException(status_code=401, detail="RUMBA authentication failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RUMBA processing failed: {e}")

@app.post("/analyze-sentiment")
async def analyze_sentiment(
    text: str,
    rumba_extractor: LangChainExtractor = Depends(get_rumba_extractor)
):
    """Analyze sentiment of text using RUMBA LLM integration."""
    try:
        result = rumba_extractor.extract_structured_data(
            prompt=f"Analyze the sentiment of this text: {text}",
            target_class=SentimentAnalysis
        )
        return {
            "analysis": result.dict(),
            "prefix": "RUMBA_",
            "model": rumba_extractor.get_current_model()
        }
    except RevosTokenError:
        raise HTTPException(status_code=401, detail="RUMBA authentication failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RUMBA analysis failed: {e}")

@app.post("/analyze-text")
async def analyze_text(
    text: str,
    rumba_extractor: LangChainExtractor = Depends(get_rumba_extractor)
):
    """Perform comprehensive text analysis using RUMBA LLM integration."""
    try:
        result = rumba_extractor.extract_structured_data(
            prompt=f"Analyze this text comprehensively: {text}",
            target_class=TextAnalysis
        )
        return {
            "analysis": result.dict(),
            "prefix": "RUMBA_",
            "model": rumba_extractor.get_current_model()
        }
    except RevosTokenError:
        raise HTTPException(status_code=401, detail="RUMBA authentication failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RUMBA analysis failed: {e}")

@app.get("/token-status")
async def get_rumba_token_status():
    """Get current RUMBA token status and refresh information."""
    if not token_manager:
        raise HTTPException(status_code=503, detail="RUMBA token manager not initialized")
    
    return {
        "prefix": "RUMBA_",
        "background_service_running": token_manager.is_background_service_running(),
        "last_refresh_time": token_manager.get_last_refresh_time(),
        "should_refresh": token_manager.should_refresh_token(),
        "current_token_available": bool(get_revos_token())
    }

@app.post("/force-refresh")
async def force_rumba_token_refresh():
    """Force a RUMBA token refresh."""
    if not token_manager:
        raise HTTPException(status_code=503, detail="RUMBA token manager not initialized")
    
    success = token_manager.force_refresh()
    return {
        "refresh_successful": success,
        "prefix": "RUMBA_",
        "message": "RUMBA token refresh completed" if success else "RUMBA token refresh failed"
    }

# Background task functions
async def log_rumba_operation(operation: str, data_size: int):
    """Background task to log RUMBA operations."""
    print(f"🎵 RUMBA operation '{operation}' completed on {data_size} characters")

# Main function for running the application
def main():
    """Main function to run the RUMBA FastAPI application."""
    print("🎵 Starting RUMBA FastAPI application...")
    print("=" * 60)
    print("This application uses RUMBA_ prefix for all configuration")
    print("Make sure to set RUMBA_ environment variables in your .env file")
    print("=" * 60)
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
