#!/usr/bin/env python3
"""
Test script for FastAPI RUMBA_ example

This script demonstrates how to test the FastAPI RUMBA_ example
by setting up environment variables and making API calls.
"""

import os
import requests
import time
from dotenv import load_dotenv

def setup_rumba_environment():
    """Set up RUMBA_ environment variables for testing."""
    print("🎵 Setting up RUMBA_ environment variables for testing...")
    
    # Set RUMBA_ environment variables
    os.environ.update({
        "RUMBA_CLIENT_ID": "test_rumba_client_id",
        "RUMBA_CLIENT_SECRET": "test_rumba_client_secret",
        "RUMBA_TOKEN_URL": "https://test-site.com/revo/oauth/token",
        "RUMBA_BASE_URL": "https://test-site.com/revo/llm-api",
        "RUMBA_LLM_MODEL": "gpt-4",
        "RUMBA_LLM_TEMPERATURE": "0.1",
        "RUMBA_LLM_MAX_TOKENS": "1000",
        "RUMBA_TOKEN_MANAGER_REFRESH_INTERVAL_MINUTES": "45",
        "RUMBA_LOGGING_LEVEL": "INFO"
    })
    
    print("✅ RUMBA_ environment variables set for testing")
    print(f"📊 RUMBA_CLIENT_ID: {os.getenv('RUMBA_CLIENT_ID')}")
    print(f"🤖 RUMBA_LLM_MODEL: {os.getenv('RUMBA_LLM_MODEL')}")
    print(f"🌡️  RUMBA_LLM_TEMPERATURE: {os.getenv('RUMBA_LLM_TEMPERATURE')}")

def test_fastapi_endpoints():
    """Test the FastAPI RUMBA_ endpoints."""
    base_url = "http://localhost:8000"
    
    print("\n🧪 Testing FastAPI RUMBA_ endpoints...")
    
    try:
        # Test root endpoint
        print("\n1. Testing root endpoint...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint: {data['message']}")
            print(f"🎵 Prefix: {data['prefix']}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
        
        # Test health check
        print("\n2. Testing health check...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data['status']}")
            print(f"🎵 RUMBA connected: {data['rumba_connected']}")
            print(f"🤖 Model: {data.get('model', 'N/A')}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
        
        # Test configuration endpoint
        print("\n3. Testing configuration endpoint...")
        response = requests.get(f"{base_url}/config")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Configuration loaded")
            print(f"🎵 Prefix: {data['prefix']}")
            print(f"📊 Client ID: {data['client_id']}")
            print(f"🤖 LLM Model: {data['llm_model']}")
        else:
            print(f"❌ Configuration endpoint failed: {response.status_code}")
        
        # Test token status
        print("\n4. Testing token status...")
        response = requests.get(f"{base_url}/token-status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Token status retrieved")
            print(f"🎵 Prefix: {data['prefix']}")
            print(f"🔄 Background service: {data['background_service_running']}")
        else:
            print(f"❌ Token status failed: {response.status_code}")
        
        # Test document summarization
        print("\n5. Testing document summarization...")
        test_text = "Artificial Intelligence is transforming industries across the globe. From healthcare to finance, AI technologies are enabling new possibilities and improving efficiency."
        
        response = requests.post(
            f"{base_url}/summarize",
            json={"text": test_text}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Document summarization successful")
            print(f"🎵 Prefix: {data['prefix']}")
            print(f"🤖 Model: {data['model']}")
            if 'summary' in data:
                summary = data['summary']
                print(f"📄 Title: {summary.get('title', 'N/A')}")
                print(f"📝 Summary: {summary.get('summary', 'N/A')[:100]}...")
        else:
            print(f"❌ Document summarization failed: {response.status_code}")
            print(f"Response: {response.text}")
        
        # Test sentiment analysis
        print("\n6. Testing sentiment analysis...")
        test_review = "This product is absolutely amazing! I love how easy it is to use and the results are fantastic."
        
        response = requests.post(
            f"{base_url}/analyze-sentiment",
            json={"text": test_review}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sentiment analysis successful")
            print(f"🎵 Prefix: {data['prefix']}")
            print(f"🤖 Model: {data['model']}")
            if 'analysis' in data:
                analysis = data['analysis']
                print(f"😊 Sentiment: {analysis.get('sentiment', 'N/A')}")
                print(f"📊 Confidence: {analysis.get('confidence', 'N/A')}")
        else:
            print(f"❌ Sentiment analysis failed: {response.status_code}")
            print(f"Response: {response.text}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to FastAPI server")
        print("💡 Make sure the FastAPI server is running on http://localhost:8000")
        print("💡 Run: python examples/fastapi_rumba_example.py")
    except Exception as e:
        print(f"❌ Error testing endpoints: {e}")

def main():
    """Main function to test the FastAPI RUMBA_ example."""
    print("🎵 FastAPI RUMBA_ Example Test Script")
    print("=" * 50)
    
    # Set up environment
    setup_rumba_environment()
    
    # Wait a moment for the server to start if it's starting
    print("\n⏳ Waiting 3 seconds for server to be ready...")
    time.sleep(3)
    
    # Test endpoints
    test_fastapi_endpoints()
    
    print("\n🎉 FastAPI RUMBA_ example test completed!")
    print("\n💡 To run the full FastAPI server:")
    print("   python examples/fastapi_rumba_example.py")
    print("\n💡 To test with your own .env file:")
    print("   1. Copy examples/env.rumba.example to .env")
    print("   2. Update the values in .env with your actual credentials")
    print("   3. Run the FastAPI server")

if __name__ == "__main__":
    main()
