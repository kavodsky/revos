#!/usr/bin/env python3
"""
Example: Using Multiple LLM Models with the Revo Library

This example demonstrates how to configure and use multiple LLM models
with different settings for different use cases.
"""

import os
from revo import (
    RevoMainConfig, 
    LangChainExtractor, 
    get_langchain_extractor,
    create_all_extractors,
    list_available_extractors
)
from pydantic import BaseModel


class TaskResult(BaseModel):
    """Example structured output for task results."""
    task: str
    result: str
    confidence: float
    reasoning: str


def example_single_model():
    """Example: Using a single model with explicit model name."""
    print("Single Model Example")
    print("=" * 25)
    
    # Create extractor with explicit model name
    extractor = get_langchain_extractor("gpt-3.5-turbo")
    
    print(f"Using model: {extractor.get_current_model()}")
    print(f"Extractor name: {extractor.name}")
    
    # Example extraction
    prompt = "Analyze the following task: 'Write a summary of machine learning'"
    
    try:
        result = extractor.extract_structured_data(
            prompt=prompt,
            target_class=TaskResult
        )
        print(f"✓ Extraction successful: {result.task}")
        print(f"  Result: {result.result[:100]}...")
        print(f"  Confidence: {result.confidence}")
    except Exception as e:
        print(f"❌ Extraction failed: {e}")


def example_specific_model():
    """Example: Using a specific model by name."""
    print("\nSpecific Model Example")
    print("=" * 28)
    
    # Create extractor for a specific model
    try:
        extractor = get_langchain_extractor("gpt-4")
        print(f"Using model: {extractor.get_current_model()}")
        print(f"Extractor name: {extractor.name}")
        
        # Example extraction
        prompt = "Create a creative story about a robot learning to paint"
        
        result = extractor.extract_structured_data(
            prompt=prompt,
            target_class=TaskResult
        )
        print(f"✓ Creative extraction successful: {result.task}")
        print(f"  Result: {result.result[:100]}...")
        
    except Exception as e:
        print(f"❌ Specific model extraction failed: {e}")


def example_multiple_extractors():
    """Example: Creating multiple extractors for different models."""
    print("\nMultiple Extractors Example")
    print("=" * 32)
    
    try:
        # Create extractors for all available models
        extractors = create_all_extractors()
        
        print(f"Created {len(extractors)} extractors:")
        for name, extractor in extractors.items():
            print(f"  - {name}: {extractor.get_current_model()} (name: {extractor.name})")
        
        # Use different extractors for different tasks
        tasks = [
            ("creative", "Write a poem about artificial intelligence"),
            ("analytical", "Analyze the pros and cons of renewable energy"),
            ("gpt-3.5-turbo", "Summarize the key points of machine learning")
        ]
        
        for model_name, task_prompt in tasks:
            if model_name in extractors:
                extractor = extractors[model_name]
                print(f"\nUsing {model_name} for: {task_prompt}")
                
                try:
                    result = extractor.extract_structured_data(
                        prompt=task_prompt,
                        target_class=TaskResult
                    )
                    print(f"✓ {model_name} extraction successful")
                    print(f"  Task: {result.task}")
                    print(f"  Result: {result.result[:80]}...")
                except Exception as e:
                    print(f"❌ {model_name} extraction failed: {e}")
            else:
                print(f"⚠️  Model {model_name} not available")
                
    except ValueError as e:
        print(f"⚠️  {e}")
        print("Please configure models in your configuration file first.")
    except Exception as e:
        print(f"❌ Multiple extractors failed: {e}")


def example_custom_extractor():
    """Example: Creating a custom extractor with specific settings."""
    print("\nCustom Extractor Example")
    print("=" * 28)
    
    try:
        # Create a custom extractor with specific name
        custom_extractor = LangChainExtractor(
            model_name="gpt-4",
            name="my_custom_extractor"
        )
        
        print(f"Custom extractor created:")
        print(f"  Name: {custom_extractor.name}")
        print(f"  Model: {custom_extractor.get_current_model()}")
        
        # Use the custom extractor
        prompt = "Explain quantum computing in simple terms"
        
        result = custom_extractor.extract_structured_data(
            prompt=prompt,
            target_class=TaskResult
        )
        print(f"✓ Custom extractor successful")
        print(f"  Task: {result.task}")
        print(f"  Result: {result.result[:100]}...")
        
    except Exception as e:
        print(f"❌ Custom extractor failed: {e}")


def example_list_models():
    """Example: Listing available models and extractors."""
    print("\nAvailable Models Example")
    print("=" * 28)
    
    try:
        # List available extractors
        available = list_available_extractors()
        
        print("Available extractors:")
        for name, description in available.items():
            print(f"  - {name}: {description}")
        
        # Show how to get specific extractors
        print(f"\nYou can get specific extractors using:")
        for name in available.keys():
            print(f"  get_langchain_extractor('{name}')")
            
    except ValueError as e:
        print(f"⚠️  {e}")
        print("Please configure models in your configuration file first.")
    except Exception as e:
        print(f"❌ List models failed: {e}")


def example_configuration():
    """Example: Loading configuration with multiple models."""
    print("\nConfiguration Example")
    print("=" * 25)
    
    try:
        # Load configuration from file (if it exists)
        config_file = "config_multiple_models.yaml.example"
        if os.path.exists(config_file):
            config = RevoMainConfig.from_file(config_file)
            print(f"✓ Loaded configuration from {config_file}")
            
            # Show available models
            if hasattr(config, 'llm_models'):
                print("Available models:")
                for name, model_config in config.llm_models.models.items():
                    print(f"  - {name}: {model_config.description}")
            else:
                print("Single model configuration detected")
        else:
            print(f"⚠️  Configuration file {config_file} not found")
            print("Using default configuration")
            
    except Exception as e:
        print(f"❌ Configuration example failed: {e}")


def main():
    """Run all multiple models examples."""
    print("Revo Library - Multiple LLM Models Examples")
    print("=" * 50)
    
    try:
        # Run examples
        example_single_model()
        example_specific_model()
        example_multiple_extractors()
        example_custom_extractor()
        example_list_models()
        example_configuration()
        
        print("\n" + "=" * 50)
        print("✓ All multiple models examples completed!")
        print("\nKey Benefits:")
        print("• Use different models for different tasks")
        print("• Optimize cost vs. performance per use case")
        print("• Easy model switching without reconfiguration")
        print("• Isolated extractor instances for better reliability")
        print("• Custom naming for better organization")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
