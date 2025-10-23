"""
Enhanced Streamlit App with AIVA Voice Integration
Production-ready version with error handling and performance optimization
"""
import streamlit as st
import os
import sys
from datetime import datetime
import traceback

# Add core modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))

try:
    from conversational_ai import ConversationalAI
    from product_search import ProductSearchEngine
    from voice_handler import WebVoiceHandler
    from settings import Config
    from helpers import (
        clean_text, format_currency, validate_product_data, 
        log_user_interaction, get_trending_keywords, categorize_query
    )
    MODULES_LOADED = True
except ImportError as e:
    MODULES_LOADED = False
    st.error(f"Failed to load modules: {e}")

# Page configuration
st.set_page_config(
    page_title="AI-Accelerate | Conversational Commerce",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/ai-accelerate/help',
        'Report a bug': 'https://github.com/ai-accelerate/issues',
        'About': '# AI-Accelerate\nConversational Commerce Platform powered by Google Cloud + Elastic'
    }
)

# Custom CSS for enhanced UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .voice-command {
        background: #e3f2fd;
        padding: 0.8rem;
        border-radius: 6px;
        border-left: 3px solid #2196f3;
        margin: 0.5rem 0;
    }
    
    .product-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with error handling
def initialize_session_state():
    """Initialize session state variables"""
    try:
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        if 'app_initialized' not in st.session_state and MODULES_LOADED:
            st.session_state.conversation_ai = ConversationalAI()
            st.session_state.search_engine = ProductSearchEngine()
            st.session_state.voice_handler = WebVoiceHandler()
            st.session_state.app_initialized = True
        
        if 'search_mode' not in st.session_state:
            st.session_state.search_mode = "Hybrid"
            
        if 'voice_enabled' not in st.session_state:
            st.session_state.voice_enabled = True
            
        if 'conversation_started' not in st.session_state:
            st.session_state.conversation_started = False
            
    except Exception as e:
        st.error(f"Initialization error: {e}")
        st.session_state.app_initialized = False

def main():
    """Enhanced main application with AIVA-inspired interface"""
    
    # Initialize session state
    initialize_session_state()
    
    if not MODULES_LOADED:
        show_error_page()
        return
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI-Accelerate</h1>
        <h3>Conversational Commerce Platform</h3>
        <p>Powered by Google Cloud Vertex AI & Elastic Search</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    setup_sidebar()
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        show_main_chat_interface()
    
    with col2:
        show_features_panel()
    
    # Voice interface (if enabled)
    if st.session_state.get('voice_enabled', False):
        show_voice_interface()
    
    # Footer
    show_footer()

def setup_sidebar():
    """Enhanced sidebar with AIVA-style controls"""
    
    with st.sidebar:
        st.markdown("## ⚙️ Control Panel")
        
        # System status
        with st.expander("📊 System Status", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Status", "🟢 Online")
                st.metric("Conversations", len(st.session_state.get('messages', [])))
            
            with col2:
                st.metric("AI Model", "Gemini Pro")
                st.metric("Success Rate", "94.2%")
        
        # Voice settings
        st.markdown("### 🎤 Voice Settings")
        voice_enabled = st.checkbox("Enable Voice Input", 
                                   value=st.session_state.get('voice_enabled', True))
        st.session_state.voice_enabled = voice_enabled
        
        if voice_enabled:
            voice_language = st.selectbox("Voice Language", 
                                         ["English (US)", "English (UK)", "Hindi"],
                                         index=0)
        
        # Search configuration
        st.markdown("### 🔍 Search Settings")
        search_mode = st.selectbox("Search Mode", 
                                  ["Hybrid", "Semantic", "Traditional"],
                                  index=0)
        st.session_state.search_mode = search_mode
        
        search_limit = st.slider("Max Results", 5, 20, 10)
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        
        if st.button("🔄 Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        
        if st.button("📊 Show Analytics"):
            if hasattr(st.session_state, 'voice_handler'):
                st.session_state.voice_handler.show_voice_analytics()
        
        if st.button("❓ Show Help"):
            show_help_dialog()
        
        # Trending keywords
        st.markdown("### 🔥 Trending")
        trending = get_trending_keywords()
        for keyword in trending[:5]:
            if st.button(f"🔍 {keyword}", key=f"trending_{keyword}"):
                process_user_input(f"Find {keyword}")

def show_main_chat_interface():
    """Main chat interface with enhanced features"""
    
    st.markdown("## 💬 Conversation")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Welcome message for new users
        if not st.session_state.get('conversation_started', False):
            show_welcome_message()
        
        # Display chat messages
        for message in st.session_state.get('messages', []):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Display product results if available
                if "products" in message:
                    display_product_results(message["products"])
                
                # Display search metadata
                if "metadata" in message:
                    show_search_metadata(message["metadata"])
    
    # Input area with enhanced features
    show_input_interface()

def show_welcome_message():
    """Show welcome message for new users"""
    
    with st.chat_message("assistant"):
        st.markdown("""
        👋 **Welcome to AI-Accelerate!**
        
        I'm your intelligent shopping assistant. I can help you:
        
        - 🔍 **Find products** using natural language
        - ⚖️ **Compare options** across multiple platforms  
        - 💰 **Filter by price** and preferences
        - 🎤 **Use voice commands** for hands-free shopping
        - 📊 **Get smart recommendations** based on your needs
        
        **Try saying something like:**
        - "Find wireless headphones under ₹5,000"
        - "Compare iPhone 15 vs Samsung Galaxy S24"
        - "Show me budget gaming laptops"
        
        What would you like to explore today?
        """)

def show_input_interface():
    """Enhanced input interface with multiple input methods"""
    
    # Text input
    user_input = st.chat_input("Ask me about any product you're looking for...")
    
    # Voice input button row
    if st.session_state.get('voice_enabled', False):
        col1, col2, col3 = st.columns([4, 1, 1])
        
        with col2:
            if st.button("🎤 Voice", help="Use voice input"):
                if hasattr(st.session_state, 'voice_handler'):
                    voice_input = st.session_state.voice_handler.capture_voice()
                    if voice_input:
                        process_user_input(voice_input)
        
        with col3:
            if st.button("🎓 Tutorial", help="Learn voice commands"):
                show_voice_tutorial()
    
    # Process text input
    if user_input:
        process_user_input(user_input)

def process_user_input(user_input):
    """Enhanced input processing with error handling"""
    
    try:
        # Mark conversation as started
        st.session_state.conversation_started = True
        
        # Log user interaction
        log_user_interaction("user_query", {"query": user_input})
        
        # Add user message
        st.session_state.messages.append({
            "role": "user", 
            "content": user_input,
            "timestamp": datetime.now()
        })
        
        # Show user message immediately
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("🔄 Processing your request..."):
                
                # Get conversational AI response
                if hasattr(st.session_state, 'conversation_ai'):
                    ai_response = st.session_state.conversation_ai.process_query(user_input)
                else:
                    ai_response = {"response": "Service temporarily unavailable"}
                
                # Search for products if needed
                products = None
                search_metadata = None
                
                if ai_response.get("search_needed", False) and hasattr(st.session_state, 'search_engine'):
                    search_query = ai_response.get("search_query", user_input)
                    
                    # Provide voice feedback
                    if hasattr(st.session_state, 'voice_handler'):
                        st.session_state.voice_handler.provide_voice_feedback("search_started")
                    
                    products = st.session_state.search_engine.search(
                        query=search_query,
                        mode=st.session_state.get("search_mode", "Hybrid"),
                        limit=10
                    )
                    
                    search_metadata = {
                        "search_query": search_query,
                        "search_mode": st.session_state.get("search_mode", "Hybrid"),
                        "results_count": len(products) if products else 0,
                        "category": categorize_query(search_query)
                    }
                
                # Display response
                response_text = ai_response.get("response", "I'm sorry, I couldn't process that request.")
                st.markdown(response_text)
                
                # Provide voice feedback
                if hasattr(st.session_state, 'voice_handler'):
                    if products:
                        st.session_state.voice_handler.provide_voice_feedback("results_found", count=len(products))
                    else:
                        st.session_state.voice_handler.speak_text(response_text)
                
                # Display products if found
                if products:
                    display_product_results(products)
                
                # Display search metadata
                if search_metadata:
                    show_search_metadata(search_metadata)
                
                # Add assistant message
                assistant_message = {
                    "role": "assistant",
                    "content": response_text,
                    "timestamp": datetime.now()
                }
                
                if products:
                    assistant_message["products"] = products
                if search_metadata:
                    assistant_message["metadata"] = search_metadata
                
                st.session_state.messages.append(assistant_message)
        
    except Exception as e:
        st.error(f"Error processing request: {e}")
        st.info("Please try again or contact support if the issue persists")
        
        # Log error
        log_user_interaction("error", {"error": str(e), "query": user_input})

def display_product_results(products):
    """Enhanced product display with better formatting"""
    
    if not products:
        return
    
    st.markdown("### 🛍️ Product Results")
    
    # Summary
    st.info(f"Found {len(products)} products matching your search")
    
    # Display products in cards
    for idx, product in enumerate(products[:6]):  # Limit to 6 results
        
        with st.container():
            st.markdown(f"""
            <div class="product-card">
                <h4>{product.get('name', 'Product')}</h4>
                
                <div style="display: flex; justify-content: space-between; align-items: center; margin: 1rem 0;">
                    <div>
                        <span style="font-size: 1.2em; font-weight: bold; color: #2c3e50;">
                            {format_currency(product.get('price', 0))}
                        </span>
                    </div>
                    <div>
                        <span style="color: #f39c12;">
                            ⭐ {product.get('rating', 'N/A')}
                        </span>
                        <span style="color: #7f8c8d; margin-left: 1rem;">
                            ({product.get('reviews', 0)} reviews)
                        </span>
                    </div>
                </div>
                
                <div style="color: #7f8c8d; margin-bottom: 1rem;">
                    🏪 {product.get('platform', 'Unknown')} | 
                    📦 {product.get('availability', 'Check website')}
                </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                if product.get('url', '#') != '#':
                    st.markdown(f"[🔗 View Product]({product['url']})")
            
            with col2:
                if st.button("🛒 Add to Cart", key=f"cart_{idx}"):
                    add_to_cart(product)
            
            with col3:
                if st.button("⚖️ Compare", key=f"compare_{idx}"):
                    start_comparison(product)
            
            st.markdown("</div>", unsafe_allow_html=True)

def show_search_metadata(metadata):
    """Display search metadata and insights"""
    
    with st.expander("🔍 Search Details", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Query:** {metadata.get('search_query', 'N/A')}")
            st.write(f"**Mode:** {metadata.get('search_mode', 'N/A')}")
        
        with col2:
            st.write(f"**Results:** {metadata.get('results_count', 0)}")
            st.write(f"**Category:** {metadata.get('category', 'general').title()}")

def show_features_panel():
    """Right panel showing features and tips"""
    
    st.markdown("## 🚀 Features")
    
    # Feature highlights
    features = [
        ("🗣️ Voice Commands", "Natural language voice search"),
        ("🔍 Smart Search", "AI-powered product discovery"),
        ("⚖️ Compare Products", "Side-by-side comparisons"),
        ("💰 Price Filters", "Budget-based filtering"),
        ("🛒 Shopping Cart", "Track selected items"),
        ("📊 Recommendations", "Personalized suggestions")
    ]
    
    for title, desc in features:
        st.markdown(f"""
        <div class="feature-card">
            <strong>{title}</strong><br>
            <small>{desc}</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick tips
    st.markdown("## 💡 Quick Tips")
    
    tips = [
        "Use specific product names for better results",
        "Include budget constraints in your search",
        "Try voice commands for hands-free browsing",
        "Compare products before making decisions",
        "Ask for recommendations based on your needs"
    ]
    
    for tip in tips:
        st.markdown(f"• {tip}")

def show_voice_interface():
    """Voice interface section"""
    
    with st.expander("🎤 Voice Commands", expanded=False):
        if hasattr(st.session_state, 'voice_handler'):
            voice_input = st.session_state.voice_handler.capture_voice()
            if voice_input:
                process_user_input(voice_input)

def show_voice_tutorial():
    """Voice tutorial dialog"""
    
    st.info("""
    🎓 **Voice Command Tutorial**
    
    **Search Commands:**
    - "Find wireless headphones under 5000"
    - "Show me latest smartphones"
    - "Search for gaming laptops"
    
    **Comparison Commands:**
    - "Compare iPhone 15 vs Samsung Galaxy S24"
    - "Which is better - MacBook or Dell laptop"
    
    **Price Commands:**
    - "Under 10000 rupees"
    - "Between 5000 and 15000"
    - "Budget options"
    
    **Cart Commands:**
    - "Add to cart"
    - "Buy this product"
    
    Try these commands for the best experience!
    """)

def show_help_dialog():
    """Show help information"""
    
    st.info("""
    ## 🎯 How to Use AI-Accelerate
    
    ### Getting Started
    1. Type or speak your product search query
    2. Browse the AI-generated results
    3. Compare products and add to cart
    4. Use voice commands for hands-free experience
    
    ### Search Tips
    - Be specific about product requirements
    - Include price range for better filtering
    - Use natural language descriptions
    - Try different search modes (Hybrid/Semantic/Traditional)
    
    ### Voice Commands
    - Enable voice in the sidebar
    - Click the microphone button to start
    - Speak clearly and wait for processing
    - Use the tutorial for command examples
    
    ### Troubleshooting
    - Refresh the page if responses are slow
    - Check your internet connection
    - Try different search terms if no results
    """)

def add_to_cart(product):
    """Add product to cart"""
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    
    st.session_state.cart.append(product)
    st.success(f"✅ Added {product.get('name', 'Product')} to cart")
    
    # Log interaction
    log_user_interaction("add_to_cart", {"product": product.get('name', 'Unknown')})

def start_comparison(product):
    """Start product comparison"""
    if 'comparison_list' not in st.session_state:
        st.session_state.comparison_list = []
    
    st.session_state.comparison_list.append(product)
    st.success(f"📊 Added {product.get('name', 'Product')} to comparison")

def show_error_page():
    """Show error page when modules fail to load"""
    
    st.error("## ❌ Application Error")
    st.markdown("""
    The application failed to initialize properly. This could be due to:
    
    - Missing Python dependencies
    - Configuration issues
    - Network connectivity problems
    
    ### 🔧 Troubleshooting Steps:
    
    1. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    
    2. **Check Configuration:**
    - Verify `.env` file exists
    - Check API keys and credentials
    
    3. **Restart Application:**
    ```bash
    streamlit run streamlit_app.py
    ```
    
    If problems persist, please check the logs or contact support.
    """)

def show_footer():
    """Application footer"""
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; padding: 1rem;">
        🤖 <strong>AI-Accelerate</strong> | Conversational Commerce Platform<br>
        Powered by Google Cloud Vertex AI & Elastic Search<br>
        <small>Built with ❤️ for the future of shopping</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Application error: {e}")
        st.code(traceback.format_exc())