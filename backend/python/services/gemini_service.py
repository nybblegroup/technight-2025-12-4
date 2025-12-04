"""
Gemini AI Service for sentiment analysis, NLU, and question generation
"""
import os
import re
from typing import List, Optional, Tuple
import google.generativeai as genai
from schemas import SentimentAnalysisResponse, GenerateQuestionResponse


class GeminiService:
    """Service for Gemini AI integration"""
    
    def __init__(self):
        """Initialize Gemini API"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        # Using gemini-2.5-flash (latest and fastest model available)
        # Alternative: gemini-2.5-pro for better quality
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    async def analyze_sentiment(self, text: str) -> SentimentAnalysisResponse:
        """
        Analyze sentiment of a text using Gemini
        
        Args:
            text: The text to analyze
            
        Returns:
            SentimentAnalysisResponse with sentiment, score, and confidence
        """
        prompt = f"""
        Analyze the sentiment of the following text and respond ONLY with a JSON object (no markdown, no backticks):
        
        {{
            "sentiment": "positive" | "negative" | "neutral",
            "score": <float between -1.0 and 1.0>,
            "confidence": <float between 0.0 and 1.0>
        }}
        
        Text to analyze: "{text}"
        
        Rules:
        - sentiment: "positive" if enthusiastic, happy, constructive
        - sentiment: "negative" if critical, unhappy, frustrated  
        - sentiment: "neutral" if balanced or informational
        - score: -1.0 (very negative) to 1.0 (very positive)
        - confidence: how confident you are in this analysis
        
        Respond with ONLY the JSON object, nothing else.
        """
        
        try:
            print(f"🤖 Gemini - Analyzing sentiment for: {text[:80]}...")
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            print(f"✅ Gemini - Raw response: {result_text}")
            
            # Clean up markdown code blocks if present
            result_text = re.sub(r'^```json\s*', '', result_text)
            result_text = re.sub(r'^```\s*', '', result_text)
            result_text = re.sub(r'\s*```$', '', result_text)
            result_text = result_text.strip()
            
            # Parse JSON response
            import json
            data = json.loads(result_text)
            
            sentiment_result = SentimentAnalysisResponse(
                sentiment=data.get("sentiment", "neutral"),
                score=float(data.get("score", 0.0)),
                confidence=float(data.get("confidence", 0.5))
            )
            
            print(f"📊 Sentiment: {sentiment_result.sentiment} (score: {sentiment_result.score:.2f}, confidence: {sentiment_result.confidence:.2f})")
            
            return sentiment_result
        except Exception as e:
            print(f"❌ Error analyzing sentiment: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to basic keyword analysis
            print("⚠️ Using fallback sentiment analysis based on keywords")
            return self._fallback_sentiment_analysis(text)
    
    def _fallback_sentiment_analysis(self, text: str) -> SentimentAnalysisResponse:
        """Fallback sentiment analysis using keyword matching"""
        positive_words = [
            'excelente', 'genial', 'bueno', 'útil', 'claro', 'interesante', 
            'me encanta', 'definitivamente', 'sí', 'perfecto', 'increíble',
            'fantástico', 'maravilloso', 'great', 'excellent', 'amazing'
        ]
        negative_words = [
            'confuso', 'difícil', 'no entendí', 'malo', 'aburrido', 'no', 
            'complicado', 'terrible', 'horrible', 'bad', 'difficult', 'boring'
        ]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
            score = min(0.7, 0.3 + (positive_count * 0.1))
        elif negative_count > positive_count:
            sentiment = "negative"
            score = max(-0.7, -0.3 - (negative_count * 0.1))
        else:
            sentiment = "neutral"
            score = 0.0
        
        return SentimentAnalysisResponse(
            sentiment=sentiment,
            score=score,
            confidence=0.6
        )
    
    async def calculate_quality_score(self, text: str, question_text: str) -> float:
        """
        Calculate quality score of a response using Gemini
        
        Args:
            text: The response text
            question_text: The original question
            
        Returns:
            Quality score between 0.0 and 1.0
        """
        # Length bonus
        length_score = min(1.0, len(text) / 100)
        
        # Complexity bonus (simple heuristic)
        words = text.split()
        complexity_score = min(1.0, len(words) / 20)
        
        # Combined score
        quality = (length_score * 0.5) + (complexity_score * 0.5)
        
        return round(quality, 2)
    
    async def generate_question(
        self, 
        context: str, 
        previous_questions: List[str] = None,
        question_type: str = "open"
    ) -> GenerateQuestionResponse:
        """
        Generate a contextual question using Gemini
        
        Args:
            context: Context about the event (e.g., "Tech Night about AI in Production")
            previous_questions: List of already asked questions to avoid repetition
            question_type: Type of question to generate
            
        Returns:
            GenerateQuestionResponse with generated question
        """
        previous_q = "\n".join([f"- {q}" for q in (previous_questions or [])])
        
        prompt = f"""
        Generate a thoughtful, engaging question for an event with this context:
        Context: {context}
        
        Previous questions already asked (avoid similar topics):
        {previous_q if previous_q else "None yet"}
        
        Question type: {question_type}
        
        Respond ONLY with a JSON object (no markdown, no backticks):
        {{
            "text": "<the question text in Spanish>",
            "question_type": "{question_type}",
            "options": ["Option 1", "Option 2", ...] (only if question_type is "quick_options" or "multiple_choice"),
            "reasoning": "<why this question is valuable>"
        }}
        
        Make the question:
        - Relevant to the event context
        - Engaging and thought-provoking
        - In Spanish (for Nybble Argentina audience)
        - Not repetitive of previous questions
        
        Respond with ONLY the JSON object.
        """
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Clean up markdown
            result_text = re.sub(r'^```json\s*', '', result_text)
            result_text = re.sub(r'^```\s*', '', result_text)
            result_text = re.sub(r'\s*```$', '', result_text)
            result_text = result_text.strip()
            
            import json
            data = json.loads(result_text)
            
            return GenerateQuestionResponse(
                text=data.get("text", "¿Qué te pareció el evento?"),
                question_type=data.get("question_type", question_type),
                options=data.get("options"),
                reasoning=data.get("reasoning", "Generated question")
            )
        except Exception as e:
            print(f"Error generating question: {e}")
            # Fallback question
            return GenerateQuestionResponse(
                text="¿Qué aspecto del evento te resultó más interesante?",
                question_type="open",
                options=None,
                reasoning="Fallback question"
            )
    
    async def extract_mentions(self, text: str) -> List[str]:
        """
        Extract @mentions from text
        
        Args:
            text: Text containing @mentions
            
        Returns:
            List of mentioned usernames (without @)
        """
        pattern = r'@(\w+)'
        mentions = re.findall(pattern, text)
        return mentions


# Singleton instance
gemini_service = GeminiService()

