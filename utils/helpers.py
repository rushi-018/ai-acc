"""
Utility Functions for AI-Accelerate
"""
import re
import json
from datetime import datetime
from typing import Dict, List, Any

def clean_text(text: str) -> str:
    """Clean and normalize text input"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove special characters but keep essential punctuation
    text = re.sub(r'[^\w\s\-\.\,\!\?]', '', text)
    
    return text

def extract_price_from_text(text: str) -> float:
    """Extract price values from text"""
    # Look for price patterns like ₹1,234 or $123.45
    price_patterns = [
        r'₹[\d,]+(?:\.\d{2})?',
        r'\$[\d,]+(?:\.\d{2})?',
        r'[\d,]+(?:\.\d{2})?\s*(?:rupees?|rs\.?|inr)',
        r'[\d,]+(?:\.\d{2})?\s*(?:dollars?|\$|usd)'
    ]
    
    for pattern in price_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Extract numeric value
            price_str = re.sub(r'[^\d\.]', '', matches[0])
            try:
                return float(price_str)
            except ValueError:
                continue
    
    return 0.0

def format_currency(amount: float, currency: str = "INR") -> str:
    """Format currency values"""
    if currency.upper() == "INR":
        return f"₹{amount:,.0f}"
    elif currency.upper() == "USD":
        return f"${amount:,.2f}"
    else:
        return f"{amount:,.2f} {currency}"

def calculate_similarity_score(text1: str, text2: str) -> float:
    """Calculate simple text similarity score"""
    words1 = set(clean_text(text1.lower()).split())
    words2 = set(clean_text(text2.lower()).split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0

def validate_product_data(product: Dict) -> bool:
    """Validate product data structure"""
    required_fields = ['name', 'price', 'platform']
    
    for field in required_fields:
        if field not in product or not product[field]:
            return False
    
    # Validate price is numeric
    try:
        float(product['price'])
    except (ValueError, TypeError):
        return False
    
    return True

def log_user_interaction(interaction_type: str, data: Dict) -> None:
    """Log user interactions for analytics"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'type': interaction_type,
        'data': data
    }
    
    # In production, this would send to analytics service
    print(f"[ANALYTICS] {json.dumps(log_entry)}")

def get_trending_keywords() -> List[str]:
    """Get trending search keywords"""
    # Mock trending keywords - in production, would come from analytics
    return [
        'iphone 15',
        'macbook air',
        'samsung galaxy s24',
        'nike shoes',
        'wireless headphones',
        'gaming laptop',
        'smartwatch',
        'bluetooth speaker'
    ]

def categorize_query(query: str) -> str:
    """Categorize user query into product categories"""
    query_lower = query.lower()
    
    categories = {
        'electronics': ['phone', 'laptop', 'computer', 'tablet', 'headphones', 'camera', 'tv', 'speaker'],
        'fashion': ['shirt', 'dress', 'shoes', 'bag', 'watch', 'jewelry', 'clothes', 'fashion'],
        'home': ['furniture', 'kitchen', 'appliance', 'decor', 'bedding', 'home'],
        'books': ['book', 'novel', 'textbook', 'magazine', 'ebook', 'reading'],
        'sports': ['fitness', 'gym', 'sports', 'exercise', 'outdoor', 'athletic']
    }
    
    for category, keywords in categories.items():
        if any(keyword in query_lower for keyword in keywords):
            return category
    
    return 'general'

def generate_search_suggestions(query: str) -> List[str]:
    """Generate search suggestions based on query"""
    suggestions = []
    
    # Add trending variations
    base_terms = query.lower().split()
    
    if 'phone' in base_terms or 'mobile' in base_terms:
        suggestions.extend([
            'latest smartphones 2024',
            'best camera phones',
            'budget smartphones under 20000',
            'flagship phones comparison'
        ])
    
    elif 'laptop' in base_terms:
        suggestions.extend([
            'gaming laptops',
            'business laptops',
            'ultrabook laptops',
            'budget laptops under 50000'
        ])
    
    elif 'headphones' in base_terms:
        suggestions.extend([
            'wireless headphones',
            'noise cancelling headphones',
            'gaming headsets',
            'bluetooth earphones'
        ])
    
    else:
        suggestions.extend([
            f'{query} reviews',
            f'{query} price comparison',
            f'best {query} 2024',
            f'{query} offers'
        ])
    
    return suggestions[:4]