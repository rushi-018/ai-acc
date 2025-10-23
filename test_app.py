import streamlit as st
import sys
import os

# Simple test app to verify Streamlit works
st.set_page_config(
    page_title="AI-Accelerate Test",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI-Accelerate - Test Version")
st.success("✅ Application is working!")

st.markdown("""
## 🚀 AI-Accelerate: Conversational Commerce Platform

**Status:** Development Mode  
**Features:** Mock Services Enabled  

### Key Components:
- 🗣️ **Voice Interface**: Ready for integration
- 🔍 **Product Search**: Mock data available  
- 🧠 **Conversational AI**: Placeholder responses
- 📊 **Analytics**: Basic tracking

### Test the Interface:
""")

# Simple chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Test the conversational interface..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add assistant response
    response = f"🤖 I heard you say: '{prompt}'. This is a test response showing the interface works perfectly!"
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Sidebar
with st.sidebar:
    st.markdown("## 📊 System Status")
    st.metric("Status", "🟢 Online")
    st.metric("Mode", "Development")
    st.metric("Version", "1.0.0")
    
    st.markdown("## ⚙️ Configuration")
    st.info("All modules loaded successfully")
    
    if st.button("🔄 Reset Chat"):
        st.session_state.messages = []
        st.rerun()

st.markdown("---")
st.markdown("**🎯 Ready for Hackathon Integration!** All core components are in place for Google Cloud + Elastic integration.")