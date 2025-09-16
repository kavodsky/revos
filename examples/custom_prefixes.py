#!/usr/bin/env python3
"""
Example: Using custom environment variable prefixes with the Revos library.

This example demonstrates how to configure the Revos library to use
custom environment variable prefixes instead of the default ones.
"""

import os
from revos import create_config_with_prefixes, RevosTokenManager


def example_custom_prefixes():
    """Example: Using custom environment variable prefixes."""
    print("Custom Environment Variable Prefixes Example")
    print("=" * 50)
    print("This example shows how to use custom prefixes like RUMBA_ instead of REVOS_")
    print()
    
    # Set custom environment variables with different prefixes
    os.environ.update({
        # RUMBA_ prefix example (as requested by user)
        "RUMBA_CLIENT_ID": "your_rumba_client_id",
        "RUMBA_CLIENT_SECRET": "your_rumba_client_secret",
        "RUMBA_TOKEN_URL": "https://your-site.com/revo/oauth/token",
        "RUMBA_BASE_URL": "https://your-site.com/revo/llm-api",
        "RUMBA_LLM_MODEL": "gpt-4",
        "RUMBA_LLM_TEMPERATURE": "0.1",
        "RUMBA_LLM_MAX_TOKENS": "1000",
        
        # Custom API prefix
        "MY_API_CLIENT_ID": "your-custom-client-id",
        "MY_API_CLIENT_SECRET": "your-custom-client-secret",
        "MY_API_TOKEN_URL": "https://your-custom-site.com/oauth/token",
        "MY_API_BASE_URL": "https://your-custom-site.com/api",
        
        # Custom LLM prefix
        "AI_MODEL": "gpt-4",
        "AI_TEMPERATURE": "0.7",
        "AI_MAX_TOKENS": "1000",
        
        # Custom logging prefix
        "APP_LOG_LEVEL": "INFO",
        "APP_LOG_FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        
        # Custom token prefix
        "AUTH_REFRESH_INTERVAL_MINUTES": "30",
        "AUTH_ENABLE_FALLBACK": "true",
    })
    
    # Example 1: RUMBA_ prefix configuration (as requested by user)
    print("🎵 Example 1: RUMBA_ Prefix Configuration")
    print("-" * 40)
    
    rumba_config = create_config_with_prefixes(
        revo_prefix="RUMBA_",  # Use RUMBA_ prefix instead of REVOS_
        llm_prefix="RUMBA_LLM_",  # Use RUMBA_LLM_ prefix for LLM settings
        logging_prefix="RUMBA_LOG_",  # Use RUMBA_LOG_ prefix for logging
        token_prefix="RUMBA_TOKEN_"  # Use RUMBA_TOKEN_ prefix for token management
    )
    
    print("✓ RUMBA_ prefix configuration created")
    print(f"  🎵 RUMBA Client ID: {rumba_config.revo.client_id}")
    print(f"  🎵 RUMBA Base URL: {rumba_config.revo.base_url}")
    print(f"  🤖 RUMBA LLM Model: {rumba_config.llm.model}")
    print(f"  🌡️  RUMBA Temperature: {rumba_config.llm.temperature}")
    print()
    
    # Example 2: Multiple custom prefixes
    print("🔧 Example 2: Multiple Custom Prefixes")
    print("-" * 40)
    
    config = create_config_with_prefixes(
        revo_prefix="MY_API_",  # Use MY_API_ prefix instead of REVOS_
        llm_prefix="AI_",  # Use AI_ prefix for LLM settings
        logging_prefix="APP_",  # Use APP_ prefix for logging
        token_prefix="AUTH_"  # Use AUTH_ prefix for token management
    )
    
    print("✓ Configuration created with custom prefixes")
    print(f"  🔧 API Client ID: {config.revo.client_id}")
    print(f"  🔧 API Base URL: {config.revo.base_url}")
    print(f"  🤖 LLM Model: {config.llm.model}")
    print(f"  🌡️  LLM Temperature: {config.llm.temperature}")
    print(f"  📝 Log Level: {config.logging.level}")
    print(f"  🔄 Token Refresh Interval: {config.token_manager.refresh_interval_minutes}")
    print(f"  🛡️  Enable Fallback: {config.token_manager.enable_fallback}")
    
    return config


def example_mixed_prefixes():
    """Example: Using different prefixes for different components."""
    print("\nMixed Prefixes Example")
    print("=" * 25)
    
    # Set environment variables with mixed prefixes
    os.environ.update({
        # Keep default Revos prefix
        "REVO_CLIENT_ID": "default-revo-client-id",
        "REVO_CLIENT_SECRET": "default-revo-client-secret",
        
        # Use custom LLM prefix
        "CUSTOM_AI_MODEL": "gpt-3.5-turbo",
        "CUSTOM_AI_TEMPERATURE": "0.5",
        
        # Use custom logging prefix
        "MY_APP_LOG_LEVEL": "DEBUG",
        "MY_APP_LOG_FILE": "/tmp/my-app.log",
    })
    
    # Create configuration with mixed prefixes
    config = create_config_with_prefixes(
        revo_prefix="REVO_",        # Keep default
        llm_prefix="CUSTOM_AI_",    # Custom prefix
        logging_prefix="MY_APP_",   # Custom prefix
        token_prefix="TOKEN_",      # Keep default
    )
    
    print("✓ Configuration created with mixed prefixes")
    print(f"  Revos Client ID: {config.revo.client_id}")
    print(f"  LLM Model: {config.llm.model}")
    print(f"  LLM Temperature: {config.llm.temperature}")
    print(f"  Log Level: {config.logging.level}")
    print(f"  Log File: {config.logging.file}")
    
    return config


def example_minimal_prefixes():
    """Example: Using minimal prefixes for simplicity."""
    print("\nMinimal Prefixes Example")
    print("=" * 25)
    
    # Set environment variables with minimal prefixes
    os.environ.update({
        "API_CLIENT_ID": "minimal-api-client-id",
        "API_CLIENT_SECRET": "minimal-api-client-secret",
        "MODEL": "gpt-4",
        "TEMP": "0.3",
        "LOG": "WARNING",
    })
    
    # Create configuration with minimal prefixes
    config = create_config_with_prefixes(
        revo_prefix="API_",         # Minimal prefix
        llm_prefix="",              # No prefix
        logging_prefix="",          # No prefix
        token_prefix="",            # No prefix
    )
    
    print("✓ Configuration created with minimal prefixes")
    print(f"  API Client ID: {config.revo.client_id}")
    print(f"  Model: {config.llm.model}")
    print(f"  Temperature: {config.llm.temperature}")
    print(f"  Log Level: {config.logging.level}")
    
    return config


def example_enterprise_prefixes():
    """Example: Using enterprise-style prefixes."""
    print("\nEnterprise Prefixes Example")
    print("=" * 30)
    
    # Set environment variables with enterprise-style prefixes
    os.environ.update({
        "COMPANY_REVO_CLIENT_ID": "enterprise-client-id",
        "COMPANY_REVO_CLIENT_SECRET": "enterprise-client-secret",
        "COMPANY_REVO_BASE_URL": "https://enterprise.company.com/revo",
        
        "COMPANY_LLM_MODEL": "gpt-4-turbo",
        "COMPANY_LLM_TEMPERATURE": "0.1",
        "COMPANY_LLM_MAX_TOKENS": "2000",
        
        "COMPANY_LOG_LEVEL": "ERROR",
        "COMPANY_LOG_FILE": "/var/log/company/revo.log",
    })
    
    # Create configuration with enterprise-style prefixes
    config = create_config_with_prefixes(
        revo_prefix="COMPANY_REVO_",
        llm_prefix="COMPANY_LLM_",
        logging_prefix="COMPANY_LOG_",
        token_prefix="COMPANY_TOKEN_",
    )
    
    print("✓ Configuration created with enterprise-style prefixes")
    print(f"  Company Revos Client ID: {config.revo.client_id}")
    print(f"  Company Revos Base URL: {config.revo.base_url}")
    print(f"  Company LLM Model: {config.llm.model}")
    print(f"  Company LLM Temperature: {config.llm.temperature}")
    print(f"  Company Log Level: {config.logging.level}")
    print(f"  Company Log File: {config.logging.file}")
    
    return config


def main():
    """Run all custom prefix examples."""
    print("Revos Library - Custom Environment Variable Prefixes")
    print("=" * 55)
    print("🎵 Including RUMBA_ prefix example as requested!")
    print()
    
    try:
        # Run examples
        example_custom_prefixes()  # Now includes RUMBA_ prefix example
        example_mixed_prefixes()
        example_minimal_prefixes()
        example_enterprise_prefixes()
        
        print("\n" + "=" * 55)
        print("✓ All custom prefix examples completed successfully!")
        print("\nKey Benefits:")
        print("• Avoid conflicts with existing environment variables")
        print("• Use your organization's naming conventions (like RUMBA_)")
        print("• Support multiple Revos instances in the same environment")
        print("• Maintain backward compatibility with default prefixes")
        print("• Easy integration with Docker, Kubernetes, and cloud platforms")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
