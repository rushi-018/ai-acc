"""
Enhanced Conversational AI Engine
Google Cloud Vertex AI + Gemini Integration with Fallbacks
"""
import os
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
import re
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Google Cloud imports with proper error handling
try:
    from google.cloud import aiplatform
    from google.cloud import texttospeech
    from google.cloud import speech
    import google.auth
    GOOGLE_CLOUD_AVAILABLE = True
    logger.info("✅ Google Cloud SDK loaded successfully")
except ImportError as e:
    GOOGLE_CLOUD_AVAILABLE = False
    logger.warning(f"⚠️ Google Cloud SDK not available: {e}")
    logger.info("🔄 Falling back to mock responses for demo")

# OpenAI as backup AI service
try:
    import openai
    OPENAI_AVAILABLE = True
    logger.info("✅ OpenAI SDK loaded successfully")
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("⚠️ OpenAI SDK not available")

@dataclass
class ConversationResponse:
    """Response from conversational AI"""
    response: str
    search_needed: bool = False
    search_query: Optional[str] = None
    intent: Optional[str] = None
    entities: List[Dict] = None
    confidence: float = 0.0

class ConversationalAI:
    """
    Conversational AI engine using Google Cloud Vertex AI and Gemini
    """
    
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "ai-accelerate-demo")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        self.model_name = "gemini-pro"
        
        # Initialize conversation context
        self.conversation_history = []
        self.user_preferences = {}
        
        # Product search keywords and patterns
        self.product_keywords = {
            'electronics': ['phone', 'laptop', 'computer', 'tablet', 'headphones', 'camera'],
            'fashion': ['shirt', 'dress', 'shoes', 'bag', 'watch', 'jewelry'],
            'home': ['furniture', 'kitchen', 'appliance', 'decor', 'bedding'],
            'books': ['book', 'novel', 'textbook', 'magazine', 'ebook'],
            'sports': ['fitness', 'gym', 'sports', 'exercise', 'outdoor']
        }
        
        # Initialize Google Cloud AI Platform (if available)
        if GOOGLE_CLOUD_AVAILABLE:
            self._initialize_vertex_ai()
    
    def _initialize_vertex_ai(self):
        """Initialize Vertex AI client"""
        try:
            aiplatform.init(project=self.project_id, location=self.location)
            print(f"Initialized Vertex AI for project: {self.project_id}")
        except Exception as e:
            print(f"Failed to initialize Vertex AI: {e}")
            print("Falling back to mock responses")
    
    def process_query(self, user_input: str) -> ConversationResponse:
        """
        Process user query and generate appropriate response
        """
        # Clean and normalize input
        cleaned_input = self._clean_input(user_input)
        
        # Analyze intent
        intent = self._analyze_intent(cleaned_input)
        
        # Extract entities
        entities = self._extract_entities(cleaned_input)
        
        # Determine if product search is needed
        search_needed = self._needs_product_search(cleaned_input, intent)
        
        # Generate response
        if GOOGLE_CLOUD_AVAILABLE:
            response = self._generate_vertex_ai_response(cleaned_input, intent, entities)
        else:
            response = self._generate_mock_response(cleaned_input, intent, entities)
        
        # Extract search query if needed
        search_query = None
        if search_needed:
            search_query = self._extract_search_query(cleaned_input, entities)
        
        # Update conversation history
        self.conversation_history.append({
            'user_input': user_input,
            'response': response,
            'intent': intent,
            'entities': entities,
            'search_needed': search_needed
        })
        
        return ConversationResponse(
            response=response,
            search_needed=search_needed,
            search_query=search_query,
            intent=intent,
            entities=entities,
            confidence=0.85
        )
    
    def _clean_input(self, text: str) -> str:
        """Clean and normalize user input"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Convert to lowercase for processing
        return text.lower()
    
    def _analyze_intent(self, text: str) -> str:
        """Analyze user intent from input"""
        
        # Product search intents
        if any(word in text for word in ['find', 'search', 'looking for', 'need', 'want', 'buy']):
            return 'product_search'
        
        # Comparison intents
        if any(word in text for word in ['compare', 'versus', 'vs', 'difference', 'better']):
            return 'product_compare'
        
        # Recommendation intents  
        if any(word in text for word in ['recommend', 'suggest', 'best', 'good', 'advice']):
            return 'recommendation'
        
        # Information intents
        if any(word in text for word in ['what', 'how', 'why', 'when', 'where', 'tell me']):
            return 'information'
        
        # Greeting intents
        if any(word in text for word in ['hello', 'hi', 'hey', 'good morning', 'good evening']):
            return 'greeting'
        
        return 'general'
    
    def _extract_entities(self, text: str) -> List[Dict]:
        """Extract entities from user input"""
        entities = []
        
        # Extract product categories
        for category, keywords in self.product_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    entities.append({
                        'type': 'product_category',
                        'value': category,
                        'keyword': keyword
                    })
        
        # Extract price ranges
        price_pattern = r'under|below|less than|(\d+(?:,\d{3})*(?:\.\d{2})?)'
        price_matches = re.findall(price_pattern, text)
        if price_matches:
            entities.append({
                'type': 'price_range',
                'value': price_matches[0] if price_matches[0] else 'budget'
            })
        
        # Extract brands (simple approach)
        common_brands = ['apple', 'samsung', 'sony', 'lg', 'nike', 'adidas', 'amazon', 'flipkart']
        for brand in common_brands:
            if brand in text:
                entities.append({
                    'type': 'brand',
                    'value': brand
                })
        
        return entities
    
    def _needs_product_search(self, text: str, intent: str) -> bool:
        """Determine if query needs product search"""
        
        # Always search for product-related intents
        if intent in ['product_search', 'product_compare', 'recommendation']:
            return True
        
        # Check for product-related keywords
        product_indicators = ['price', 'buy', 'purchase', 'shop', 'store', 'deal', 'offer']
        if any(word in text for word in product_indicators):
            return True
        
        # Check if any product categories mentioned
        for keywords in self.product_keywords.values():
            if any(keyword in text for keyword in keywords):
                return True
        
        return False
    
    def _extract_search_query(self, text: str, entities: List[Dict]) -> str:
        """Extract search query from user input"""
        
        # Start with original text
        search_query = text
        
        # Remove common stop words for search
        stop_words = ['find', 'search', 'looking for', 'i want', 'i need', 'show me']
        for stop_word in stop_words:
            search_query = search_query.replace(stop_word, '').strip()
        
        # If we have product entities, focus on them
        product_entities = [e for e in entities if e['type'] == 'product_category']
        if product_entities:
            # Use the most specific product keyword
            search_query = product_entities[0]['keyword']
        
        # Add brand if specified
        brand_entities = [e for e in entities if e['type'] == 'brand']
        if brand_entities:
            search_query = f"{brand_entities[0]['value']} {search_query}"
        
        return search_query.strip()
    
    def _generate_vertex_ai_response(self, text: str, intent: str, entities: List[Dict]) -> str:
        """Generate response using Google Cloud Vertex AI"""
        
        try:
            # Construct prompt for Gemini
            prompt = self._build_prompt(text, intent, entities)
            
            # Call Vertex AI Gemini model (placeholder - implement actual API call)
            # This would use the actual Vertex AI SDK
            response = "AI-powered response from Vertex AI would go here"
            
            return response
            
        except Exception as e:
            print(f"Error calling Vertex AI: {e}")
            return self._generate_mock_response(text, intent, entities)
    
    def _generate_mock_response(self, text: str, intent: str, entities: List[Dict]) -> str:
        """Generate mock response for development/testing"""
        
        if intent == 'greeting':
            return "Hello! I'm your AI shopping assistant. I can help you find products, compare prices, and get recommendations. What are you looking for today?"
        
        elif intent == 'product_search':
            product_type = "products"
            if entities:
                for entity in entities:
                    if entity['type'] == 'product_category':
                        product_type = entity['keyword']
                        break
            
            return f"I'll help you find the best {product_type}! Let me search across multiple platforms to get you the best deals and options."
        
        elif intent == 'recommendation':
            return "I'd be happy to recommend some great options! Based on your preferences and current market trends, here are some top-rated products:"
        
        elif intent == 'product_compare':
            return "I'll help you compare these products across different factors like price, features, ratings, and user reviews to help you make the best choice."
        
        elif intent == 'information':
            return "I can provide detailed information about products, features, specifications, and help you understand which option might work best for your needs."
        
        else:
            return "I'm here to help you with product searches, recommendations, and comparisons. What would you like to explore today?"
    
    def _build_prompt(self, text: str, intent: str, entities: List[Dict]) -> str:
        """Build prompt for Vertex AI Gemini model"""
        
        context = f"""
        You are an intelligent shopping assistant powered by AI. 
        
        User Intent: {intent}
        Entities Found: {entities}
        User Query: {text}
        
        Conversation History: {self.conversation_history[-3:] if self.conversation_history else "New conversation"}
        
        Respond helpfully and conversationally. If the user is looking for products, 
        acknowledge that you'll search for them and provide helpful guidance.
        
        Keep responses concise but informative.
        """
        
        return context
    
    def update_preferences(self, preferences: Dict):
        """Update user preferences for personalized responses"""
        self.user_preferences.update(preferences)
    
    def get_conversation_summary(self) -> Dict:
        """Get summary of current conversation"""
        return {
            'total_interactions': len(self.conversation_history),
            'intents': [item['intent'] for item in self.conversation_history],
            'search_queries': len([item for item in self.conversation_history if item['search_needed']]),
            'preferences': self.user_preferences
        }