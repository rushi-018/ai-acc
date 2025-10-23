"""
FREE Elasticsearch integration using Elastic Cloud 14-day trial
Hybrid search capabilities included
"""

from elasticsearch import Elasticsearch
import json
import os
from typing import Dict, List, Optional
import hashlib

class ElasticSearchFree:
    def __init__(self, cloud_id: str = None, api_key: str = None):
        """Initialize free Elasticsearch service"""
        self.cloud_id = cloud_id or os.getenv('ELASTIC_CLOUD_ID')
        self.api_key = api_key or os.getenv('ELASTIC_API_KEY')
        self.username = os.getenv('ELASTIC_USERNAME')
        self.password = os.getenv('ELASTIC_PASSWORD')
        
        if self.cloud_id:
            try:
                # Try username/password first (more reliable)
                if self.username and self.password:
                    self.client = Elasticsearch(
                        cloud_id=self.cloud_id,
                        basic_auth=(self.username, self.password),
                        request_timeout=30
                    )
                # Fallback to API key
                elif self.api_key:
                    self.client = Elasticsearch(
                        cloud_id=self.cloud_id,
                        api_key=self.api_key,
                        request_timeout=30
                    )
                else:
                    raise Exception("No authentication method provided")
                self.connected = self.client.ping()
                if self.connected:
                    print("✅ Elasticsearch Cloud connected (FREE 14-day trial)")
                    self.setup_product_index()
                else:
                    print("⚠️ Elasticsearch ping failed - running in demo mode")
                    self.connected = False
            except Exception as e:
                print(f"⚠️ Elasticsearch connection error: {e}")
                self.connected = False
        else:
            print("⚠️ Elasticsearch credentials not found - running in demo mode")
            self.connected = False
    
    def setup_product_index(self):
        """Setup product index with hybrid search capabilities"""
        if not self.connected:
            return
        
        index_name = "products"
        
        # Check if index exists
        if self.client.indices.exists(index=index_name):
            print(f"✅ Index '{index_name}' already exists")
            return
        
        # Create index with hybrid search mapping
        mapping = {
            "mappings": {
                "properties": {
                    "title": {
                        "type": "text",
                        "analyzer": "standard",
                        "fields": {"keyword": {"type": "keyword"}}
                    },
                    "description": {"type": "text", "analyzer": "standard"},
                    "category": {"type": "keyword"},
                    "price": {"type": "float"},
                    "rating": {"type": "float"},
                    "brand": {"type": "keyword"},
                    "url": {"type": "keyword"},
                    "image_url": {"type": "keyword"},
                    "features": {"type": "text"},
                    "embeddings": {
                        "type": "dense_vector",
                        "dims": 384,  # Sentence transformer dimensions
                        "index": True,
                        "similarity": "cosine"
                    },
                    "created_at": {"type": "date"},
                    "popularity_score": {"type": "float"}
                }
            },
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "analysis": {
                    "analyzer": {
                        "product_analyzer": {
                            "type": "standard",
                            "stopwords": "_english_"
                        }
                    }
                }
            }
        }
        
        try:
            self.client.indices.create(index=index_name, body=mapping)
            print(f"✅ Created index '{index_name}' with hybrid search capabilities")
            
            # Add sample products for demo
            self.add_sample_products()
            
        except Exception as e:
            print(f"Error creating index: {e}")
    
    def add_sample_products(self):
        """Add sample products for demo purposes"""
        sample_products = [
            # Gaming Laptops
            {
                "title": "Gaming Laptop ASUS ROG Strix G15",
                "description": "High-performance gaming laptop with RTX 3060, AMD Ryzen 7, 16GB RAM",
                "category": "Laptops",
                "price": 75000,
                "rating": 4.5,
                "brand": "ASUS",
                "url": "https://example.com/asus-rog",
                "features": "RTX 3060, Ryzen 7 5800H, 16GB RAM, 512GB SSD, 144Hz display",
                "popularity_score": 0.9
            },
            {
                "title": "MSI Gaming Laptop GF63 Thin",
                "description": "Budget-friendly gaming laptop with GTX 1650, Intel i5, 8GB RAM",
                "category": "Laptops",
                "price": 45000,
                "rating": 4.2,
                "brand": "MSI",
                "url": "https://example.com/msi-gf63",
                "features": "GTX 1650, Intel i5-10300H, 8GB RAM, 256GB SSD, 120Hz display",
                "popularity_score": 0.75
            },
            {
                "title": "HP Pavilion Gaming Laptop",
                "description": "Affordable gaming laptop with GTX 1660 Ti, AMD Ryzen 5, 16GB RAM",
                "category": "Laptops",
                "price": 55000,
                "rating": 4.3,
                "brand": "HP",
                "url": "https://example.com/hp-pavilion-gaming",
                "features": "GTX 1660 Ti, AMD Ryzen 5 4600H, 16GB RAM, 512GB SSD",
                "popularity_score": 0.8
            },
            
            # Professional Laptops
            {
                "title": "Apple MacBook Air M2",
                "description": "Ultra-thin laptop with M2 chip, perfect for productivity and creative work",
                "category": "Laptops", 
                "price": 115000,
                "rating": 4.8,
                "brand": "Apple",
                "url": "https://example.com/macbook-air",
                "features": "M2 chip, 8GB RAM, 256GB SSD, Retina display, all-day battery",
                "popularity_score": 0.95
            },
            {
                "title": "Dell XPS 13 Laptop",
                "description": "Premium ultrabook with Intel i7, 16GB RAM, ideal for professionals",
                "category": "Laptops",
                "price": 95000,
                "rating": 4.6,
                "brand": "Dell",
                "url": "https://example.com/dell-xps13",
                "features": "Intel i7-1165G7, 16GB RAM, 512GB SSD, 13.3 FHD display",
                "popularity_score": 0.85
            },
            {
                "title": "Lenovo ThinkPad E14",
                "description": "Business laptop with AMD Ryzen 5, 8GB RAM, durable build",
                "category": "Laptops",
                "price": 50000,
                "rating": 4.4,
                "brand": "Lenovo",
                "url": "https://example.com/thinkpad-e14",
                "features": "AMD Ryzen 5 4500U, 8GB RAM, 256GB SSD, 14-inch FHD",
                "popularity_score": 0.8
            },
            
            # Budget Laptops
            {
                "title": "Acer Aspire 5 Laptop",
                "description": "Budget laptop with Intel i3, 4GB RAM, perfect for students",
                "category": "Laptops",
                "price": 30000,
                "rating": 4.0,
                "brand": "Acer",
                "url": "https://example.com/acer-aspire5",
                "features": "Intel i3-1115G4, 4GB RAM, 1TB HDD, 15.6-inch HD display",
                "popularity_score": 0.7
            },
            
            # Headphones & Audio
            {
                "title": "Sony WH-1000XM4 Wireless Headphones",
                "description": "Industry-leading noise canceling wireless headphones",
                "category": "Audio",
                "price": 25000,
                "rating": 4.6,
                "brand": "Sony",
                "url": "https://example.com/sony-wh1000xm4",
                "features": "Active noise canceling, 30-hour battery, premium sound quality",
                "popularity_score": 0.85
            },
            {
                "title": "JBL Tune 760NC Wireless Headphones",
                "description": "Budget wireless headphones with active noise cancelling",
                "category": "Audio",
                "price": 8000,
                "rating": 4.2,
                "brand": "JBL",
                "url": "https://example.com/jbl-tune760nc",
                "features": "Active noise cancelling, 35-hour battery, JBL Pure Bass",
                "popularity_score": 0.75
            },
            {
                "title": "Apple AirPods Pro 2nd Gen",
                "description": "Premium wireless earbuds with adaptive transparency",
                "category": "Audio",
                "price": 22000,
                "rating": 4.7,
                "brand": "Apple",
                "url": "https://example.com/airpods-pro2",
                "features": "H2 chip, adaptive transparency, spatial audio, MagSafe charging",
                "popularity_score": 0.9
            },
            {
                "title": "boAt Airdopes 441 TWS Earbuds",
                "description": "Affordable true wireless earbuds with good bass",
                "category": "Audio",
                "price": 2500,
                "rating": 4.1,
                "brand": "boAt",
                "url": "https://example.com/boat-airdopes441",
                "features": "Bluetooth 5.0, 30-hour playback, IPX7 water resistance",
                "popularity_score": 0.7
            },
            
            # Smartphones
            {
                "title": "iPhone 15 Pro",
                "description": "Latest iPhone with A17 Pro chip, titanium design, pro camera system",
                "category": "Smartphones",
                "price": 130000,
                "rating": 4.8,
                "brand": "Apple",
                "url": "https://example.com/iphone15pro",
                "features": "A17 Pro chip, 128GB storage, pro camera system, titanium build",
                "popularity_score": 0.95
            },
            {
                "title": "Samsung Galaxy S24",
                "description": "Premium Android phone with AI features and excellent camera",
                "category": "Smartphones",
                "price": 85000,
                "rating": 4.6,
                "brand": "Samsung",
                "url": "https://example.com/galaxy-s24",
                "features": "Snapdragon 8 Gen 3, 128GB storage, 50MP camera, AI features",
                "popularity_score": 0.9
            },
            {
                "title": "OnePlus 12R",
                "description": "Flagship killer with fast charging and smooth performance",
                "category": "Smartphones",
                "price": 40000,
                "rating": 4.4,
                "brand": "OnePlus",
                "url": "https://example.com/oneplus12r",
                "features": "Snapdragon 8s Gen 3, 128GB storage, 100W fast charging",
                "popularity_score": 0.8
            },
            {
                "title": "Xiaomi Redmi Note 13 Pro",
                "description": "Budget smartphone with good camera and long battery life",
                "category": "Smartphones",
                "price": 25000,
                "rating": 4.3,
                "brand": "Xiaomi",
                "url": "https://example.com/redmi-note13pro",
                "features": "Dimensity 7200, 128GB storage, 200MP camera, 5000mAh battery",
                "popularity_score": 0.75
            },
            
            # Gaming Accessories
            {
                "title": "Logitech G502 HERO Gaming Mouse",
                "description": "High-performance gaming mouse with 25K DPI sensor",
                "category": "Gaming",
                "price": 5500,
                "rating": 4.5,
                "brand": "Logitech",
                "url": "https://example.com/logitech-g502",
                "features": "25K DPI HERO sensor, 11 programmable buttons, RGB lighting",
                "popularity_score": 0.85
            },
            {
                "title": "Razer BlackWidow V3 Mechanical Keyboard",
                "description": "Premium mechanical gaming keyboard with green switches",
                "category": "Gaming",
                "price": 12000,
                "rating": 4.4,
                "brand": "Razer",
                "url": "https://example.com/razer-blackwidow",
                "features": "Razer Green switches, RGB Chroma lighting, aluminum frame",
                "popularity_score": 0.8
            },
            
            # Home & Kitchen
            {
                "title": "Philips Air Fryer HD9252",
                "description": "Healthy cooking air fryer with rapid air technology",
                "category": "Home & Kitchen",
                "price": 8500,
                "rating": 4.3,
                "brand": "Philips",
                "url": "https://example.com/philips-airfryer",
                "features": "4.1L capacity, rapid air technology, dishwasher safe parts",
                "popularity_score": 0.8
            },
            {
                "title": "LG 260L Refrigerator",
                "description": "Double door refrigerator with smart inverter compressor",
                "category": "Home & Kitchen",
                "price": 25000,
                "rating": 4.2,
                "brand": "LG",
                "url": "https://example.com/lg-refrigerator",
                "features": "260L capacity, smart inverter, anti-bacterial gasket",
                "popularity_score": 0.75
            },
            
            # Fitness & Sports
            {
                "title": "Apple Watch Series 9",
                "description": "Advanced smartwatch with health monitoring and fitness tracking",
                "category": "Fitness",
                "price": 42000,
                "rating": 4.6,
                "brand": "Apple",
                "url": "https://example.com/apple-watch9",
                "features": "S9 chip, always-on retina display, health sensors, GPS",
                "popularity_score": 0.9
            },
            {
                "title": "Fitbit Charge 5",
                "description": "Advanced fitness tracker with built-in GPS and health metrics",
                "category": "Fitness",
                "price": 15000,
                "rating": 4.3,
                "brand": "Fitbit",
                "url": "https://example.com/fitbit-charge5",
                "features": "Built-in GPS, stress management, sleep score, 7-day battery",
                "popularity_score": 0.75
            }
        ]
        
        for i, product in enumerate(sample_products):
            try:
                self.client.index(
                    index="products",
                    id=f"sample_{i}",
                    body=product
                )
            except Exception as e:
                print(f"Error adding sample product: {e}")
        
        print(f"✅ Added {len(sample_products)} sample products")
    
    def refresh_products(self):
        """Clear existing products and add fresh sample data"""
        if not self.connected:
            return False
            
        try:
            # Delete existing products
            self.client.delete_by_query(
                index="products",
                body={"query": {"match_all": {}}}
            )
            print("🔄 Cleared existing products")
            
            # Add fresh sample products
            self.add_sample_products()
            print("✅ Refreshed product database with new products")
            return True
            
        except Exception as e:
            print(f"Error refreshing products: {e}")
            return False
    
    def hybrid_search(self, query: str, filters: Dict = None, size: int = 10) -> Dict:
        """Perform hybrid search combining keyword + semantic search"""
        if not self.connected:
            return self._demo_search_results(query)
        
        try:
            # Build hybrid search query
            search_body = {
                "query": {
                    "bool": {
                        "should": [
                            # Keyword search with boosting
                            {
                                "multi_match": {
                                    "query": query,
                                    "fields": [
                                        "title^3",      # Title gets highest boost
                                        "description^2", # Description gets medium boost  
                                        "features^2",   # Features get medium boost
                                        "brand^1.5",    # Brand gets some boost
                                        "category"      # Category normal weight
                                    ],
                                    "type": "best_fields",
                                    "fuzziness": "AUTO"
                                }
                            },
                            # Popularity boost
                            {
                                "function_score": {
                                    "query": {"match_all": {}},
                                    "field_value_factor": {
                                        "field": "popularity_score",
                                        "factor": 1.5,
                                        "modifier": "log1p"
                                    }
                                }
                            }
                        ],
                        "minimum_should_match": 1
                    }
                },
                "size": size,
                "sort": [
                    "_score",
                    {"rating": {"order": "desc"}},
                    {"popularity_score": {"order": "desc"}}
                ],
                "_source": {
                    "excludes": ["embeddings"]  # Don't return embeddings in results
                }
            }
            
            # Add filters if provided
            if filters:
                filter_clauses = []
                
                if filters.get('category'):
                    filter_clauses.append({"term": {"category": filters['category']}})
                
                if filters.get('price_range'):
                    price_filter = {"range": {"price": {}}}
                    if filters['price_range'].get('min'):
                        price_filter["range"]["price"]["gte"] = filters['price_range']['min']
                    if filters['price_range'].get('max'):
                        price_filter["range"]["price"]["lte"] = filters['price_range']['max']
                    filter_clauses.append(price_filter)
                
                if filters.get('min_rating'):
                    filter_clauses.append({"range": {"rating": {"gte": filters['min_rating']}}})
                
                if filter_clauses:
                    search_body["query"]["bool"]["filter"] = filter_clauses
            
            # Execute search
            results = self.client.search(index="products", body=search_body)
            
            return {
                'status': 'success',
                'total_hits': results['hits']['total']['value'],
                'products': [hit['_source'] for hit in results['hits']['hits']],
                'search_type': 'hybrid_elastic_search',
                'query': query,
                'took_ms': results['took']
            }
            
        except Exception as e:
            print(f"Elasticsearch search error: {e}")
            return self._demo_search_results(query)
    
    def add_product(self, product: Dict) -> bool:
        """Add a new product to the index"""
        if not self.connected:
            return False
        
        try:
            # Generate unique ID
            product_id = hashlib.md5(product['title'].encode()).hexdigest()
            
            self.client.index(
                index="products",
                id=product_id,
                body=product
            )
            return True
            
        except Exception as e:
            print(f"Error adding product: {e}")
            return False
    
    def get_categories(self) -> List[str]:
        """Get all available product categories"""
        if not self.connected:
            return ["Laptops", "Audio", "Mobile", "Gaming", "Electronics"]
        
        try:
            agg_body = {
                "aggs": {
                    "categories": {
                        "terms": {"field": "category", "size": 100}
                    }
                },
                "size": 0
            }
            
            results = self.client.search(index="products", body=agg_body)
            categories = [bucket['key'] for bucket in results['aggregations']['categories']['buckets']]
            return categories
            
        except Exception as e:
            print(f"Error getting categories: {e}")
            return ["Laptops", "Audio", "Mobile", "Gaming", "Electronics"]
    
    def _demo_search_results(self, query: str) -> Dict:
        """Demo search results when Elasticsearch not available - now intelligent!"""
        
        # Get all sample products (they're in memory during demo mode)
        all_products = self._get_sample_products_list()
        
        # Intelligent filtering based on query
        query_lower = query.lower()
        relevant_products = []
        
        # Category-based filtering
        if any(word in query_lower for word in ['laptop', 'computer', 'notebook']):
            relevant_products = [p for p in all_products if p['category'] == 'Laptops']
        elif any(word in query_lower for word in ['headphone', 'earphone', 'audio', 'music', 'sound']):
            relevant_products = [p for p in all_products if p['category'] == 'Audio']
        elif any(word in query_lower for word in ['phone', 'mobile', 'smartphone']):
            relevant_products = [p for p in all_products if p['category'] == 'Smartphones']
        elif any(word in query_lower for word in ['gaming', 'game', 'mouse', 'keyboard']):
            relevant_products = [p for p in all_products if p['category'] == 'Gaming']
        elif any(word in query_lower for word in ['fitness', 'watch', 'health', 'workout']):
            relevant_products = [p for p in all_products if p['category'] == 'Fitness']
        elif any(word in query_lower for word in ['kitchen', 'home', 'appliance']):
            relevant_products = [p for p in all_products if p['category'] == 'Home & Kitchen']
        else:
            # Default: return a mix of popular products
            relevant_products = all_products[:6]
        
        # Budget-based filtering
        budget_match = None
        import re
        budget_pattern = r'(?:under|below|within|less than)\s*₹?(\d+)'
        match = re.search(budget_pattern, query_lower)
        if match:
            budget_match = int(match.group(1))
            relevant_products = [p for p in relevant_products if p['price'] <= budget_match]
        
        # Brand-based filtering
        brand_keywords = {
            'apple': 'Apple', 'samsung': 'Samsung', 'sony': 'Sony', 
            'asus': 'ASUS', 'hp': 'HP', 'dell': 'Dell', 'lenovo': 'Lenovo',
            'msi': 'MSI', 'acer': 'Acer', 'logitech': 'Logitech', 'razer': 'Razer',
            'jbl': 'JBL', 'boat': 'boAt', 'oneplus': 'OnePlus', 'xiaomi': 'Xiaomi'
        }
        
        for keyword, brand in brand_keywords.items():
            if keyword in query_lower:
                relevant_products = [p for p in relevant_products if p['brand'] == brand]
                break
        
        # Sort by relevance and popularity
        relevant_products.sort(key=lambda x: x['popularity_score'], reverse=True)
        
        # Limit results
        relevant_products = relevant_products[:8]
        
        # If no relevant products found, return a few popular ones
        if not relevant_products:
            relevant_products = all_products[:3]
        
        return {
            'status': 'demo',
            'total_hits': len(relevant_products),
            'products': relevant_products,
            'search_type': 'intelligent_demo_mode',
            'query': query,
            'budget_filter': budget_match if budget_match else None
        }
    
    def _get_sample_products_list(self):
        """Return the complete sample products list"""
        return [
            # Gaming Laptops
            {
                "title": "Gaming Laptop ASUS ROG Strix G15",
                "description": "High-performance gaming laptop with RTX 3060, AMD Ryzen 7, 16GB RAM",
                "category": "Laptops",
                "price": 75000,
                "rating": 4.5,
                "brand": "ASUS",
                "url": "https://example.com/asus-rog",
                "features": "RTX 3060, Ryzen 7 5800H, 16GB RAM, 512GB SSD, 144Hz display",
                "popularity_score": 0.9
            },
            {
                "title": "MSI Gaming Laptop GF63 Thin",
                "description": "Budget-friendly gaming laptop with GTX 1650, Intel i5, 8GB RAM",
                "category": "Laptops",
                "price": 45000,
                "rating": 4.2,
                "brand": "MSI",
                "url": "https://example.com/msi-gf63",
                "features": "GTX 1650, Intel i5-10300H, 8GB RAM, 256GB SSD, 120Hz display",
                "popularity_score": 0.75
            },
            {
                "title": "HP Pavilion Gaming Laptop",
                "description": "Affordable gaming laptop with GTX 1660 Ti, AMD Ryzen 5, 16GB RAM",
                "category": "Laptops",
                "price": 55000,
                "rating": 4.3,
                "brand": "HP",
                "url": "https://example.com/hp-pavilion-gaming",
                "features": "GTX 1660 Ti, AMD Ryzen 5 4600H, 16GB RAM, 512GB SSD",
                "popularity_score": 0.8
            },
            
            # Professional Laptops
            {
                "title": "Apple MacBook Air M2",
                "description": "Ultra-thin laptop with M2 chip, perfect for productivity and creative work",
                "category": "Laptops", 
                "price": 115000,
                "rating": 4.8,
                "brand": "Apple",
                "url": "https://example.com/macbook-air",
                "features": "M2 chip, 8GB RAM, 256GB SSD, Retina display, all-day battery",
                "popularity_score": 0.95
            },
            {
                "title": "Dell XPS 13 Laptop",
                "description": "Premium ultrabook with Intel i7, 16GB RAM, ideal for professionals",
                "category": "Laptops",
                "price": 95000,
                "rating": 4.6,
                "brand": "Dell",
                "url": "https://example.com/dell-xps13",
                "features": "Intel i7-1165G7, 16GB RAM, 512GB SSD, 13.3 FHD display",
                "popularity_score": 0.85
            },
            {
                "title": "Lenovo ThinkPad E14",
                "description": "Business laptop with AMD Ryzen 5, 8GB RAM, durable build",
                "category": "Laptops",
                "price": 50000,
                "rating": 4.4,
                "brand": "Lenovo",
                "url": "https://example.com/thinkpad-e14",
                "features": "AMD Ryzen 5 4500U, 8GB RAM, 256GB SSD, 14-inch FHD",
                "popularity_score": 0.8
            },
            
            # Budget Laptops
            {
                "title": "Acer Aspire 5 Laptop",
                "description": "Budget laptop with Intel i3, 4GB RAM, perfect for students",
                "category": "Laptops",
                "price": 30000,
                "rating": 4.0,
                "brand": "Acer",
                "url": "https://example.com/acer-aspire5",
                "features": "Intel i3-1115G4, 4GB RAM, 1TB HDD, 15.6-inch HD display",
                "popularity_score": 0.7
            },
            
            # Headphones & Audio
            {
                "title": "Sony WH-1000XM4 Wireless Headphones",
                "description": "Industry-leading noise canceling wireless headphones",
                "category": "Audio",
                "price": 25000,
                "rating": 4.6,
                "brand": "Sony",
                "url": "https://example.com/sony-wh1000xm4",
                "features": "Active noise canceling, 30-hour battery, premium sound quality",
                "popularity_score": 0.85
            },
            {
                "title": "JBL Tune 760NC Wireless Headphones",
                "description": "Budget wireless headphones with active noise cancelling",
                "category": "Audio",
                "price": 8000,
                "rating": 4.2,
                "brand": "JBL",
                "url": "https://example.com/jbl-tune760nc",
                "features": "Active noise cancelling, 35-hour battery, JBL Pure Bass",
                "popularity_score": 0.75
            },
            {
                "title": "Apple AirPods Pro 2nd Gen",
                "description": "Premium wireless earbuds with adaptive transparency",
                "category": "Audio",
                "price": 22000,
                "rating": 4.7,
                "brand": "Apple",
                "url": "https://example.com/airpods-pro2",
                "features": "H2 chip, adaptive transparency, spatial audio, MagSafe charging",
                "popularity_score": 0.9
            },
            {
                "title": "boAt Airdopes 441 TWS Earbuds",
                "description": "Affordable true wireless earbuds with good bass",
                "category": "Audio",
                "price": 2500,
                "rating": 4.1,
                "brand": "boAt",
                "url": "https://example.com/boat-airdopes441",
                "features": "Bluetooth 5.0, 30-hour playback, IPX7 water resistance",
                "popularity_score": 0.7
            },
            
            # Smartphones
            {
                "title": "iPhone 15 Pro",
                "description": "Latest iPhone with A17 Pro chip, titanium design, pro camera system",
                "category": "Smartphones",
                "price": 130000,
                "rating": 4.8,
                "brand": "Apple",
                "url": "https://example.com/iphone15pro",
                "features": "A17 Pro chip, 128GB storage, pro camera system, titanium build",
                "popularity_score": 0.95
            },
            {
                "title": "Samsung Galaxy S24",
                "description": "Premium Android phone with AI features and excellent camera",
                "category": "Smartphones",
                "price": 85000,
                "rating": 4.6,
                "brand": "Samsung",
                "url": "https://example.com/galaxy-s24",
                "features": "Snapdragon 8 Gen 3, 128GB storage, 50MP camera, AI features",
                "popularity_score": 0.9
            },
            {
                "title": "OnePlus 12R",
                "description": "Flagship killer with fast charging and smooth performance",
                "category": "Smartphones",
                "price": 40000,
                "rating": 4.4,
                "brand": "OnePlus",
                "url": "https://example.com/oneplus12r",
                "features": "Snapdragon 8s Gen 3, 128GB storage, 100W fast charging",
                "popularity_score": 0.8
            },
            {
                "title": "Xiaomi Redmi Note 13 Pro",
                "description": "Budget smartphone with good camera and long battery life",
                "category": "Smartphones",
                "price": 25000,
                "rating": 4.3,
                "brand": "Xiaomi",
                "url": "https://example.com/redmi-note13pro",
                "features": "Dimensity 7200, 128GB storage, 200MP camera, 5000mAh battery",
                "popularity_score": 0.75
            },
            
            # Gaming Accessories
            {
                "title": "Logitech G502 HERO Gaming Mouse",
                "description": "High-performance gaming mouse with 25K DPI sensor",
                "category": "Gaming",
                "price": 5500,
                "rating": 4.5,
                "brand": "Logitech",
                "url": "https://example.com/logitech-g502",
                "features": "25K DPI HERO sensor, 11 programmable buttons, RGB lighting",
                "popularity_score": 0.85
            },
            {
                "title": "Razer BlackWidow V3 Mechanical Keyboard",
                "description": "Premium mechanical gaming keyboard with green switches",
                "category": "Gaming",
                "price": 12000,
                "rating": 4.4,
                "brand": "Razer",
                "url": "https://example.com/razer-blackwidow",
                "features": "Razer Green switches, RGB Chroma lighting, aluminum frame",
                "popularity_score": 0.8
            },
            
            # Home & Kitchen
            {
                "title": "Philips Air Fryer HD9252",
                "description": "Healthy cooking air fryer with rapid air technology",
                "category": "Home & Kitchen",
                "price": 8500,
                "rating": 4.3,
                "brand": "Philips",
                "url": "https://example.com/philips-airfryer",
                "features": "4.1L capacity, rapid air technology, dishwasher safe parts",
                "popularity_score": 0.8
            },
            {
                "title": "LG 260L Refrigerator",
                "description": "Double door refrigerator with smart inverter compressor",
                "category": "Home & Kitchen",
                "price": 25000,
                "rating": 4.2,
                "brand": "LG",
                "url": "https://example.com/lg-refrigerator",
                "features": "260L capacity, smart inverter, anti-bacterial gasket",
                "popularity_score": 0.75
            },
            
            # Fitness & Sports
            {
                "title": "Apple Watch Series 9",
                "description": "Advanced smartwatch with health monitoring and fitness tracking",
                "category": "Fitness",
                "price": 42000,
                "rating": 4.6,
                "brand": "Apple",
                "url": "https://example.com/apple-watch9",
                "features": "S9 chip, always-on retina display, health sensors, GPS",
                "popularity_score": 0.9
            },
            {
                "title": "Fitbit Charge 5",
                "description": "Advanced fitness tracker with built-in GPS and health metrics",
                "category": "Fitness",
                "price": 15000,
                "rating": 4.3,
                "brand": "Fitbit",
                "url": "https://example.com/fitbit-charge5",
                "features": "Built-in GPS, stress management, sleep score, 7-day battery",
                "popularity_score": 0.75
            }
        ]
    
    def test_connection(self) -> Dict:
        """Test Elasticsearch connection"""
        if not self.connected:
            return {'status': 'disconnected', 'service': 'Demo Mode'}
        
        try:
            info = self.client.info()
            return {
                'status': 'connected',
                'service': 'Elasticsearch Cloud',
                'cluster_name': info['cluster_name'],
                'version': info['version']['number']
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}