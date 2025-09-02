#!/usr/bin/env python3
"""
Swiss Olympic Biathlon Dashboard Launcher
Simple script to launch the Streamlit web interface
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit dashboard"""
    
    print("🏔️ SWISS OLYMPIC BIATHLON DASHBOARD")
    print("=" * 50)
    print("Starting web interface...")
    print("\n📝 Instructions:")
    print("1. The dashboard will open in your web browser")
    print("2. If it doesn't open automatically, go to: http://localhost:8501")
    print("3. Press Ctrl+C to stop the server")
    print("\n🚀 Launching dashboard...")
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard stopped successfully!")
    except Exception as e:
        print(f"\n❌ Error launching dashboard: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you have installed all requirements: pip install -r requirements.txt")
        print("2. Ensure all data files are present")
        print("3. Try running: streamlit run app.py")

if __name__ == "__main__":
    main()
