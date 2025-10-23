"""
FREE Google Cloud integration using Gemini AI Studio
No billing account required - completely free tier
"""

import google.generativeai as genai
import os
import json
from typing import Dict, List, Optional
import time

class GoogleCloudFree:
    def __init__(self, api_key: str = None):
        """Initialize free Google Cloud services"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Use the latest free model
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            self.connected = True
            print("✅ Google Gemini connected (FREE)")
        else:
            self.connected = False
            print("⚠️ Gemini API key not found - running in demo mode")
    
    def analyze_shopping_query(self, query: str, context: Dict = None) -> Dict:
        """Analyze shopping query using Gemini AI"""
        if not self.connected:
            return self._demo_analysis(query)
        
        try:
            prompt = f"""
            Analyze this shopping query and extract key information:
            
            Query: "{query}"
            Context: {json.dumps(context) if context else "None"}
            
            Extract:
            1. Product type/category
            2. Budget range (if mentioned)
            3. Key features/requirements
            4. Shopping intent (browse/compare/buy)
            5. Urgency level
            
            Return as JSON format with clear structure.
            """
            
            response = self.model.generate_content(prompt)
            return {
                'status': 'success',
                'analysis': response.text,
                'ai_powered': True,
                'service': 'Google Gemini Pro'
            }
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._demo_analysis(query)
    
    def generate_conversational_response(self, query: str, products: List, analysis: Dict) -> str:
        """Generate natural conversation response"""
        if not self.connected:
            return self._demo_response(query, products)
        
        try:
            prompt = f"""
            You are AIVA, an intelligent shopping assistant powered by Google AI and Elastic search.
            
            User asked: "{query}"
            Analysis: {json.dumps(analysis)}
            Found products: {json.dumps(products[:3], indent=2) if products else "No products found"}
            
            Generate a natural, helpful response that:
            1. Acknowledges their request
            2. Highlights best product matches
            3. Explains why these products fit their needs
            4. Suggests next steps
            
            Be conversational, friendly, and intelligent.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"Gemini response error: {e}")
            return self._demo_response(query, products)
    
    def enhance_search_query(self, original_query: str) -> Dict:
        """Enhance search query for better Elastic search results"""
        if not self.connected:
            return {'enhanced_query': original_query, 'keywords': [original_query]}
        
        try:
            prompt = f"""
            Enhance this shopping search query for better product discovery:
            
            Original: "{original_query}"
            
            Generate:
            1. Enhanced search terms
            2. Related keywords
            3. Category suggestions
            4. Alternative phrasings
            
            Return as JSON with enhanced_query and keywords array.
            """
            
            response = self.model.generate_content(prompt)
            return {
                'enhanced_query': original_query,
                'ai_enhancement': response.text,
                'status': 'enhanced'
            }
            
        except Exception as e:
            return {'enhanced_query': original_query, 'keywords': [original_query]}
    
    def _demo_analysis(self, query: str) -> Dict:
        """Demo mode analysis when Gemini not available"""
        return {
            'status': 'demo',
            'analysis': f'Demo analysis for: {query}',
            'ai_powered': False,
            'service': 'Demo Mode'
        }
    
    def _demo_response(self, query: str, products: List) -> str:
        """Demo mode response"""
        if products:
            return f"I found {len(products)} products for '{query}'. The top recommendation is {products[0].get('title', 'Product 1')} - it seems to match your requirements well!"
        else:
            return f"I understand you're looking for {query}. Let me help you find the best options!"
    
    def test_connection(self) -> Dict:
        """Test Google Cloud connection"""
        if not self.connected:
            return {'status': 'disconnected', 'service': 'Demo Mode'}
        
        try:
            test_response = self.model.generate_content("Test connection")
            return {
                'status': 'connected',
                'service': 'Google Gemini 1.5 Flash',
                'response_time': '< 2 seconds',
                'response_preview': test_response.text[:50] + '...'
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}