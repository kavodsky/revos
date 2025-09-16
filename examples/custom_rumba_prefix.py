#!/usr/bin/env python3
"""
Custom RUMBA_ Prefix Example

This example demonstrates how to use Revos with a custom environment variable
prefix (RUMBA_) instead of the default REVOS_ prefix.

This is useful when:
- You want to avoid conflicts with other libraries
- You're integrating Revos into an existing system
- You need to maintain consistent naming conventions
- You're working with multiple environments or configurations
"""

import os
from revos import create_config_with_prefixes, LangChainExtractor, get_revos_token
from pydantic import BaseModel

# Example 1: Basic Custom Prefix Configuration
def example_basic_custom_prefix():
    """Basic example of using RUMBA_ prefix."""
    print("🎯 Example 1: Basic Custom Prefix Configuration")
    print("=" * 60)
    
    # Set environment variables with RUMBA_ prefix
    os.environ.update({
        "RUMBA_CLIENT_ID": "your_rumba_client_id",
        "RUMBA_CLIENT_SECRET": "your_rumba_client_secret",
        "RUMBA_TOKEN_URL": "https://your-site.com/revo/oauth/token",
        "RUMBA_BASE_URL": "https://your-site.com/revo/llm-api",
        "RUMBA_TOKEN_BUFFER_MINUTES": "5",
        "RUMBA_MAX_RETRIES": "3",
        "RUMBA_REQUEST_TIMEOUT": "30",
        
        # LLM configuration with RUMBA_ prefix
        "RUMBA_LLM_MODEL": "gpt-4",
        "RUMBA_LLM_TEMPERATURE": "0.1",
        "RUMBA_LLM_MAX_TOKENS": "1000",
        "RUMBA_LLM_TOP_P": "1.0",
        "RUMBA_LLM_FREQUENCY_PENALTY": "0.0",
        "RUMBA_LLM_PRESENCE_PENALTY": "0.0",
        
        # Token manager configuration
        "RUMBA_TOKEN_MANAGER_REFRESH_INTERVAL_MINUTES": "45",
        "RUMBA_TOKEN_MANAGER_MAX_FAILURES_BEFORE_FALLBACK": "3",
        "RUMBA_TOKEN_MANAGER_ENABLE_PERIODIC_REFRESH": "true",
        "RUMBA_TOKEN_MANAGER_ENABLE_FALLBACK": "true",
        
        # Logging configuration
        "RUMBA_LOGGING_LEVEL": "INFO",
        "RUMBA_LOGGING_FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    })
    
    # Create configuration with custom RUMBA_ prefix
    config = create_config_with_prefixes(
        revo_prefix="RUMBA_",  # Use RUMBA_ prefix instead of REVOS_
        llm_prefix="RUMBA_LLM_",  # Use RUMBA_LLM_ prefix for LLM settings
        logging_prefix="RUMBA_LOG_",  # Use RUMBA_LOG_ prefix for logging
        token_prefix="RUMBA_TOKEN_"  # Use RUMBA_TOKEN_ prefix for token management
    )
    
    print(f"✅ Configuration created with RUMBA_ prefix")
    print(f"📊 Client ID: {config.revos.client_id}")
    print(f"🤖 LLM Model: {config.llm.model}")
    print(f"🔄 Refresh Interval: {config.token_manager.refresh_interval_minutes} minutes")
    print(f"📝 Logging Level: {config.logging.level}")
    print()

# Example 2: Multiple Models with Custom Prefix
def example_multiple_models_custom_prefix():
    """Example with multiple LLM models using RUMBA_ prefix."""
    print("🎯 Example 2: Multiple Models with Custom Prefix")
    print("=" * 60)
    
    # Set environment variables for multiple models
    os.environ.update({
        "RUMBA_CLIENT_ID": "your_rumba_client_id",
        "RUMBA_CLIENT_SECRET": "your_rumba_client_secret",
        "RUMBA_TOKEN_URL": "https://your-site.com/revo/oauth/token",
        "RUMBA_BASE_URL": "https://your-site.com/revo/llm-api",
        
        # Multiple LLM models with RUMBA_ prefix
        "RUMBA_LLM_MODELS_0_MODEL": "gpt-3.5-turbo",
        "RUMBA_LLM_MODELS_0_TEMPERATURE": "0.0",
        "RUMBA_LLM_MODELS_0_MAX_TOKENS": "500",
        "RUMBA_LLM_MODELS_0_DESCRIPTION": "Fast model for simple tasks",
        
        "RUMBA_LLM_MODELS_1_MODEL": "gpt-4",
        "RUMBA_LLM_MODELS_1_TEMPERATURE": "0.0",
        "RUMBA_LLM_MODELS_1_MAX_TOKENS": "2000",
        "RUMBA_LLM_MODELS_1_DESCRIPTION": "Accurate model for complex tasks",
        
        "RUMBA_LLM_MODELS_2_MODEL": "gpt-4",
        "RUMBA_LLM_MODELS_2_TEMPERATURE": "0.8",
        "RUMBA_LLM_MODELS_2_MAX_TOKENS": "1500",
        "RUMBA_LLM_MODELS_2_DESCRIPTION": "Creative model for brainstorming"
    })
    
    # Create configuration with multiple models
    config = create_config_with_prefixes(
        revo_prefix="RUMBA_",  # Use RUMBA_ prefix
        llm_prefix="RUMBA_LLM_",  # Use RUMBA_LLM_ prefix for LLM settings
        logging_prefix="RUMBA_LOG_",  # Use RUMBA_LOG_ prefix for logging
        token_prefix="RUMBA_TOKEN_"  # Use RUMBA_TOKEN_ prefix for token management
    )
    
    print(f"✅ Multiple models configuration created with RUMBA_ prefix")
    print(f"📊 Available models: {list(config.llm_models.models.keys())}")
    
    for model_name, model_config in config.llm_models.models.items():
        print(f"  🎯 {model_name}: {model_config.model} ({model_config.description})")
    print()

# Example 3: Environment-Specific Custom Prefixes
def example_environment_specific_prefixes():
    """Example showing different prefixes for different environments."""
    print("🎯 Example 3: Environment-Specific Custom Prefixes")
    print("=" * 60)
    
    # Development environment with RUMBA_DEV_ prefix
    dev_config = create_config_with_prefixes(
        revos={
            "client_id": "dev_rumba_client_id",
            "client_secret": "dev_rumba_client_secret",
            "token_url": "https://dev-api.example.com/oauth/token",
            "base_url": "https://dev-api.example.com/llm-api"
        },
        llm={
            "model": "gpt-3.5-turbo",
            "temperature": 0.1,
            "max_tokens": 500
        },
        token_manager={
            "refresh_interval_minutes": 30,
            "max_failures_before_fallback": 2
        },
        logging={
            "level": "DEBUG"
        }
    )
    
    # Production environment with RUMBA_PROD_ prefix
    prod_config = create_config_with_prefixes(
        revos={
            "client_id": "prod_rumba_client_id",
            "client_secret": "prod_rumba_client_secret",
            "token_url": "https://api.example.com/oauth/token",
            "base_url": "https://api.example.com/llm-api"
        },
        llm={
            "model": "gpt-4",
            "temperature": 0.0,
            "max_tokens": 2000
        },
        token_manager={
            "refresh_interval_minutes": 60,
            "max_failures_before_fallback": 5
        },
        logging={
            "level": "INFO"
        }
    )
    
    print(f"✅ Development configuration:")
    print(f"  🏗️  Environment: Development")
    print(f"  🔗 Token URL: {dev_config.revos.token_url}")
    print(f"  🤖 Model: {dev_config.llm.model}")
    print(f"  📝 Logging: {dev_config.logging.level}")
    print()
    
    print(f"✅ Production configuration:")
    print(f"  🚀 Environment: Production")
    print(f"  🔗 Token URL: {prod_config.revos.token_url}")
    print(f"  🤖 Model: {prod_config.llm.model}")
    print(f"  📝 Logging: {prod_config.logging.level}")
    print()

# Example 4: Using Custom Prefix with LangChain Extractor
def example_custom_prefix_with_extractor():
    """Example of using custom prefix configuration with LangChain extractor."""
    print("🎯 Example 4: Using Custom Prefix with LangChain Extractor")
    print("=" * 60)
    
    # Define a data model
    class RumbaAnalysis(BaseModel):
        sentiment: str
        confidence: float
        key_themes: list[str]
        language: str
    
    # Create configuration with RUMBA_ prefix
    config = create_config_with_prefixes(
        revos={
            "client_id": "your_rumba_client_id",
            "client_secret": "your_rumba_client_secret"
        },
        llm={
            "model": "gpt-4",
            "temperature": 0.1,
            "max_tokens": 1000
        }
    )
    
    try:
        # Initialize extractor with custom configuration
        extractor = LangChainExtractor(
            model_name="gpt-4",
            settings_instance=config
        )
        
        print(f"✅ LangChain extractor initialized with RUMBA_ prefix configuration")
        print(f"🤖 Current model: {extractor.get_current_model()}")
        
        # Example extraction
        sample_text = "The RUMBA system is absolutely fantastic! It's revolutionizing how we handle data processing and analysis."
        
        result = extractor.extract_structured_data(
            prompt=f"Analyze this text about RUMBA: {sample_text}",
            target_class=RumbaAnalysis
        )
        
        print(f"📊 Analysis Results:")
        print(f"  😊 Sentiment: {result.sentiment}")
        print(f"  📈 Confidence: {result.confidence:.2f}")
        print(f"  🎯 Key Themes: {', '.join(result.key_themes)}")
        print(f"  🌍 Language: {result.language}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure to set valid RUMBA_ environment variables")
    print()

# Example 5: Docker Environment with Custom Prefix
def example_docker_environment():
    """Example of using custom prefix in Docker environment."""
    print("🎯 Example 5: Docker Environment with Custom Prefix")
    print("=" * 60)
    
    # Docker environment variables (typically set in docker-compose.yml or Dockerfile)
    docker_env_vars = {
        "RUMBA_CLIENT_ID": "docker_rumba_client_id",
        "RUMBA_CLIENT_SECRET": "docker_rumba_client_secret",
        "RUMBA_TOKEN_URL": "https://docker-api.example.com/oauth/token",
        "RUMBA_BASE_URL": "https://docker-api.example.com/llm-api",
        "RUMBA_LLM_MODEL": "gpt-4",
        "RUMBA_LLM_TEMPERATURE": "0.0",
        "RUMBA_LLM_MAX_TOKENS": "1500",
        "RUMBA_TOKEN_MANAGER_REFRESH_INTERVAL_MINUTES": "30",
        "RUMBA_LOGGING_LEVEL": "INFO"
    }
    
    print("🐳 Docker Environment Variables:")
    for key, value in docker_env_vars.items():
        if "SECRET" in key:
            print(f"  {key}=***hidden***")
        else:
            print(f"  {key}={value}")
    print()
    
    # Create configuration for Docker environment
    config = create_config_with_prefixes(
        revos={
            "client_id": "docker_rumba_client_id",
            "client_secret": "docker_rumba_client_secret",
            "token_url": "https://docker-api.example.com/oauth/token",
            "base_url": "https://docker-api.example.com/llm-api"
        },
        llm={
            "model": "gpt-4",
            "temperature": 0.0,
            "max_tokens": 1500
        },
        token_manager={
            "refresh_interval_minutes": 30
        },
        logging={
            "level": "INFO"
        }
    )
    
    print(f"✅ Docker configuration created with RUMBA_ prefix")
    print(f"🐳 Environment: Docker")
    print(f"🔗 Base URL: {config.revos.base_url}")
    print(f"🤖 Model: {config.llm.model}")
    print(f"🔄 Refresh Interval: {config.token_manager.refresh_interval_minutes} minutes")
    print()

# Example 6: Kubernetes ConfigMap with Custom Prefix
def example_kubernetes_configmap():
    """Example of using custom prefix with Kubernetes ConfigMap."""
    print("🎯 Example 6: Kubernetes ConfigMap with Custom Prefix")
    print("=" * 60)
    
    # Kubernetes ConfigMap YAML example
    configmap_yaml = """
apiVersion: v1
kind: ConfigMap
metadata:
  name: rumba-config
  namespace: default
data:
  RUMBA_CLIENT_ID: "k8s_rumba_client_id"
  RUMBA_CLIENT_SECRET: "k8s_rumba_client_secret"
  RUMBA_TOKEN_URL: "https://k8s-api.example.com/oauth/token"
  RUMBA_BASE_URL: "https://k8s-api.example.com/llm-api"
  RUMBA_LLM_MODEL: "gpt-4"
  RUMBA_LLM_TEMPERATURE: "0.0"
  RUMBA_LLM_MAX_TOKENS: "2000"
  RUMBA_TOKEN_MANAGER_REFRESH_INTERVAL_MINUTES: "45"
  RUMBA_LOGGING_LEVEL: "INFO"
"""
    
    print("☸️  Kubernetes ConfigMap YAML:")
    print(configmap_yaml)
    
    # Create configuration for Kubernetes environment
    config = create_config_with_prefixes(
        revos={
            "client_id": "k8s_rumba_client_id",
            "client_secret": "k8s_rumba_client_secret",
            "token_url": "https://k8s-api.example.com/oauth/token",
            "base_url": "https://k8s-api.example.com/llm-api"
        },
        llm={
            "model": "gpt-4",
            "temperature": 0.0,
            "max_tokens": 2000
        },
        token_manager={
            "refresh_interval_minutes": 45
        },
        logging={
            "level": "INFO"
        }
    )
    
    print(f"✅ Kubernetes configuration created with RUMBA_ prefix")
    print(f"☸️  Environment: Kubernetes")
    print(f"🔗 Base URL: {config.revos.base_url}")
    print(f"🤖 Model: {config.llm.model}")
    print(f"🔄 Refresh Interval: {config.token_manager.refresh_interval_minutes} minutes")
    print()

def main():
    """Run all RUMBA_ prefix examples."""
    print("🎵 RUMBA_ Custom Prefix Examples")
    print("=" * 80)
    print("This example demonstrates how to use Revos with a custom RUMBA_ prefix")
    print("instead of the default REVOS_ prefix.")
    print()
    
    try:
        example_basic_custom_prefix()
        example_multiple_models_custom_prefix()
        example_environment_specific_prefixes()
        example_custom_prefix_with_extractor()
        example_docker_environment()
        example_kubernetes_configmap()
        
        print("🎉 All RUMBA_ prefix examples completed successfully!")
        print()
        print("💡 Key Benefits of Custom Prefixes:")
        print("  🔧 Avoid conflicts with other libraries")
        print("  🏗️  Maintain consistent naming conventions")
        print("  🌍 Support multiple environments")
        print("  🐳 Easy integration with Docker/Kubernetes")
        print("  🔒 Better security with environment-specific configs")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")
        print("💡 Make sure to set valid RUMBA_ environment variables")

if __name__ == "__main__":
    main()
