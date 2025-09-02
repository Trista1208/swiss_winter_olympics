#!/usr/bin/env python3
"""
Swiss Olympic Athlete Lookup Launcher
Launch the interactive athlete search and lookup system
"""

import subprocess
import sys
import os

def main():
    """Launch the athlete lookup system"""
    
    print("🔍 SWISS OLYMPIC ATHLETE LOOKUP SYSTEM")
    print("=" * 55)
    print("Interactive search tool for Swiss Olympic athletes")
    print("\n🎯 FEATURES:")
    print("• Search athletes by name (type or select)")
    print("• Filter by sport (all sports, not just biathlon)")
    print("• Filter by gender (Men/Women)")
    print("• Check Olympic qualification status")
    print("• View detailed athlete information")
    print("• Browse recent results and performance")
    
    print("\n📝 INSTRUCTIONS:")
    print("1. The lookup tool will open in your web browser")
    print("2. If it doesn't open automatically, go to: http://localhost:8502")
    print("3. Use the search box to find specific athletes")
    print("4. Apply filters to browse by sport or gender")
    print("5. Press Ctrl+C to stop the server")
    
    print("\n🚀 Launching athlete lookup system...")
    
    try:
        # Run streamlit on a different port to avoid conflicts
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "athlete_lookup.py",
            "--server.port", "8502",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n\n✅ Athlete lookup system stopped successfully!")
    except Exception as e:
        print(f"\n❌ Error launching lookup system: {e}")
        print("\n🔧 TROUBLESHOOTING:")
        print("1. Make sure you have installed all requirements: pip install -r requirements.txt")
        print("2. Ensure all data files are present")
        print("3. Try running: streamlit run athlete_lookup.py --server.port 8502")
        print("4. Or use the dashboard: python run_dashboard.py")

if __name__ == "__main__":
    main()
