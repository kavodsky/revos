#!/usr/bin/env python3
"""
Basic usage example for the Revos library.

This example demonstrates:
1. Setting up environment variables
2. Getting Apollo tokens
3. Using LangChain extractor for structured data extraction
4. Token management
"""

import asyncio
import os
from pydantic import BaseModel
from langchain_core.prompts import PromptTemplate

# Import the revo library
from revos import (
    RevosMainConfig,
    RevosConfig,
    LLMConfig,
    LoggingConfig,
    TokenManagerConfig,
    get_settings,
    load_config_from_file,
    RevosTokenManager,
        get_revos_token,
    LangChainExtractor,
    TokenManager
)


class PersonInfo(BaseModel):
    """Example data model for person information extraction."""
    name: str
    age: int
    occupation: str
    location: str


async def main():
    """Main example function."""
    print("Revos Library Basic Usage Example")
    print("=" * 40)
    
    # Check if environment variables are set
    required_vars = ["REVO_CLIENT_ID", "REVO_CLIENT_SECRET"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Warning: Missing environment variables: {missing_vars}")
        print("Please set the following environment variables:")
        for var in missing_vars:
            print(f"  export {var}='your_value_here'")
        print("\nContinuing with example (will show expected behavior)...")
    
    # 1. Basic token management
    print("\n1. Basic Token Management")
    print("-" * 25)
    
    try:
        # Get token using the global function
        token = get_revo_token()
        print(f"✓ Successfully obtained token: {token[:20]}...")
        
        # Create a custom token manager
        token_manager = RevosTokenManager()
        token2 = token_manager.get_token()
        print(f"✓ Custom token manager token: {token2[:20]}...")
        
    except Exception as e:
        print(f"✗ Token management failed: {e}")
    
    # 2. Configuration
    print("\n2. Configuration")
    print("-" * 15)
    
    # Get current settings
    settings = get_settings()
    print(f"✓ Revos Token URL: {settings.revos.token_url}")
    print(f"✓ Revos Base URL: {settings.revos.base_url}")
    print(f"✓ LLM Model: {settings.llm.model}")
    print(f"✓ LLM Temperature: {settings.llm.temperature}")
    print(f"✓ Token Buffer Minutes: {settings.revos.token_buffer_minutes}")
    print(f"✓ Refresh Interval: {settings.token_manager.refresh_interval_minutes} minutes")
    print(f"✓ Log Level: {settings.logging.level}")
    
    # Show how to create custom configuration
    print("\n3. Custom Configuration")
    print("-" * 22)
    
    # Create a custom configuration
    custom_config = RevosMainConfig(
        revo=RevosConfig(
            client_id="custom_client_id",
            client_secret="custom_client_secret",
            token_url="https://custom.example.com/token"
        ),
        llm=LLMConfig(
            model="gpt-4",
            temperature=0.2
        ),
        debug=True
    )
    
    print(f"✓ Custom Revos URL: {custom_config.revos.token_url}")
    print(f"✓ Custom LLM Model: {custom_config.llm.model}")
    print(f"✓ Debug Mode: {custom_config.debug}")
    
    # Show configuration summary
    print("\n4. Configuration Summary")
    print("-" * 25)
    print(f"  Revos API URL: {custom_config.revos.base_url}")
    print(f"  LLM Model: {custom_config.llm.model}")
    print(f"  Log Level: {custom_config.logging.level}")
    print(f"  Debug Mode: {custom_config.debug}")
    
    # 5. LangChain Extractor
    print("\n5. LangChain Extractor")
    print("-" * 22)
    
    try:
        # Create extractor
        extractor = LangChainExtractor()
        
        # Create a prompt template
        template = """
        Extract person information from the following text:
        {text}
        
        {format_instructions}
        """
        prompt = PromptTemplate(template=template, input_variables=["text"])
        
        # Example text to extract from
        text = "John Smith is 30 years old, works as a software engineer in San Francisco."
        
        # Extract structured data
        result = await extractor.extract(
            target=PersonInfo,
            prompt=prompt,
            text=text
        )
        
        print(f"✓ Extracted data:")
        print(f"  Name: {result.name}")
        print(f"  Age: {result.age}")
        print(f"  Occupation: {result.occupation}")
        print(f"  Location: {result.location}")
        
    except Exception as e:
        print(f"✗ Extraction failed: {e}")
        print("  This is expected if Revos credentials are not configured.")
    
    # 6. Token Manager with periodic refresh
    print("\n6. Token Manager")
    print("-" * 18)
    
    try:
        # Create token manager
        token_manager = TokenManager(refresh_interval_minutes=1)  # Short interval for demo
        
        # Check if refresh is needed
        needs_refresh = token_manager.should_refresh_token()
        print(f"✓ Token needs refresh: {needs_refresh}")
        
        # Attempt refresh
        refresh_success = token_manager.refresh_extractor()
        print(f"✓ Refresh successful: {refresh_success}")
        
    except Exception as e:
        print(f"✗ Token manager failed: {e}")
    
    print("\n" + "=" * 40)
    print("Example completed!")


if __name__ == "__main__":
    asyncio.run(main())
