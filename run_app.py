"""
Quick Start Script for AI-Accelerate
Run this to test the application locally
"""
import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def run_streamlit_app():
    """Run the Streamlit application"""
    print("🚀 Starting AI-Accelerate...")
    
    try:
        # Set environment variables
        os.environ["STREAMLIT_SERVER_PORT"] = "8501"
        os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
        
        # Run streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main setup and run script"""
    
    print("🤖 AI-Accelerate Setup & Launch")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("streamlit_app.py"):
        print("❌ streamlit_app.py not found. Please run this from the ai-accelerate directory")
        return
    
    print("📍 Current directory:", os.getcwd())
    
    # Install dependencies
    if not install_dependencies():
        print("⚠️  Continuing without dependency installation...")
    
    print("\n🔧 Application will start in development mode with mock services")
    print("📝 For production, configure Google Cloud and Elastic credentials in .env")
    print("\n" + "=" * 40)
    
    # Run the application
    run_streamlit_app()

if __name__ == "__main__":
    main()