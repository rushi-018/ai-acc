"""
REAL-TIME WEB SCRAPING for Live Product Data
Scrapes actual e-commerce sites for real products and prices
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
from typing import Dict, List
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from datetime import datetime

class RealDataScraper:
    def __init__(self):
        """Initialize real data scraper with multiple sources"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.sources = {
            'amazon': 'https://www.amazon.in',
            'flipkart': 'https://www.flipkart.com',
            'croma': 'https://www.croma.com',
            'reliance': 'https://www.reliancedigital.in'
        }
        
    def setup_driver(self):
        """Setup undetected Chrome driver for real scraping"""
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            driver = uc.Chrome(options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            return driver
        except Exception as e:
            print(f"Driver setup failed: {e}")
            return None
    
    def scrape_amazon_products(self, query: str, max_results: int = 10) -> List[Dict]:
        """Scrape real Amazon products"""
        products = []
        
        try:
            # Amazon search URL
            search_url = f"https://www.amazon.in/s?k={query.replace(' ', '+')}"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            for container in product_containers[:max_results]:
                try:
                    # Extract product details
                    title_elem = container.find('h2', class_='a-size-mini')
                    if not title_elem:
                        continue
                        
                    title = title_elem.get_text().strip()
                    
                    # Price
                    price_elem = container.find('span', class_='a-price-whole')
                    price = 0
                    if price_elem:
                        price_text = price_elem.get_text().replace(',', '').replace('₹', '')
                        price = int(re.findall(r'\d+', price_text)[0]) if re.findall(r'\d+', price_text) else 0
                    
                    # Rating
                    rating_elem = container.find('span', class_='a-icon-alt')
                    rating = 4.0
                    if rating_elem:
                        rating_text = rating_elem.get_text()
                        rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                        if rating_match:
                            rating = float(rating_match.group(1))
                    
                    # Product URL
                    link_elem = container.find('a', class_='a-link-normal')
                    product_url = f"https://www.amazon.in{link_elem.get('href')}" if link_elem else ""
                    
                    # Image
                    img_elem = container.find('img', class_='s-image')
                    image_url = img_elem.get('src') if img_elem else ""
                    
                    product = {
                        'title': title,
                        'price': price,
                        'rating': rating,
                        'url': product_url,
                        'image': image_url,
                        'source': 'Amazon',
                        'scraped_at': datetime.now().isoformat(),
                        'category': self.classify_product(title),
                        'brand': self.extract_brand(title),
                        'description': title,
                        'features': self.extract_features(title),
                        'popularity_score': rating / 5.0
                    }
                    
                    if product['price'] > 0:  # Only add products with valid prices
                        products.append(product)
                        
                except Exception as e:
                    print(f"Error parsing Amazon product: {e}")
                    continue
                    
        except Exception as e:
            print(f"Amazon scraping error: {e}")
            
        return products
    
    def scrape_flipkart_products(self, query: str, max_results: int = 10) -> List[Dict]:
        """Scrape real Flipkart products"""
        products = []
        
        try:
            search_url = f"https://www.flipkart.com/search?q={query.replace(' ', '%20')}"
            
            response = requests.get(search_url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Flipkart uses different selectors
            product_containers = soup.find_all('div', class_='_1AtVbE')
            
            for container in product_containers[:max_results]:
                try:
                    # Product title
                    title_elem = container.find('div', class_='_4rR01T')
                    if not title_elem:
                        continue
                    title = title_elem.get_text().strip()
                    
                    # Price
                    price_elem = container.find('div', class_='_30jeq3')
                    price = 0
                    if price_elem:
                        price_text = price_elem.get_text().replace(',', '').replace('₹', '')
                        price = int(re.findall(r'\d+', price_text)[0]) if re.findall(r'\d+', price_text) else 0
                    
                    # Rating
                    rating_elem = container.find('div', class_='_3LWZlK')
                    rating = 4.0
                    if rating_elem:
                        rating = float(rating_elem.get_text())
                    
                    product = {
                        'title': title,
                        'price': price,
                        'rating': rating,
                        'url': f"https://www.flipkart.com{container.find('a')['href']}" if container.find('a') else "",
                        'source': 'Flipkart',
                        'scraped_at': datetime.now().isoformat(),
                        'category': self.classify_product(title),
                        'brand': self.extract_brand(title),
                        'description': title,
                        'features': self.extract_features(title),
                        'popularity_score': rating / 5.0
                    }
                    
                    if product['price'] > 0:
                        products.append(product)
                        
                except Exception as e:
                    print(f"Error parsing Flipkart product: {e}")
                    continue
                    
        except Exception as e:
            print(f"Flipkart scraping error: {e}")
            
        return products
    
    def classify_product(self, title: str) -> str:
        """Classify product into category based on title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['laptop', 'notebook', 'macbook']):
            return 'Laptops'
        elif any(word in title_lower for word in ['headphone', 'earphone', 'earbud', 'airpods']):
            return 'Audio'
        elif any(word in title_lower for word in ['phone', 'mobile', 'smartphone', 'iphone']):
            return 'Smartphones'
        elif any(word in title_lower for word in ['mouse', 'keyboard', 'gaming']):
            return 'Gaming'
        elif any(word in title_lower for word in ['watch', 'fitness', 'tracker']):
            return 'Fitness'
        elif any(word in title_lower for word in ['tv', 'television', 'monitor']):
            return 'Electronics'
        else:
            return 'Electronics'
    
    def extract_brand(self, title: str) -> str:
        """Extract brand from product title"""
        brands = [
            'Apple', 'Samsung', 'Sony', 'LG', 'HP', 'Dell', 'Lenovo', 'ASUS', 'Acer', 'MSI',
            'OnePlus', 'Xiaomi', 'Realme', 'Oppo', 'Vivo', 'Google', 'Microsoft', 'Intel',
            'AMD', 'Nvidia', 'Logitech', 'Razer', 'Corsair', 'JBL', 'Bose', 'Sennheiser',
            'Boat', 'Noise', 'Amazfit', 'Fitbit', 'Garmin', 'Canon', 'Nikon'
        ]
        
        title_upper = title.upper()
        for brand in brands:
            if brand.upper() in title_upper:
                return brand
        
        # Try to extract first word as brand
        first_word = title.split()[0] if title.split() else 'Unknown'
        return first_word
    
    def extract_features(self, title: str) -> str:
        """Extract key features from product title"""
        # Extract RAM, storage, processor info
        features = []
        title_lower = title.lower()
        
        # RAM
        ram_match = re.search(r'(\d+)\s*gb\s*(ram|memory)', title_lower)
        if ram_match:
            features.append(f"{ram_match.group(1)}GB RAM")
        
        # Storage
        storage_match = re.search(r'(\d+)\s*(gb|tb)\s*(ssd|storage)', title_lower)
        if storage_match:
            features.append(f"{storage_match.group(1)}{storage_match.group(2).upper()} {storage_match.group(3).upper()}")
        
        # Screen size
        screen_match = re.search(r'(\d+\.?\d*)\s*inch', title_lower)
        if screen_match:
            features.append(f"{screen_match.group(1)}-inch display")
        
        return ', '.join(features) if features else title[:50]
    
    def get_real_products(self, query: str, max_per_source: int = 5) -> List[Dict]:
        """Get real products from multiple sources"""
        all_products = []
        
        print(f"🔍 Scraping real products for: {query}")
        
        # Scrape Amazon
        try:
            amazon_products = self.scrape_amazon_products(query, max_per_source)
            all_products.extend(amazon_products)
            print(f"📦 Amazon: Found {len(amazon_products)} products")
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"Amazon scraping failed: {e}")
        
        # Scrape Flipkart
        try:
            flipkart_products = self.scrape_flipkart_products(query, max_per_source)
            all_products.extend(flipkart_products)
            print(f"🛒 Flipkart: Found {len(flipkart_products)} products")
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"Flipkart scraping failed: {e}")
        
        # Remove duplicates and sort by relevance
        unique_products = self.remove_duplicates(all_products)
        
        print(f"✅ Total unique products: {len(unique_products)}")
        return unique_products[:20]  # Return top 20 results
    
    def remove_duplicates(self, products: List[Dict]) -> List[Dict]:
        """Remove duplicate products based on title similarity"""
        unique_products = []
        seen_titles = set()
        
        for product in products:
            # Create a normalized title for comparison
            normalized_title = re.sub(r'[^\w\s]', '', product['title'].lower())
            title_hash = hashlib.md5(normalized_title.encode()).hexdigest()
            
            if title_hash not in seen_titles:
                seen_titles.add(title_hash)
                unique_products.append(product)
        
        return unique_products
    
    def get_live_deals(self, categories: List[str] = None) -> List[Dict]:
        """Get live deals and discounts"""
        deals = []
        
        deal_queries = [
            'laptop deals today',
            'mobile phone offers',
            'headphones discount',
            'gaming accessories sale'
        ]
        
        for query in deal_queries:
            try:
                products = self.get_real_products(query, 3)
                for product in products:
                    if product['price'] > 0:
                        # Calculate deal quality
                        product['deal_quality'] = self.calculate_deal_quality(product)
                        deals.append(product)
            except Exception as e:
                print(f"Deal scraping error for {query}: {e}")
        
        # Sort by deal quality
        deals.sort(key=lambda x: x.get('deal_quality', 0), reverse=True)
        return deals[:10]
    
    def calculate_deal_quality(self, product: Dict) -> float:
        """Calculate deal quality score"""
        score = 0.0
        
        # Rating contribution (40%)
        score += (product.get('rating', 0) / 5.0) * 0.4
        
        # Price range contribution (30%)
        price = product.get('price', 0)
        if 10000 <= price <= 50000:  # Sweet spot
            score += 0.3
        elif 5000 <= price <= 10000:
            score += 0.25
        elif price < 5000:
            score += 0.2
        
        # Brand reputation (20%)
        brand = product.get('brand', '').lower()
        premium_brands = ['apple', 'samsung', 'sony', 'hp', 'dell', 'asus']
        if brand in premium_brands:
            score += 0.2
        else:
            score += 0.1
        
        # Freshness (10%)
        score += 0.1  # All scraped data is fresh
        
        return min(score, 1.0)