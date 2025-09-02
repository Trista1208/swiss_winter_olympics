#!/usr/bin/env python3
"""
Swiss Olympic Multi-Sport Dashboard Launcher
Simple script to launch the Streamlit web interface
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit dashboard"""
    
    # Change to project root directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    print("🏔️ SWISS OLYMPIC MULTI-SPORT DASHBOARD")
    print("=" * 55)
    print("Multi-Sport Team Selection System")
    print("📊 Sports: Biathlon, Alpine Skiing, Cross-Country Skiing, Freestyle Skiing, Bobsleigh, Figure Skating")
    print("\n📝 Instructions:")
    print("1. The dashboard will open in your web browser")
    print("2. If it doesn't open automatically, go to: http://localhost:8501")
    print("3. Press Ctrl+C to stop the server")
    print("\n🚀 Launching multi-sport dashboard...")
    
    try:
        # Run streamlit on the app in src folder
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "src/app.py",
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
        print("3. Try running: streamlit run src/app.py")

if __name__ == "__main__":
    main()