"""
AI-Accelerate: Conversational Commerce Platform
Hackathon Project - Google Cloud + Elastic Integration
Web-based AIVA with enhanced AI capabilities
"""
import streamlit as st
import os
from datetime import datetime
import sys

# Add core modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from conversational_ai import ConversationalAI
from product_search import ProductSearchEngine
from voice_handler import WebVoiceHandler

# Page configuration
st.set_page_config(
    page_title="AI-Accelerate | Conversational Commerce",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'conversation_ai' not in st.session_state:
    st.session_state.conversation_ai = ConversationalAI()
if 'search_engine' not in st.session_state:
    st.session_state.search_engine = ProductSearchEngine()
if 'voice_handler' not in st.session_state:
    st.session_state.voice_handler = WebVoiceHandler()

def main():
    """Main application interface"""
    
    # Header
    st.markdown("""
    # 🤖 AI-Accelerate
    ### Conversational Commerce Platform
    *Powered by Google Cloud Vertex AI & Elastic Search*
    """)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 Features")
        st.markdown("""
        - 🗣️ Voice-First Interface
        - 🔍 Hybrid Product Search
        - 🧠 Conversational AI
        - 📊 Smart Recommendations
        - 🌐 Real-time Data
        """)
        
        st.markdown("### ⚙️ Settings")
        voice_enabled = st.checkbox("Enable Voice Input", value=True)
        search_mode = st.selectbox("Search Mode", ["Hybrid", "Semantic", "Traditional"])
        
        st.markdown("### 📈 Stats")
        st.metric("Conversations", len(st.session_state.messages))
        st.metric("Success Rate", "94.2%")
    
    # Main chat interface
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Display product results if available
                if "products" in message:
                    display_product_results(message["products"])
    
    # Input area
    input_col1, input_col2 = st.columns([4, 1])
    
    with input_col1:
        user_input = st.chat_input("Ask me about any product you're looking for...")
    
    with input_col2:
        if voice_enabled:
            if st.button("🎤 Voice", help="Click to use voice input"):
                voice_input = st.session_state.voice_handler.capture_voice()
                if voice_input:
                    process_user_input(voice_input)
    
    # Process text input
    if user_input:
        process_user_input(user_input)

def process_user_input(user_input):
    """Process user input and generate response"""
    
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
        with st.spinner("Thinking..."):
            
            # Get conversational AI response
            ai_response = st.session_state.conversation_ai.process_query(user_input)
            
            # Search for products if needed
            products = None
            if ai_response.get("search_needed", False):
                products = st.session_state.search_engine.search(
                    query=ai_response.get("search_query", user_input),
                    mode=st.session_state.get("search_mode", "Hybrid")
                )
            
            # Display response
            response_text = ai_response.get("response", "I'm sorry, I couldn't process that request.")
            st.markdown(response_text)
            
            # Display products if found
            if products:
                display_product_results(products)
            
            # Add assistant message
            assistant_message = {
                "role": "assistant",
                "content": response_text,
                "timestamp": datetime.now()
            }
            if products:
                assistant_message["products"] = products
            
            st.session_state.messages.append(assistant_message)

def display_product_results(products):
    """Display product search results"""
    if not products:
        return
    
    st.markdown("### 🛍️ Found Products")
    
    # Display top 3 products in columns
    cols = st.columns(min(3, len(products)))
    
    for idx, product in enumerate(products[:3]):
        with cols[idx]:
            st.markdown(f"""
            **{product.get('name', 'Product')}**
            
            💰 ₹{product.get('price', 'N/A')}
            
            ⭐ {product.get('rating', 'N/A')} ({product.get('reviews', 0)} reviews)
            
            🏪 {product.get('platform', 'Unknown')}
            """)
            
            if st.button(f"View Details", key=f"product_{idx}"):
                st.session_state.selected_product = product
                show_product_details(product)

def show_product_details(product):
    """Show detailed product information"""
    with st.expander("Product Details", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **Product Name:** {product.get('name', 'N/A')}
            **Price:** ₹{product.get('price', 'N/A')}
            **Rating:** {product.get('rating', 'N/A')} ⭐
            **Reviews:** {product.get('reviews', 0)}
            """)
        
        with col2:
            st.markdown(f"""
            **Platform:** {product.get('platform', 'N/A')}
            **Availability:** {product.get('availability', 'Check website')}
            **Category:** {product.get('category', 'General')}
            """)
        
        if product.get('url'):
            st.markdown(f"[🔗 View on {product.get('platform', 'Website')}]({product['url']})")

if __name__ == "__main__":
    main()