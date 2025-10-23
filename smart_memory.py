"""
Smart Shopping Memory - AI-powered user preference learning and personalization
Remembers user behavior, preferences, and provides intelligent recommendations
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import numpy as np
from collections import defaultdict
import pickle

class SmartShoppingMemory:
    def __init__(self, db_path="shopping_memory.db"):
        self.db_path = db_path
        self.user_profiles = {}
        self.conversation_history = []
        self.learning_model = UserPreferenceLearner()
        self.initialize_database()
    
    def initialize_database(self):
        """Initialize SQLite database for persistent memory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                category TEXT,
                preference_type TEXT,
                preference_value TEXT,
                confidence_score REAL,
                last_updated TIMESTAMP,
                frequency INTEGER DEFAULT 1
            )
        ''')
        
        # Shopping history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shopping_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                session_id TEXT,
                query TEXT,
                products_viewed TEXT,
                products_added_to_cart TEXT,
                final_purchase TEXT,
                timestamp TIMESTAMP,
                satisfaction_score REAL
            )
        ''')
        
        # Conversation memory table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                conversation_text TEXT,
                intent_detected TEXT,
                context_data TEXT,
                response_generated TEXT,
                timestamp TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Smart memory database initialized")
    
    def learn_from_conversation(self, user_id: str, conversation: str, products_shown: List, user_actions: Dict):
        """Learn user preferences from conversation and actions"""
        
        learning_insights = {
            'preferences_detected': [],
            'behavior_patterns': [],
            'confidence_updates': {},
            'personalization_improvements': []
        }
        
        # Extract preferences from conversation
        preferences = self.extract_preferences_from_text(conversation)
        
        # Learn from user actions (clicks, cart additions, purchases)
        action_insights = self.analyze_user_actions(user_actions, products_shown)
        
        # Update user profile
        for preference in preferences + action_insights:
            self.update_user_preference(
                user_id, 
                preference['category'],
                preference['type'],
                preference['value'],
                preference['confidence']
            )
            learning_insights['preferences_detected'].append(preference)
        
        # Detect behavior patterns
        patterns = self.detect_behavior_patterns(user_id, conversation, user_actions)
        learning_insights['behavior_patterns'] = patterns
        
        # Store conversation for future learning
        self.store_conversation_memory(user_id, conversation, products_shown, user_actions)
        
        return learning_insights
    
    def extract_preferences_from_text(self, text: str) -> List[Dict]:
        """Extract shopping preferences from natural language"""
        preferences = []
        
        # Brand preferences
        brand_keywords = {
            'apple': 0.9, 'samsung': 0.9, 'oneplus': 0.8, 'xiaomi': 0.8,
            'nike': 0.9, 'adidas': 0.9, 'puma': 0.8, 'reebok': 0.7,
            'sony': 0.9, 'bose': 0.9, 'jbl': 0.8
        }
        
        for brand, confidence in brand_keywords.items():
            if brand.lower() in text.lower():
                preferences.append({
                    'category': 'brand_preference',
                    'type': 'preferred_brand',
                    'value': brand.title(),
                    'confidence': confidence
                })
        
        # Budget preferences
        budget_patterns = [
            r'under (\d+)', r'below (\d+)', r'less than (\d+)', 
            r'around (\d+)', r'budget (\d+)', r'(\d+) range'
        ]
        
        import re
        for pattern in budget_patterns:
            match = re.search(pattern, text.lower())
            if match:
                budget = int(match.group(1))
                preferences.append({
                    'category': 'budget_preference',
                    'type': 'max_budget',
                    'value': str(budget),
                    'confidence': 0.8
                })
        
        # Category preferences
        category_keywords = {
            'gaming': ['gaming', 'games', 'fps', 'performance'],
            'photography': ['camera', 'photos', 'photography', 'selfie'],
            'music': ['music', 'audio', 'sound', 'headphones'],
            'fitness': ['fitness', 'workout', 'gym', 'running'],
            'work': ['work', 'office', 'professional', 'business']
        }
        
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in text.lower():
                    preferences.append({
                        'category': 'usage_preference',
                        'type': 'primary_use',
                        'value': category,
                        'confidence': 0.7
                    })
                    break
        
        return preferences
    
    def analyze_user_actions(self, actions: Dict, products: List) -> List[Dict]:
        """Analyze user actions to infer preferences"""
        action_insights = []
        
        # Analyze clicked products
        if actions.get('clicked_products'):
            clicked_products = actions['clicked_products']
            
            # Brand preference from clicks
            brands = [p.get('brand') for p in clicked_products if p.get('brand')]
            if brands:
                most_clicked_brand = max(set(brands), key=brands.count)
                action_insights.append({
                    'category': 'brand_preference',
                    'type': 'clicked_brand',
                    'value': most_clicked_brand,
                    'confidence': 0.6
                })
            
            # Price range preference from clicks
            prices = [p.get('price') for p in clicked_products if p.get('price')]
            if prices:
                avg_price = sum(prices) / len(prices)
                action_insights.append({
                    'category': 'budget_preference',
                    'type': 'preferred_range',
                    'value': str(int(avg_price)),
                    'confidence': 0.5
                })
        
        # Analyze cart additions
        if actions.get('added_to_cart'):
            cart_items = actions['added_to_cart']
            
            # Strong signal for actual purchase intent
            for item in cart_items:
                if item.get('category'):
                    action_insights.append({
                        'category': 'purchase_intent',
                        'type': 'high_interest_category',
                        'value': item['category'],
                        'confidence': 0.9
                    })
        
        return action_insights
    
    def get_personalized_recommendations(self, user_id: str, query: str, products: List) -> Dict:
        """Generate personalized recommendations based on learned preferences"""
        
        user_profile = self.get_user_profile(user_id)
        
        personalized_results = {
            'original_products': products,
            'personalized_ranking': [],
            'personalization_reasons': [],
            'confidence_score': 0.0,
            'learning_insights': {}
        }
        
        if not user_profile:
            # No profile yet - return original ranking
            personalized_results['personalized_ranking'] = products
            personalized_results['learning_insights']['message'] = "Building your profile - ask more questions!"
            return personalized_results
        
        # Score products based on user preferences
        scored_products = []
        
        for product in products:
            score = self.calculate_personalization_score(product, user_profile)
            reasons = self.get_personalization_reasons(product, user_profile)
            
            scored_products.append({
                'product': product,
                'personalization_score': score,
                'reasons': reasons
            })
        
        # Sort by personalization score
        scored_products.sort(key=lambda x: x['personalization_score'], reverse=True)
        
        personalized_results['personalized_ranking'] = [sp['product'] for sp in scored_products]
        personalized_results['personalization_reasons'] = [sp['reasons'] for sp in scored_products]
        personalized_results['confidence_score'] = self.calculate_overall_confidence(user_profile)
        
        # Generate learning insights
        personalized_results['learning_insights'] = self.generate_learning_insights(user_profile, query)
        
        return personalized_results
    
    def calculate_personalization_score(self, product: Dict, user_profile: Dict) -> float:
        """Calculate how well a product matches user preferences"""
        score = 0.0
        max_score = 0.0
        
        # Brand preference matching
        if product.get('brand') and 'brand_preference' in user_profile:
            brand_prefs = user_profile['brand_preference']
            if product['brand'].lower() in [bp['value'].lower() for bp in brand_prefs]:
                matching_pref = next(bp for bp in brand_prefs if bp['value'].lower() == product['brand'].lower())
                score += matching_pref['confidence'] * matching_pref['frequency'] * 0.3
            max_score += 0.3
        
        # Budget preference matching
        if product.get('price') and 'budget_preference' in user_profile:
            budget_prefs = user_profile['budget_preference']
            for budget_pref in budget_prefs:
                if budget_pref['type'] == 'max_budget':
                    max_budget = float(budget_pref['value'])
                    if product['price'] <= max_budget:
                        # Score higher for products closer to budget
                        budget_score = (max_budget - product['price']) / max_budget * 0.25
                        score += budget_score * budget_pref['confidence']
                    max_score += 0.25
        
        # Category/Usage preference matching
        if product.get('category') and 'usage_preference' in user_profile:
            usage_prefs = user_profile['usage_preference']
            for usage_pref in usage_prefs:
                if usage_pref['value'].lower() in product.get('description', '').lower():
                    score += usage_pref['confidence'] * usage_pref['frequency'] * 0.2
            max_score += 0.2
        
        # Purchase history matching
        if 'purchase_intent' in user_profile:
            intent_prefs = user_profile['purchase_intent']
            for intent in intent_prefs:
                if intent['value'].lower() == product.get('category', '').lower():
                    score += intent['confidence'] * 0.25
            max_score += 0.25
        
        return score / max_score if max_score > 0 else 0.0
    
    def generate_contextual_insights(self, user_id: str) -> Dict:
        """Generate insights about user's shopping behavior and preferences"""
        
        user_profile = self.get_user_profile(user_id)
        shopping_history = self.get_shopping_history(user_id)
        
        insights = {
            'personality_insights': [],
            'shopping_patterns': [],
            'recommendations': [],
            'next_actions': []
        }
        
        if not user_profile:
            insights['recommendations'].append("Start shopping to help me learn your preferences!")
            return insights
        
        # Analyze shopping personality
        if 'budget_preference' in user_profile:
            avg_budget = np.mean([float(bp['value']) for bp in user_profile['budget_preference']])
            if avg_budget < 15000:
                insights['personality_insights'].append("You're a budget-conscious shopper who values great deals!")
            elif avg_budget > 50000:
                insights['personality_insights'].append("You prefer premium products and quality over price!")
            else:
                insights['personality_insights'].append("You balance quality and value in your purchases!")
        
        # Brand loyalty analysis
        if 'brand_preference' in user_profile:
            brand_counts = {}
            for bp in user_profile['brand_preference']:
                brand_counts[bp['value']] = bp['frequency']
            
            if len(brand_counts) <= 2:
                top_brand = max(brand_counts, key=brand_counts.get)
                insights['personality_insights'].append(f"You're loyal to {top_brand} - I'll prioritize their products!")
            else:
                insights['personality_insights'].append("You like to explore different brands - I'll show you variety!")
        
        # Shopping pattern analysis
        recent_searches = self.get_recent_conversation_patterns(user_id)
        if recent_searches:
            popular_categories = self.extract_popular_categories(recent_searches)
            insights['shopping_patterns'] = [f"You frequently search for {cat}" for cat in popular_categories[:3]]
        
        # Proactive recommendations
        insights['recommendations'] = self.generate_proactive_recommendations(user_profile, shopping_history)
        
        return insights
    
    def update_user_preference(self, user_id: str, category: str, pref_type: str, value: str, confidence: float):
        """Update user preference in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if preference exists
        cursor.execute('''
            SELECT id, frequency, confidence_score FROM user_preferences 
            WHERE user_id = ? AND category = ? AND preference_type = ? AND preference_value = ?
        ''', (user_id, category, pref_type, value))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update existing preference
            new_frequency = existing[1] + 1
            new_confidence = (existing[2] + confidence) / 2  # Average confidence
            
            cursor.execute('''
                UPDATE user_preferences 
                SET frequency = ?, confidence_score = ?, last_updated = ?
                WHERE id = ?
            ''', (new_frequency, new_confidence, datetime.now(), existing[0]))
        else:
            # Insert new preference
            cursor.execute('''
                INSERT INTO user_preferences 
                (user_id, category, preference_type, preference_value, confidence_score, last_updated, frequency)
                VALUES (?, ?, ?, ?, ?, ?, 1)
            ''', (user_id, category, pref_type, value, confidence, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def get_user_profile(self, user_id: str) -> Dict:
        """Get complete user profile from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT category, preference_type, preference_value, confidence_score, frequency
            FROM user_preferences WHERE user_id = ?
        ''', (user_id,))
        
        preferences = cursor.fetchall()
        conn.close()
        
        profile = defaultdict(list)
        for pref in preferences:
            profile[pref[0]].append({
                'type': pref[1],
                'value': pref[2],
                'confidence': pref[3],
                'frequency': pref[4]
            })
        
        return dict(profile)
    
    def get_shopping_history(self, user_id: str) -> List[Dict]:
        """Get user's shopping history from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT query, products_viewed, products_added_to_cart, final_purchase, timestamp
            FROM shopping_history WHERE user_id = ?
            ORDER BY timestamp DESC LIMIT 50
        ''', (user_id,))
        
        history = cursor.fetchall()
        conn.close()
        
        return [
            {
                'query': h[0],
                'products_viewed': json.loads(h[1]) if h[1] else [],
                'products_added_to_cart': json.loads(h[2]) if h[2] else [],
                'final_purchase': json.loads(h[3]) if h[3] else None,
                'timestamp': h[4]
            }
            for h in history
        ]
    
    def store_conversation_memory(self, user_id: str, conversation: str, products: List, actions: Dict):
        """Store conversation in memory database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversation_memory 
            (user_id, conversation_text, intent_detected, context_data, response_generated, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_id, 
            conversation, 
            actions.get('intent', 'search'),
            json.dumps({'products': len(products), 'actions': list(actions.keys())}),
            'AI response generated',
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
    
    def detect_behavior_patterns(self, user_id: str, conversation: str, actions: Dict) -> List[str]:
        """Detect user behavior patterns"""
        patterns = []
        
        # Pattern 1: Time-based shopping
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 11:
            patterns.append("Morning shopper - you like to browse deals early!")
        elif 20 <= current_hour <= 23:
            patterns.append("Evening shopper - you prefer to shop after work!")
        
        # Pattern 2: Query complexity
        if len(conversation.split()) > 10:
            patterns.append("Detailed searcher - you know exactly what you want!")
        else:
            patterns.append("Quick searcher - you like to browse and discover!")
        
        # Pattern 3: Budget mentions
        budget_words = ['budget', 'cheap', 'affordable', 'under', 'below']
        if any(word in conversation.lower() for word in budget_words):
            patterns.append("Budget-conscious - you always look for great value!")
        
        return patterns
    
    def get_recent_conversation_patterns(self, user_id: str) -> List[str]:
        """Get recent conversation patterns"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT conversation_text FROM conversation_memory 
            WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10
        ''', (user_id,))
        
        conversations = cursor.fetchall()
        conn.close()
        
        return [conv[0] for conv in conversations]
    
    def extract_popular_categories(self, conversations: List[str]) -> List[str]:
        """Extract popular categories from conversations"""
        category_keywords = {
            'electronics': ['laptop', 'phone', 'mobile', 'tablet', 'computer'],
            'fashion': ['shirt', 'dress', 'shoes', 'clothing', 'fashion'],
            'beauty': ['makeup', 'skincare', 'cosmetics', 'beauty'],
            'sports': ['gym', 'fitness', 'sports', 'workout'],
            'home': ['furniture', 'home', 'kitchen', 'decor']
        }
        
        category_counts = defaultdict(int)
        
        for conversation in conversations:
            for category, keywords in category_keywords.items():
                if any(keyword in conversation.lower() for keyword in keywords):
                    category_counts[category] += 1
        
        # Sort by frequency
        popular_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        return [cat[0] for cat in popular_categories]
    
    def generate_proactive_recommendations(self, user_profile: Dict, shopping_history: List) -> List[str]:
        """Generate proactive recommendations"""
        recommendations = []
        
        # Based on brand preferences
        if 'brand_preference' in user_profile:
            top_brand = max(user_profile['brand_preference'], key=lambda x: x['frequency'])
            recommendations.append(f"Check out new {top_brand['value']} products that just launched!")
        
        # Based on budget patterns
        if 'budget_preference' in user_profile:
            avg_budget = sum(float(bp['value']) for bp in user_profile['budget_preference']) / len(user_profile['budget_preference'])
            recommendations.append(f"I found great deals under ₹{int(avg_budget)} in your favorite categories!")
        
        # Based on usage patterns
        if 'usage_preference' in user_profile:
            top_usage = max(user_profile['usage_preference'], key=lambda x: x['frequency'])
            recommendations.append(f"New {top_usage['value']} products are trending - want to see them?")
        
        return recommendations[:3]  # Return top 3
    
    def get_personalization_reasons(self, product: Dict, user_profile: Dict) -> List[str]:
        """Get reasons for personalization"""
        reasons = []
        
        # Brand matching
        if product.get('brand') and 'brand_preference' in user_profile:
            for bp in user_profile['brand_preference']:
                if bp['value'].lower() == product['brand'].lower():
                    reasons.append(f"You love {product['brand']} products")
        
        # Budget matching
        if product.get('price') and 'budget_preference' in user_profile:
            for bp in user_profile['budget_preference']:
                if float(bp['value']) >= product['price']:
                    reasons.append(f"Within your budget of ₹{bp['value']}")
        
        # Category matching
        if product.get('category') and 'usage_preference' in user_profile:
            for up in user_profile['usage_preference']:
                if up['value'].lower() in product.get('description', '').lower():
                    reasons.append(f"Matches your interest in {up['value']}")
        
        return reasons[:2]  # Return top 2 reasons
    
    def calculate_overall_confidence(self, user_profile: Dict) -> float:
        """Calculate overall confidence in user profile"""
        if not user_profile:
            return 0.0
        
        total_confidence = 0.0
        total_preferences = 0
        
        for category, preferences in user_profile.items():
            for pref in preferences:
                total_confidence += pref['confidence'] * pref['frequency']
                total_preferences += pref['frequency']
        
        return total_confidence / total_preferences if total_preferences > 0 else 0.0
    
    def generate_learning_insights(self, user_profile: Dict, query: str) -> Dict:
        """Generate learning insights for the user"""
        insights = {
            'new_preferences_learned': [],
            'confidence_updates': [],
            'behavior_patterns': [],
            'recommendations_reason': []
        }
        
        # Analyze what we learned from this query
        if user_profile:
            # Check for new brand preferences
            if 'brand_preference' in user_profile:
                for brand in user_profile['brand_preference']:
                    if brand['frequency'] == 1:  # New brand discovered
                        insights['new_preferences_learned'].append(f"Discovered you like {brand['value']} products")
            
            # Check for budget insights
            if 'budget_preference' in user_profile:
                for budget in user_profile['budget_preference']:
                    if budget['confidence'] > 0.7:
                        insights['confidence_updates'].append(f"High confidence in ₹{budget['value']} budget range")
            
            # Check for usage patterns
            if 'usage_preference' in user_profile:
                for usage in user_profile['usage_preference']:
                    if usage['frequency'] > 2:
                        insights['behavior_patterns'].append(f"Strong interest in {usage['value']} products")
        
        # Analyze current query for insights
        query_lower = query.lower()
        
        # Budget analysis
        budget_words = ['under', 'below', 'within', 'budget', 'cheap', 'affordable']
        if any(word in query_lower for word in budget_words):
            insights['recommendations_reason'].append("Prioritizing budget-friendly options")
        
        # Quality analysis
        quality_words = ['best', 'top', 'premium', 'high-quality', 'good']
        if any(word in query_lower for word in quality_words):
            insights['recommendations_reason'].append("Focusing on high-quality products")
        
        # Usage analysis
        usage_words = ['gaming', 'office', 'home', 'travel', 'workout', 'professional']
        for word in usage_words:
            if word in query_lower:
                insights['recommendations_reason'].append(f"Tailored for {word} use")
                break
        
        return insights

class UserPreferenceLearner:
    """ML-based user preference learning"""
    
    def __init__(self):
        self.model = None
        self.feature_extractor = None
    
    def train_from_interactions(self, interaction_data: List[Dict]):
        """Train model from user interaction data"""
        # Implementation for ML-based preference learning
        pass
    
    def predict_user_preferences(self, user_behavior: Dict) -> Dict:
        """Predict user preferences using ML model"""
        # Implementation for preference prediction
        pass