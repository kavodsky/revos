#!/usr/bin/env python3
"""
Simple RUMBA_ Prefix Example

This example demonstrates how to use Revos with a custom RUMBA_ prefix
instead of the default REVOS_ prefix.
"""

import os
from revos import create_config_with_prefixes

def main():
    """Simple RUMBA_ prefix example."""
    print("🎵 Simple RUMBA_ Prefix Example")
    print("=" * 50)
    
    # Set environment variables with RUMBA_ prefix
    os.environ.update({
        "RUMBA_CLIENT_ID": "your_rumba_client_id",
        "RUMBA_CLIENT_SECRET": "your_rumba_client_secret",
        "RUMBA_TOKEN_URL": "https://your-site.com/revo/oauth/token",
        "RUMBA_BASE_URL": "https://your-site.com/revo/llm-api",
        "RUMBA_LLM_MODEL": "gpt-4",
        "RUMBA_LLM_TEMPERATURE": "0.1",
        "RUMBA_LLM_MAX_TOKENS": "1000",
        "RUMBA_TOKEN_MANAGER_REFRESH_INTERVAL_MINUTES": "45",
        "RUMBA_LOGGING_LEVEL": "INFO"
    })
    
    # Create configuration with custom RUMBA_ prefix
    config = create_config_with_prefixes(
        revo_prefix="RUMBA_",  # Use RUMBA_ prefix instead of REVOS_
        llm_prefix="RUMBA_LLM_",  # Use RUMBA_LLM_ prefix for LLM settings
        logging_prefix="RUMBA_LOG_",  # Use RUMBA_LOG_ prefix for logging
        token_prefix="RUMBA_TOKEN_"  # Use RUMBA_TOKEN_ prefix for token management
    )
    
    print("✅ Configuration created with RUMBA_ prefix")
    print(f"📊 Client ID: {config.revo.client_id}")
    print(f"🔗 Token URL: {config.revo.token_url}")
    print(f"🌐 Base URL: {config.revo.base_url}")
    print(f"🤖 LLM Model: {config.llm.model}")
    print(f"🌡️  Temperature: {config.llm.temperature}")
    print(f"📝 Max Tokens: {config.llm.max_tokens}")
    print(f"🔄 Refresh Interval: {config.token_manager.refresh_interval_minutes} minutes")
    print(f"📝 Logging Level: {config.logging.level}")
    print()
    
    print("🎉 RUMBA_ prefix example completed successfully!")
    print()
    print("💡 Key Benefits of RUMBA_ Prefix:")
    print("  🎵 Avoid conflicts with other libraries")
    print("  🏗️  Maintain consistent naming conventions")
    print("  🌍 Support multiple environments")
    print("  🐳 Easy integration with Docker/Kubernetes")
    print("  🔒 Better security with environment-specific configs")

if __name__ == "__main__":
    main()
