#!/usr/bin/env python3
"""
Configuration examples for the Revo library.

This example demonstrates various ways to configure the library:
1. Using environment variables
2. Using configuration files
3. Using programmatic configuration
4. Loading from different file formats
"""

import os
import tempfile
from pathlib import Path

from revo import (
    RevoMainConfig,
    RevoConfig,
    LLMConfig,
    LoggingConfig,
    TokenManagerConfig,
    get_settings,
    load_config_from_file
)


def example_environment_variables():
    """Example: Configuration via environment variables."""
    print("1. Environment Variables Configuration")
    print("=" * 40)
    
    # Set environment variables
    os.environ.update({
        "REVO_CLIENT_ID": "env_client_id",
        "REVO_CLIENT_SECRET": "env_client_secret",
        "REVO_TOKEN_URL": "https://env.example.com/token",
        "LLM_MODEL": "gpt-4",
        "LLM_TEMPERATURE": "0.3",
        "LOG_LEVEL": "DEBUG",
        "TOKEN_REFRESH_INTERVAL_MINUTES": "30"
    })
    
    # Load configuration
    config = get_settings()
    
    print(f"✓ Revo Client ID: {config.revo.client_id}")
    print(f"✓ LLM Model: {config.llm.model}")
    print(f"✓ Log Level: {config.logging.level}")
    print(f"✓ Refresh Interval: {config.token_manager.refresh_interval_minutes} minutes")


def example_programmatic_configuration():
    """Example: Programmatic configuration."""
    print("\n2. Programmatic Configuration")
    print("=" * 35)
    
    # Create configuration programmatically
    config = RevoMainConfig(
        revo=RevoConfig(
            client_id="prog_client_id",
            client_secret="prog_client_secret",
            token_url="https://prog.example.com/token",
            base_url="https://prog.example.com/api",
            token_buffer_minutes=10,
            max_retries=5,
            request_timeout=60
        ),
        llm=LLMConfig(
            model="gpt-4-turbo",
            temperature=0.2,
            max_tokens=2048,
            top_p=0.9,
            frequency_penalty=0.1,
            presence_penalty=0.1
        ),
        logging=LoggingConfig(
            level="INFO",
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            file="/tmp/revo.log",
            max_size=20 * 1024 * 1024,  # 20MB
            backup_count=3
        ),
        token_manager=TokenManagerConfig(
            refresh_interval_minutes=60,
            max_failures_before_fallback=2,
            enable_periodic_refresh=True,
            enable_fallback=True
        ),
        debug=True
    )
    
    print(f"✓ Revo URL: {config.revo.token_url}")
    print(f"✓ LLM Model: {config.llm.model}")
    print(f"✓ Temperature: {config.llm.temperature}")
    print(f"✓ Max Tokens: {config.llm.max_tokens}")
    print(f"✓ Log File: {config.logging.file}")
    print(f"✓ Debug Mode: {config.debug}")


def example_yaml_configuration():
    """Example: YAML configuration file."""
    print("\n3. YAML Configuration File")
    print("=" * 30)
    
    # Create a temporary YAML file
    yaml_content = """
revo:
  client_id: "yaml_client_id"
  client_secret: "yaml_client_secret"
  token_url: "https://yaml.example.com/token"
  base_url: "https://yaml.example.com/api"
  token_buffer_minutes: 15
  max_retries: 3
  request_timeout: 45

llm:
  model: "gpt-3.5-turbo"
  temperature: 0.1
  max_tokens: 1024
  top_p: 1.0
  frequency_penalty: 0.0
  presence_penalty: 0.0

logging:
  level: "WARNING"
  format: "%(asctime)s - %(levelname)s - %(message)s"
  file: "/tmp/yaml_revo.log"
  max_size: 10485760  # 10MB
  backup_count: 5

token_manager:
  refresh_interval_minutes: 45
  max_failures_before_fallback: 1
  enable_periodic_refresh: true
  enable_fallback: true

debug: false
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write(yaml_content)
        yaml_file = f.name
    
    try:
        # Load configuration from YAML file
        config = load_config_from_file(yaml_file)
        
        print(f"✓ Revo Client ID: {config.revo.client_id}")
        print(f"✓ Token Buffer: {config.revo.token_buffer_minutes} minutes")
        print(f"✓ LLM Model: {config.llm.model}")
        print(f"✓ Log Level: {config.logging.level}")
        print(f"✓ Debug Mode: {config.debug}")
        
    finally:
        # Clean up
        os.unlink(yaml_file)


def example_json_configuration():
    """Example: JSON configuration file."""
    print("\n4. JSON Configuration File")
    print("=" * 30)
    
    # Create a temporary JSON file
    json_content = """
{
  "apollo": {
    "client_id": "json_client_id",
    "client_secret": "json_client_secret",
    "token_url": "https://json.example.com/token",
    "base_url": "https://json.example.com/api",
    "token_buffer_minutes": 20,
    "max_retries": 4,
    "request_timeout": 30
  },
  "llm": {
    "model": "gpt-4",
    "temperature": 0.5,
    "max_tokens": 4096,
    "top_p": 0.8,
    "frequency_penalty": 0.2,
    "presence_penalty": 0.2
  },
  "logging": {
    "level": "ERROR",
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "file": "/tmp/json_revo.log",
    "max_size": 5242880,
    "backup_count": 2
  },
  "token_manager": {
    "refresh_interval_minutes": 30,
    "max_failures_before_fallback": 3,
    "enable_periodic_refresh": false,
    "enable_fallback": true
  },
  "debug": true
}
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write(json_content)
        json_file = f.name
    
    try:
        # Load configuration from JSON file
        config = load_config_from_file(json_file)
        
        print(f"✓ Revo Client ID: {config.revo.client_id}")
        print(f"✓ Request Timeout: {config.revo.request_timeout} seconds")
        print(f"✓ LLM Temperature: {config.llm.temperature}")
        print(f"✓ Max Tokens: {config.llm.max_tokens}")
        print(f"✓ Periodic Refresh: {config.token_manager.enable_periodic_refresh}")
        
    finally:
        # Clean up
        os.unlink(json_file)


def example_env_file():
    """Example: .env file configuration."""
    print("\n5. .env File Configuration")
    print("=" * 28)
    
    # Create a temporary .env file
    env_content = """
# Apollo Configuration
APOLLO_CLIENT_ID=env_file_client_id
APOLLO_CLIENT_SECRET=env_file_client_secret
APOLLO_TOKEN_URL=https://envfile.example.com/token
APOLLO_BASE_URL=https://envfile.example.com/api
APOLLO_TOKEN_BUFFER_MINUTES=25
APOLLO_MAX_RETRIES=2
APOLLO_REQUEST_TIMEOUT=40

# LLM Configuration
LLM_MODEL=gpt-3.5-turbo
LLM_TEMPERATURE=0.15
LLM_MAX_TOKENS=2048
LLM_TOP_P=0.95
LLM_FREQUENCY_PENALTY=0.05
LLM_PRESENCE_PENALTY=0.05

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
LOG_FILE=/tmp/envfile_revo.log
LOG_MAX_SIZE=15728640
LOG_BACKUP_COUNT=4

# Token Manager Configuration
TOKEN_REFRESH_INTERVAL_MINUTES=50
TOKEN_MAX_FAILURES_BEFORE_FALLBACK=2
TOKEN_ENABLE_PERIODIC_REFRESH=true
TOKEN_ENABLE_FALLBACK=true

# Global Configuration
DEBUG=false
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write(env_content)
        env_file = f.name
    
    try:
        # Load configuration from .env file
        config = RevoMainConfig(_env_file=env_file)
        
        print(f"✓ Revo Client ID: {config.revo.client_id}")
        print(f"✓ Token Buffer: {config.revo.token_buffer_minutes} minutes")
        print(f"✓ LLM Model: {config.llm.model}")
        print(f"✓ Temperature: {config.llm.temperature}")
        print(f"✓ Log File: {config.logging.file}")
        print(f"✓ Refresh Interval: {config.token_manager.refresh_interval_minutes} minutes")
        
    finally:
        # Clean up
        os.unlink(env_file)


def example_save_configuration():
    """Example: Save configuration to file."""
    print("\n6. Save Configuration to File")
    print("=" * 33)
    
    # Create a configuration
    config = RevoMainConfig(
        revo=RevoConfig(
            client_id="save_client_id",
            client_secret="save_client_secret"
        ),
        llm=LLMConfig(
            model="gpt-4",
            temperature=0.3
        ),
        debug=True
    )
    
    # Save to YAML file
    with tempfile.NamedTemporaryFile(suffix='.yaml', delete=False) as f:
        yaml_file = f.name
    
    try:
        config.save_to_file(yaml_file, format='yaml')
        print(f"✓ Configuration saved to: {yaml_file}")
        
        # Verify by loading it back
        loaded_config = load_config_from_file(yaml_file)
        print(f"✓ Loaded Revo Client ID: {loaded_config.revo.client_id}")
        print(f"✓ Loaded LLM Model: {loaded_config.llm.model}")
        print(f"✓ Loaded Debug Mode: {loaded_config.debug}")
        
    finally:
        # Clean up
        os.unlink(yaml_file)


def example_environment_variables_export():
    """Example: Export configuration as environment variables."""
    print("\n7. Export as Environment Variables")
    print("=" * 37)
    
    # Create a configuration
    config = RevoMainConfig(
        revo=RevoConfig(
            client_id="export_client_id",
            client_secret="export_client_secret",
            token_url="https://export.example.com/token"
        ),
        llm=LLMConfig(
            model="gpt-4-turbo",
            temperature=0.2
        ),
        debug=True
    )
    
    # Show configuration summary
    print("Configuration summary:")
    print(f"  Revo API URL: {config.revo.base_url}")
    print(f"  LLM Model: {config.llm.model}")
    print(f"  Log Level: {config.logging.level}")
    print(f"  Debug Mode: {config.debug}")


def main():
    """Run all configuration examples."""
    print("Revo Library Configuration Examples")
    print("=" * 40)
    
    try:
        example_environment_variables()
        example_programmatic_configuration()
        example_yaml_configuration()
        example_json_configuration()
        example_env_file()
        example_save_configuration()
        example_environment_variables_export()
        
        print("\n" + "=" * 40)
        print("All configuration examples completed successfully!")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
