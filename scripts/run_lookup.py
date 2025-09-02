#!/usr/bin/env python3
"""
Swiss Olympic Athlete Lookup Launcher
Simple script to launch the athlete search interface
"""

import subprocess
import sys
import os

def main():
    """Launch the athlete lookup interface"""
    
    # Change to project root directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    print("🔍 SWISS OLYMPIC ATHLETE LOOKUP")
    print("=" * 45)
    print("Interactive athlete search and qualification checker")
    print("📊 Search across all 6 sports with detailed qualification status")
    print("\n📝 Instructions:")
    print("1. The lookup interface will open in your web browser")
    print("2. If it doesn't open automatically, go to: http://localhost:8502")
    print("3. Press Ctrl+C to stop the server")
    print("\n🚀 Launching athlete lookup...")
    
    try:
        # Run streamlit on the athlete lookup in src folder
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "src/athlete_lookup.py",
            "--server.port", "8502",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n\n✅ Athlete lookup stopped successfully!")
    except Exception as e:
        print(f"\n❌ Error launching athlete lookup: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you have installed all requirements: pip install -r requirements.txt")
        print("2. Ensure all data files are present")
        print("3. Try running: streamlit run src/athlete_lookup.py")

if __name__ == "__main__":
    main()
