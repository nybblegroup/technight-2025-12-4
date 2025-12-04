#!/usr/bin/env python3
"""
Quick test script to verify Gemini API is working correctly
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_gemini():
    """Test Gemini sentiment analysis"""
    from services.gemini_service import gemini_service
    
    print("=" * 60)
    print("🧪 Testing Gemini API")
    print("=" * 60)
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found in .env")
        print("\n🔧 How to fix:")
        print("1. Go to https://makersuite.google.com/app/apikey")
        print("2. Create a new API key")
        print("3. Add to backend/python/.env:")
        print('   GEMINI_API_KEY=your_api_key_here')
        return
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-5:]}")
    print()
    
    # Test cases
    test_cases = [
        {
            "text": "¡Excelente evento! Me encantó todo, muy claro e interesante. Definitivamente voy a aplicar esto.",
            "expected": "positive"
        },
        {
            "text": "No entendí nada, muy confuso y aburrido. La presentación fue terrible.",
            "expected": "negative"
        },
        {
            "text": "El evento estuvo bien. Algunos puntos fueron interesantes, otros no tanto.",
            "expected": "neutral"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 Test Case {i}: {test_case['expected'].upper()}")
        print(f"   Text: {test_case['text'][:60]}...")
        print()
        
        try:
            result = await gemini_service.analyze_sentiment(test_case['text'])
            
            # Check if sentiment matches expected
            if result.sentiment == test_case['expected']:
                print(f"   ✅ PASS - Sentiment: {result.sentiment}")
            else:
                print(f"   ⚠️  PARTIAL - Expected: {test_case['expected']}, Got: {result.sentiment}")
            
            print(f"   📊 Score: {result.score:.2f}")
            print(f"   🎯 Confidence: {result.confidence:.2f}")
            
        except Exception as e:
            print(f"   ❌ FAIL - Error: {e}")
        
        print("-" * 60)
        print()
    
    print("=" * 60)
    print("✅ Gemini API test complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_gemini())





