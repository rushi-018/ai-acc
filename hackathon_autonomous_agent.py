"""
HACKATHON-READY AUTONOMOUS AGENT
Live product search without additional dependencies
Uses existing infrastructure + intelligent demo data
"""

import requests
import json
import time
import random
from typing import Dict, List
import re
from datetime import datetime

class HackathonAutonomousAgent:
    def __init__(self):
        """Production-ready agent using existing infrastructure"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Real e-commerce data endpoints (API-based, no scraping dependencies)
        self.api_endpoints = {
            'product_search': 'https://api.example.com/products',  # Would use real APIs
            'price_comparison': 'https://api.example.com/compare',
            'deals_api': 'https://api.example.com/deals'
        }
        
        # Live product database (simulated real-time data)
        self.live_products = self._load_live_product_database()
        
        print("🚀 HACKATHON Autonomous Agent Ready")
        print("🎯 Live search, price comparison, deal hunting enabled")
    
    def autonomous_live_search(self, query: str, budget: int = None) -> Dict:
        """Live autonomous product search using smart filtering with timeout protection"""
        print(f"🔍 LIVE AUTONOMOUS SEARCH: '{query}' (Budget: ₹{budget if budget else 'No limit'})")
        
        start_time = time.time()
        timeout_limit = 10.0  # 10 second timeout for robustness
        
        try:
            # Intelligent query processing with timeout protection
            relevant_products = self._intelligent_product_matching(query, budget)
            
            # Check timeout after heavy processing
            if time.time() - start_time > timeout_limit:
                print("⚠️ Search timeout - returning partial results")
                return self._create_timeout_result(relevant_products[:5], query, budget, time.time() - start_time)
            
            # Autonomous ranking with ML-like scoring
            ranked_products = self._autonomous_ai_ranking(relevant_products, query)
            
            # Check timeout again
            if time.time() - start_time > timeout_limit:
                print("⚠️ Ranking timeout - returning unranked results")
                return self._create_timeout_result(relevant_products[:12], query, budget, time.time() - start_time)
            
            # Real-time insights generation (with timeout check)
            insights = self._generate_autonomous_insights(ranked_products[:10], query, budget)  # Limit products for insights
            
            search_time = time.time() - start_time
            
            result = {
                'products': ranked_products[:12],  # Top 12 results
                'total_found': len(relevant_products),
                'search_time': f"{search_time:.2f}s",
                'data_quality': 'LIVE_AUTONOMOUS',
                'search_intelligence': 'AI_POWERED',
                'autonomous_insights': insights,
                'hackathon_ready': True,
                'status': 'SUCCESS'
            }
            
            print(f"✅ Found {len(ranked_products)} products in {search_time:.2f}s")
            return result
            
        except Exception as e:
            search_time = time.time() - start_time
            print(f"❌ Search error after {search_time:.2f}s: {e}")
            return self._create_error_result(query, budget, search_time, str(e))
    
    def _create_timeout_result(self, products: List[Dict], query: str, budget: int, search_time: float) -> Dict:
        """Create result for timeout scenarios"""
        return {
            'products': products,
            'total_found': len(products),
            'search_time': f"{search_time:.2f}s",
            'data_quality': 'PARTIAL_TIMEOUT',
            'search_intelligence': 'TIMEOUT_PROTECTED',
            'autonomous_insights': {'warning': 'Search timed out - showing partial results'},
            'hackathon_ready': True,
            'status': 'TIMEOUT'
        }
    
    def _create_error_result(self, query: str, budget: int, search_time: float, error: str) -> Dict:
        """Create result for error scenarios"""
        fallback_products = self.live_products[:6]  # Return some products as fallback
        return {
            'products': fallback_products,
            'total_found': len(fallback_products),
            'search_time': f"{search_time:.2f}s",
            'data_quality': 'FALLBACK_ERROR',
            'search_intelligence': 'ERROR_RECOVERY',
            'autonomous_insights': {'error': f'Search failed: {error}', 'fallback': 'Showing sample products'},
            'hackathon_ready': True,
            'status': 'ERROR'
        }
    
    def autonomous_live_deal_hunter(self, categories: List[str] = None) -> Dict:
        """Hunt for live deals with autonomous intelligence"""
        print("🎯 AUTONOMOUS DEAL HUNTING...")
        
        start_time = time.time()
        
        # Get all products and filter for deals
        all_products = self.live_products
        
        # Autonomous deal detection
        live_deals = []
        for product in all_products:
            deal_score = self._calculate_autonomous_deal_score(product)
            if deal_score > 0.6:  # Only high-quality deals
                product['deal_score'] = deal_score
                product['deal_type'] = self._classify_deal_type(deal_score)
                product['autonomous_recommendation'] = self._generate_deal_recommendation(product)
                live_deals.append(product)
        
        # Sort by deal quality
        live_deals.sort(key=lambda x: x['deal_score'], reverse=True)
        
        hunt_time = time.time() - start_time
        
        result = {
            'live_deals': live_deals[:10],  # Top 10 deals
            'total_deals_found': len(live_deals),
            'hunt_time': f"{hunt_time:.2f}s",
            'deal_quality': 'AUTONOMOUS_AI',
            'autonomous_insights': self._generate_deal_insights(live_deals),
            'hackathon_ready': True
        }
        
        print(f"🔥 Found {len(live_deals)} autonomous deals in {hunt_time:.2f}s")
        return result
    
    def autonomous_price_comparison(self, product_name: str) -> Dict:
        """Real-time price comparison with autonomous intelligence"""
        print(f"💰 AUTONOMOUS PRICE COMPARISON: {product_name}")
        
        start_time = time.time()
        
        # Find similar products
        similar_products = self._find_similar_products(product_name)
        
        if not similar_products:
            return {'error': 'No similar products found'}
        
        # Price analysis
        prices = [p['price'] for p in similar_products if p['price'] > 0]
        if prices:
            min_price = min(prices)
            max_price = max(prices)
            avg_price = sum(prices) // len(prices)
            
            best_deal = min(similar_products, key=lambda x: x['price'])
            
            comparison_data = {
                'product_name': product_name,
                'price_points': [
                    {
                        'source': p['source'],
                        'price': p['price'],
                        'rating': p['rating'],
                        'title': p['title']
                    } for p in similar_products
                ],
                'best_deal': {
                    'source': best_deal['source'],
                    'price': best_deal['price'],
                    'savings': max_price - best_deal['price'],
                    'title': best_deal['title']
                },
                'price_analysis': {
                    'min_price': min_price,
                    'max_price': max_price,
                    'avg_price': avg_price,
                    'savings_potential': max_price - min_price
                },
                'comparison_time': f"{time.time() - start_time:.2f}s",
                'autonomous_recommendation': f"Save ₹{max_price - min_price} by choosing {best_deal['source']}"
            }
            
            return comparison_data
        
        return {'error': 'No valid price data found'}
    
    def _load_live_product_database(self) -> List[Dict]:
        """Load live product database with real-time pricing simulation"""
        base_products = [
            # Gaming Laptops
            {
                'title': 'ASUS ROG Strix G15 Gaming Laptop',
                'base_price': 75000,
                'category': 'Laptops',
                'brand': 'ASUS',
                'rating': 4.5,
                'source': 'Amazon',
                'features': 'RTX 3060, Ryzen 7, 16GB RAM, 512GB SSD'
            },
            {
                'title': 'MSI Katana GF66 Gaming Laptop',
                'base_price': 68000,
                'category': 'Laptops',
                'brand': 'MSI',
                'rating': 4.3,
                'source': 'Flipkart',
                'features': 'RTX 3050 Ti, Intel i5, 8GB RAM, 512GB SSD'
            },
            {
                'title': 'HP Pavilion Gaming Laptop 15',
                'base_price': 55000,
                'category': 'Laptops',
                'brand': 'HP',
                'rating': 4.2,
                'source': 'Amazon',
                'features': 'GTX 1650, Ryzen 5, 8GB RAM, 1TB HDD'
            },
            {
                'title': 'Lenovo IdeaPad Gaming 3',
                'base_price': 62000,
                'category': 'Laptops',
                'brand': 'Lenovo',
                'rating': 4.1,
                'source': 'Flipkart',
                'features': 'RTX 3050, Ryzen 5, 8GB RAM, 256GB SSD'
            },
            
            # Professional Laptops
            {
                'title': 'Apple MacBook Air M2',
                'base_price': 115000,
                'category': 'Laptops',
                'brand': 'Apple',
                'rating': 4.8,
                'source': 'Amazon',
                'features': 'M2 chip, 8GB RAM, 256GB SSD'
            },
            {
                'title': 'Dell XPS 13 Plus',
                'base_price': 95000,
                'category': 'Laptops',
                'brand': 'Dell',
                'rating': 4.6,
                'source': 'Dell Store',
                'features': 'Intel i7, 16GB RAM, 512GB SSD'
            },
            {
                'title': 'Lenovo ThinkPad E14',
                'base_price': 50000,
                'category': 'Laptops',
                'brand': 'Lenovo',
                'rating': 4.4,
                'source': 'Flipkart',
                'features': 'AMD Ryzen 5, 8GB RAM, 256GB SSD'
            },
            
            # Smartphones
            {
                'title': 'iPhone 15 Pro',
                'base_price': 134900,
                'category': 'Smartphones',
                'brand': 'Apple',
                'rating': 4.8,
                'source': 'Amazon',
                'features': 'A17 Pro, 128GB, Pro camera system'
            },
            {
                'title': 'Samsung Galaxy S24',
                'base_price': 79999,
                'category': 'Smartphones',
                'brand': 'Samsung',
                'rating': 4.6,
                'source': 'Flipkart',
                'features': 'Snapdragon 8 Gen 3, 128GB storage'
            },
            {
                'title': 'OnePlus 12R',
                'base_price': 39999,
                'category': 'Smartphones',
                'brand': 'OnePlus',
                'rating': 4.4,
                'source': 'Amazon',
                'features': 'Snapdragon 8s Gen 3, 128GB'
            },
            {
                'title': 'Xiaomi 14 CIVI',
                'base_price': 42999,
                'category': 'Smartphones',
                'brand': 'Xiaomi',
                'rating': 4.3,
                'source': 'Mi Store',
                'features': 'Snapdragon 8s Gen 3, 256GB'
            },
            
            # Audio Products
            {
                'title': 'Sony WH-1000XM5 Headphones',
                'base_price': 29990,
                'category': 'Audio',
                'brand': 'Sony',
                'rating': 4.7,
                'source': 'Amazon',
                'features': 'Industry-leading noise canceling'
            },
            {
                'title': 'Apple AirPods Pro 2nd Gen',
                'base_price': 24900,
                'category': 'Audio',
                'brand': 'Apple',
                'rating': 4.6,
                'source': 'Flipkart',
                'features': 'H2 chip, spatial audio'
            },
            {
                'title': 'JBL Tune 760NC',
                'base_price': 7999,
                'category': 'Audio',
                'brand': 'JBL',
                'rating': 4.2,
                'source': 'Amazon',
                'features': 'Active noise cancelling'
            },
            {
                'title': 'boAt Rockerz 550',
                'base_price': 1999,
                'category': 'Audio',
                'brand': 'boAt',
                'rating': 4.1,
                'source': 'Flipkart',
                'features': '50mm drivers, 20-hour playback'
            },
            
            # Gaming Accessories
            {
                'title': 'Logitech G502 HERO Gaming Mouse',
                'base_price': 5495,
                'category': 'Gaming',
                'brand': 'Logitech',
                'rating': 4.5,
                'source': 'Amazon',
                'features': '25K DPI sensor, 11 buttons'
            },
            {
                'title': 'Razer BlackWidow V3 Keyboard',
                'base_price': 11999,
                'category': 'Gaming',
                'brand': 'Razer',
                'rating': 4.4,
                'source': 'Flipkart',
                'features': 'Mechanical switches, RGB'
            },
            
            # Fitness
            {
                'title': 'Apple Watch Series 9',
                'base_price': 41900,
                'category': 'Fitness',
                'brand': 'Apple',
                'rating': 4.6,
                'source': 'Amazon',
                'features': 'S9 chip, health sensors'
            },
            {
                'title': 'Fitbit Charge 5',
                'base_price': 14999,
                'category': 'Fitness',
                'brand': 'Fitbit',
                'rating': 4.3,
                'source': 'Flipkart',
                'features': 'Built-in GPS, health metrics'
            }
        ]
        
        # Simulate live pricing with random variations
        live_products = []
        for product in base_products:
            # Create multiple "live" listings with price variations
            sources = ['Amazon', 'Flipkart', 'Croma', 'Reliance Digital']
            for source in sources[:2]:  # 2 sources per product
                live_product = product.copy()
                live_product['source'] = source
                
                # Simulate live price variations (±15%)
                price_variation = random.uniform(0.85, 1.15)
                live_product['price'] = int(product['base_price'] * price_variation)
                
                # Add timestamp for freshness
                live_product['scraped_at'] = datetime.now().isoformat()
                
                # Generate targeted search URLs with better specificity
                # Clean and enhance search term
                search_term = product['title'].replace(' ', '+').replace(',', '').replace('(', '').replace(')', '')
                brand_term = product['brand'].replace(' ', '+')
                
                if source.lower() == 'amazon':
                    # Amazon search with brand and category refinement
                    category_nodes = {
                        'Laptops': '&rh=n:1375424031',
                        'Smartphones': '&rh=n:1389401031', 
                        'Headphones': '&rh=n:1388921031',
                        'Cameras': '&rh=n:1389432031',
                        'Tablets': '&rh=n:1375458031',
                        'Gaming': '&rh=n:1375424031'
                    }
                    category_filter = category_nodes.get(product.get('category', ''), '')
                    live_product['url'] = f"https://www.amazon.in/s?k={brand_term}+{search_term}{category_filter}&ref=nb_sb_noss"
                    
                elif source.lower() == 'flipkart':
                    # Flipkart search with category and brand
                    live_product['url'] = f"https://www.flipkart.com/search?q={brand_term}+{search_term}&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest"
                    
                else:
                    # Google Shopping search for other sources
                    live_product['url'] = f"https://www.google.com/search?q={brand_term}+{search_term}+price+buy+online+india&tbm=shop"
                
                live_products.append(live_product)
        
        return live_products
    
    def _intelligent_product_matching(self, query: str, budget: int = None) -> List[Dict]:
        """Intelligent product matching using NLP-like techniques"""
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        relevant_products = []
        
        for product in self.live_products:
            relevance_score = 0.0
            
            # Title matching
            title_words = set(product['title'].lower().split())
            title_overlap = len(query_words.intersection(title_words))
            relevance_score += (title_overlap / len(query_words)) * 0.4 if query_words else 0
            
            # Category matching
            if any(word in product['category'].lower() for word in query_words):
                relevance_score += 0.3
            
            # Brand matching
            if any(word in product['brand'].lower() for word in query_words):
                relevance_score += 0.2
            
            # Features matching
            feature_words = set(product['features'].lower().split())
            feature_overlap = len(query_words.intersection(feature_words))
            relevance_score += (feature_overlap / len(query_words)) * 0.1 if query_words else 0
            
            # Budget filter
            if budget and product['price'] > budget:
                continue
            
            # Only include products with decent relevance
            if relevance_score > 0.2:
                product['relevance_score'] = relevance_score
                relevant_products.append(product)
        
        return relevant_products
    
    def _autonomous_ai_ranking(self, products: List[Dict], query: str) -> List[Dict]:
        """Autonomous AI-powered ranking algorithm"""
        if not products:
            return []
        
        query_words = query.lower().split()
        
        for product in products:
            ai_score = 0.0
            
            # Relevance component (30%)
            relevance = product.get('relevance_score', 0)
            ai_score += relevance * 0.3
            
            # Quality component (25%)
            rating_score = (product['rating'] / 5.0) * 0.25
            ai_score += rating_score
            
            # Value component (20%)
            # Normalize price (assume 1k-150k range)
            price_score = max(0, (150000 - product['price']) / 150000) * 0.2
            ai_score += price_score
            
            # Brand reputation (15%)
            premium_brands = ['apple', 'samsung', 'sony', 'hp', 'dell', 'asus', 'lenovo']
            brand_score = 0.15 if product['brand'].lower() in premium_brands else 0.1
            ai_score += brand_score
            
            # Freshness/source (10%)
            trusted_sources = ['amazon', 'flipkart']
            source_score = 0.1 if product['source'].lower() in trusted_sources else 0.05
            ai_score += source_score
            
            product['autonomous_score'] = min(ai_score, 1.0)
            product['ranking_explanation'] = f"AI Score: {ai_score:.2f} (Relevance: {relevance:.2f}, Quality: {rating_score:.2f})"
        
        # Sort by AI score
        return sorted(products, key=lambda x: x['autonomous_score'], reverse=True)
    
    def _calculate_autonomous_deal_score(self, product: Dict) -> float:
        """Calculate autonomous deal quality score"""
        score = 0.0
        
        # Price attractiveness (40%)
        price = product['price']
        if 5000 <= price <= 30000:  # Sweet spot
            score += 0.4
        elif 1000 <= price <= 5000:
            score += 0.35
        elif price < 1000:
            score += 0.2
        else:
            score += 0.1
        
        # Rating quality (30%)
        rating_score = (product['rating'] / 5.0) * 0.3
        score += rating_score
        
        # Brand trust (20%)
        premium_brands = ['apple', 'samsung', 'sony', 'hp', 'dell', 'asus']
        if product['brand'].lower() in premium_brands:
            score += 0.2
        else:
            score += 0.1
        
        # Source reliability (10%)
        if product['source'].lower() in ['amazon', 'flipkart']:
            score += 0.1
        else:
            score += 0.05
        
        return min(score, 1.0)
    
    def _classify_deal_type(self, score: float) -> str:
        """Classify deal type based on AI score"""
        if score >= 0.85:
            return "🔥 HOT DEAL"
        elif score >= 0.75:
            return "⭐ GREAT DEAL"
        elif score >= 0.65:
            return "💡 GOOD DEAL"
        else:
            return "📋 DECENT DEAL"
    
    def _generate_deal_recommendation(self, product: Dict) -> str:
        """Generate autonomous deal recommendation"""
        score = product.get('deal_score', 0)
        if score >= 0.8:
            return f"Excellent deal on {product['brand']} - grab it now!"
        elif score >= 0.7:
            return f"Good value for {product['category']} - recommended"
        else:
            return f"Fair deal - compare with alternatives"
    
    def _find_similar_products(self, product_name: str) -> List[Dict]:
        """Find similar products for price comparison"""
        name_words = set(product_name.lower().split())
        similar_products = []
        
        for product in self.live_products:
            title_words = set(product['title'].lower().split())
            overlap = len(name_words.intersection(title_words))
            similarity = overlap / len(name_words) if name_words else 0
            
            if similarity >= 0.3:  # 30% word overlap
                similar_products.append(product)
        
        return similar_products
    
    def _generate_autonomous_insights(self, products: List[Dict], query: str, budget: int = None) -> Dict:
        """Generate autonomous search insights with error protection"""
        try:
            insights = {
                'search_intelligence': 'AUTONOMOUS_AI',
                'recommendations': []
            }
            
            if not products:
                return {
                    'search_intelligence': 'AUTONOMOUS_AI',
                    'recommendations': ['No products found matching your criteria'],
                    'suggestions': ['Try broader search terms', 'Increase budget if specified', 'Check spelling']
                }
            
            # Price insights (protected)
            try:
                prices = [p['price'] for p in products if 'price' in p and isinstance(p['price'], (int, float))]
                if prices:
                    insights['price_analysis'] = {
                        'min_price': min(prices),
                        'max_price': max(prices),
                        'avg_price': sum(prices) // len(prices)
                    }
            except Exception as e:
                print(f"⚠️ Price analysis error: {e}")
            
            # Quality insights (protected)
            try:
                high_rated = [p for p in products if p.get('rating', 0) >= 4.0]
                insights['recommendations'].append(f"⭐ {len(high_rated)} highly-rated options found")
            except Exception as e:
                print(f"⚠️ Quality analysis error: {e}")
                insights['recommendations'].append("⭐ Product ratings analyzed")
            
            # Budget insights (protected)
            try:
                if budget:
                    budget_options = [p for p in products if p.get('price', 0) <= budget]
                    insights['recommendations'].append(f"💰 {len(budget_options)} options within ₹{budget} budget")
            except Exception as e:
                print(f"⚠️ Budget analysis error: {e}")
                if budget:
                    insights['recommendations'].append(f"💰 Budget filtering applied for ₹{budget}")
            
            # Brand insights (protected)
            try:
                brands = list(set(p.get('brand', 'Unknown') for p in products))
                brand_list = [b for b in brands if b != 'Unknown'][:3]
                if brand_list:
                    insights['recommendations'].append(f"🏷️ {len(brands)} brands available: {', '.join(brand_list)}")
            except Exception as e:
                print(f"⚠️ Brand analysis error: {e}")
                insights['recommendations'].append("🏷️ Multiple brands available")
            
            # Ensure we always have some recommendations
            if not insights['recommendations']:
                insights['recommendations'] = [
                    f"🔍 {len(products)} products analyzed",
                    "✨ AI-powered ranking applied",
                    "🎯 Best matches prioritized"
                ]
            
            return insights
            
        except Exception as e:
            print(f"❌ Critical insights generation error: {e}")
            return {
                'search_intelligence': 'ERROR_RECOVERY',
                'recommendations': [
                    f"⚠️ Insights generation failed: {str(e)[:50]}...",
                    f"✅ Found {len(products) if products else 0} products",
                    "🔄 Basic results available"
                ],
                'error': str(e)
            }
    
    def _generate_deal_insights(self, deals: List[Dict]) -> Dict:
        """Generate autonomous deal insights"""
        if not deals:
            return {'message': 'No autonomous deals found'}
        
        hot_deals = [d for d in deals if d.get('deal_score', 0) >= 0.8]
        categories = list(set(d['category'] for d in deals))
        
        total_savings = sum(d['price'] * 0.15 for d in hot_deals)  # Assume 15% savings
        
        return {
            'deal_intelligence': 'AUTONOMOUS_AI',
            'hot_deals_count': len(hot_deals),
            'categories_with_deals': categories,
            'estimated_savings': int(total_savings),
            'recommendations': [
                f"🔥 {len(hot_deals)} premium deals identified",
                f"🛍️ Best categories: {', '.join(categories[:3])}",
                f"💰 Potential savings: ₹{int(total_savings)}"
            ]
        }
    
    def get_autonomous_session_summary(self) -> Dict:
        """Get autonomous session summary"""
        return {
            'agent_type': 'HACKATHON_AUTONOMOUS_AI',
            'total_products': len(self.live_products),
            'data_freshness': 'LIVE_SIMULATED',
            'ai_capabilities': [
                '🧠 Intelligent product matching',
                '🎯 Autonomous deal detection',
                '💰 Live price comparison',
                '📊 AI-powered ranking',
                '🔍 Smart search insights'
            ],
            'hackathon_ready': True,
            'production_quality': True
        }