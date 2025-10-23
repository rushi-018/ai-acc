"""
Product Search Engine
Elastic Search + Hybrid Search Integration
"""
import os
import json
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
import random
from datetime import datetime

# Mock Elasticsearch for development
try:
    from elasticsearch import Elasticsearch
    ELASTICSEARCH_AVAILABLE = True
except ImportError:
    ELASTICSEARCH_AVAILABLE = False
    print("Elasticsearch not available. Using mock data.")

@dataclass
class Product:
    """Product data structure"""
    id: str
    name: str
    price: float
    rating: float
    reviews: int
    platform: str
    url: str
    category: str
    availability: str = "In Stock"
    description: str = ""
    image_url: str = ""

class ProductSearchEngine:
    """
    Hybrid product search engine using Elastic Search
    Combines traditional keyword search with semantic search
    """
    
    def __init__(self):
        self.elasticsearch_url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
        self.index_name = "products"
        
        # Mock product database for development
        self.mock_products = self._load_mock_products()
        
        # Initialize Elasticsearch client (if available)
        if ELASTICSEARCH_AVAILABLE:
            self._initialize_elasticsearch()
    
    def _initialize_elasticsearch(self):
        """Initialize Elasticsearch client"""
        try:
            self.es_client = Elasticsearch([self.elasticsearch_url])
            
            # Test connection
            if self.es_client.ping():
                print("Connected to Elasticsearch")
                self._ensure_index_exists()
            else:
                print("Failed to connect to Elasticsearch. Using mock data.")
                self.es_client = None
                
        except Exception as e:
            print(f"Elasticsearch initialization error: {e}")
            self.es_client = None
    
    def _ensure_index_exists(self):
        """Create index if it doesn't exist"""
        if not self.es_client.indices.exists(index=self.index_name):
            
            # Define index mapping for hybrid search
            mapping = {
                "mappings": {
                    "properties": {
                        "name": {
                            "type": "text",
                            "analyzer": "standard",
                            "fields": {
                                "keyword": {"type": "keyword"}
                            }
                        },
                        "description": {
                            "type": "text",
                            "analyzer": "standard"
                        },
                        "category": {"type": "keyword"},
                        "platform": {"type": "keyword"},
                        "price": {"type": "float"},
                        "rating": {"type": "float"},
                        "reviews": {"type": "integer"},
                        "embedding": {
                            "type": "dense_vector",
                            "dims": 384  # For sentence transformers
                        },
                        "created_at": {"type": "date"}
                    }
                }
            }
            
            self.es_client.indices.create(index=self.index_name, body=mapping)
            print(f"Created Elasticsearch index: {self.index_name}")
    
    def search(self, query: str, mode: str = "Hybrid", limit: int = 10) -> List[Dict]:
        """
        Search for products using different modes
        
        Args:
            query: Search query
            mode: Search mode - "Hybrid", "Semantic", "Traditional"
            limit: Maximum number of results
        """
        
        if ELASTICSEARCH_AVAILABLE and hasattr(self, 'es_client') and self.es_client:
            return self._elasticsearch_search(query, mode, limit)
        else:
            return self._mock_search(query, limit)
    
    def _elasticsearch_search(self, query: str, mode: str, limit: int) -> List[Dict]:
        """Search using Elasticsearch"""
        
        try:
            if mode == "Traditional":
                # Traditional keyword search
                search_body = {
                    "query": {
                        "multi_match": {
                            "query": query,
                            "fields": ["name^2", "description", "category"],
                            "type": "best_fields",
                            "fuzziness": "AUTO"
                        }
                    },
                    "sort": [
                        {"rating": {"order": "desc"}},
                        {"reviews": {"order": "desc"}},
                        "_score"
                    ],
                    "size": limit
                }
            
            elif mode == "Semantic":
                # Semantic search using embeddings (requires vector generation)
                query_embedding = self._generate_query_embedding(query)
                
                search_body = {
                    "query": {
                        "script_score": {
                            "query": {"match_all": {}},
                            "script": {
                                "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                                "params": {"query_vector": query_embedding}
                            }
                        }
                    },
                    "size": limit
                }
            
            else:  # Hybrid mode
                # Combine keyword and semantic search
                query_embedding = self._generate_query_embedding(query)
                
                search_body = {
                    "query": {
                        "bool": {
                            "should": [
                                {
                                    "multi_match": {
                                        "query": query,
                                        "fields": ["name^2", "description", "category"],
                                        "type": "best_fields",
                                        "fuzziness": "AUTO",
                                        "boost": 1.0
                                    }
                                },
                                {
                                    "script_score": {
                                        "query": {"match_all": {}},
                                        "script": {
                                            "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                                            "params": {"query_vector": query_embedding}
                                        },
                                        "boost": 0.5
                                    }
                                }
                            ],
                            "minimum_should_match": 1
                        }
                    },
                    "sort": [
                        "_score",
                        {"rating": {"order": "desc"}},
                        {"reviews": {"order": "desc"}}
                    ],
                    "size": limit
                }
            
            # Execute search
            response = self.es_client.search(index=self.index_name, body=search_body)
            
            # Convert to product format
            products = []
            for hit in response['hits']['hits']:
                source = hit['_source']
                products.append({
                    'id': hit['_id'],
                    'name': source.get('name', 'Unknown Product'),
                    'price': source.get('price', 0),
                    'rating': source.get('rating', 0),
                    'reviews': source.get('reviews', 0),
                    'platform': source.get('platform', 'Unknown'),
                    'url': source.get('url', '#'),
                    'category': source.get('category', 'General'),
                    'availability': source.get('availability', 'Check website'),
                    'score': hit['_score']
                })
            
            return products
            
        except Exception as e:
            print(f"Elasticsearch search error: {e}")
            return self._mock_search(query, limit)
    
    def _generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for semantic search (mock implementation)"""
        # In real implementation, use sentence transformers or OpenAI embeddings
        # For now, return random embedding for testing
        return [random.random() for _ in range(384)]
    
    def _mock_search(self, query: str, limit: int) -> List[Dict]:
        """Mock search for development"""
        
        # Simple keyword matching on mock data
        query_lower = query.lower()
        matching_products = []
        
        for product in self.mock_products:
            score = 0
            
            # Name matching (highest weight)
            if query_lower in product['name'].lower():
                score += 3
            
            # Category matching
            if query_lower in product['category'].lower():
                score += 2
            
            # Description matching  
            if query_lower in product.get('description', '').lower():
                score += 1
            
            # Add some fuzzy matching for common variations
            query_words = query_lower.split()
            for word in query_words:
                if word in product['name'].lower():
                    score += 0.5
            
            if score > 0:
                product_copy = product.copy()
                product_copy['score'] = score
                matching_products.append(product_copy)
        
        # Sort by score (desc), then rating (desc), then reviews (desc)
        matching_products.sort(key=lambda x: (x['score'], x['rating'], x['reviews']), reverse=True)
        
        return matching_products[:limit]
    
    def _load_mock_products(self) -> List[Dict]:
        """Load mock product data for development"""
        
        mock_data = [
            {
                'id': '1',
                'name': 'iPhone 15 Pro Max',
                'price': 159900,
                'rating': 4.5,
                'reviews': 1250,
                'platform': 'Amazon',
                'url': 'https://amazon.in/iphone-15-pro-max',
                'category': 'electronics',
                'availability': 'In Stock',
                'description': 'Latest iPhone with A17 Pro chip and titanium design'
            },
            {
                'id': '2', 
                'name': 'Samsung Galaxy S24 Ultra',
                'price': 134999,
                'rating': 4.4,
                'reviews': 890,
                'platform': 'Flipkart',
                'url': 'https://flipkart.com/galaxy-s24-ultra',
                'category': 'electronics',
                'availability': 'In Stock',
                'description': 'Premium Android phone with S Pen and amazing cameras'
            },
            {
                'id': '3',
                'name': 'MacBook Air M3',
                'price': 114900,
                'rating': 4.6,
                'reviews': 567,
                'platform': 'Apple Store',
                'url': 'https://apple.com/macbook-air-m3',
                'category': 'electronics',
                'availability': 'In Stock',
                'description': 'Ultra-thin laptop with M3 chip for incredible performance'
            },
            {
                'id': '4',
                'name': 'Nike Air Force 1',
                'price': 7495,
                'rating': 4.3,
                'reviews': 2340,
                'platform': 'Nike',
                'url': 'https://nike.com/air-force-1',
                'category': 'fashion',
                'availability': 'In Stock', 
                'description': 'Classic white sneakers for everyday style'
            },
            {
                'id': '5',
                'name': 'Sony WH-1000XM5 Headphones',
                'price': 29990,
                'rating': 4.7,
                'reviews': 834,
                'platform': 'Amazon',
                'url': 'https://amazon.in/sony-wh1000xm5',
                'category': 'electronics',
                'availability': 'In Stock',
                'description': 'Premium noise-canceling wireless headphones'
            },
            {
                'id': '6',
                'name': 'Levi\'s 501 Original Jeans',
                'price': 3999,
                'rating': 4.2,
                'reviews': 1567,
                'platform': 'Flipkart',
                'url': 'https://flipkart.com/levis-501-jeans',
                'category': 'fashion',
                'availability': 'In Stock',
                'description': 'Classic straight-fit jeans in authentic blue denim'
            },
            {
                'id': '7',
                'name': 'Dell XPS 13 Laptop',
                'price': 89990,
                'rating': 4.4,
                'reviews': 445,
                'platform': 'Dell',
                'url': 'https://dell.com/xps-13',
                'category': 'electronics',
                'availability': 'In Stock',
                'description': 'Premium ultrabook with InfinityEdge display'
            },
            {
                'id': '8',
                'name': 'Adidas Ultraboost 22',
                'price': 16999,
                'rating': 4.5,
                'reviews': 678,
                'platform': 'Adidas',
                'url': 'https://adidas.com/ultraboost-22',
                'category': 'fashion',
                'availability': 'Limited Stock',
                'description': 'High-performance running shoes with Boost technology'
            }
        ]
        
        return mock_data
    
    def add_product(self, product: Dict) -> bool:
        """Add a product to the search index"""
        
        if ELASTICSEARCH_AVAILABLE and hasattr(self, 'es_client') and self.es_client:
            try:
                # Generate embedding for the product
                text_for_embedding = f"{product.get('name', '')} {product.get('description', '')} {product.get('category', '')}"
                embedding = self._generate_query_embedding(text_for_embedding)
                
                # Add embedding to product
                product_with_embedding = product.copy()
                product_with_embedding['embedding'] = embedding
                product_with_embedding['created_at'] = datetime.now().isoformat()
                
                # Index the product
                response = self.es_client.index(
                    index=self.index_name,
                    id=product.get('id'),
                    body=product_with_embedding
                )
                
                return response['result'] in ['created', 'updated']
                
            except Exception as e:
                print(f"Error adding product to Elasticsearch: {e}")
                return False
        else:
            # Add to mock database
            self.mock_products.append(product)
            return True
    
    def get_trending_products(self, category: Optional[str] = None, limit: int = 5) -> List[Dict]:
        """Get trending/popular products"""
        
        products = self.mock_products.copy()
        
        if category:
            products = [p for p in products if p['category'].lower() == category.lower()]
        
        # Sort by rating and reviews
        products.sort(key=lambda x: (x['rating'] * x['reviews']), reverse=True)
        
        return products[:limit]
    
    def get_price_range_products(self, min_price: float, max_price: float, category: Optional[str] = None) -> List[Dict]:
        """Get products within price range"""
        
        products = self.mock_products.copy()
        
        # Filter by price range
        products = [p for p in products if min_price <= p['price'] <= max_price]
        
        if category:
            products = [p for p in products if p['category'].lower() == category.lower()]
        
        # Sort by rating
        products.sort(key=lambda x: x['rating'], reverse=True)
        
        return products