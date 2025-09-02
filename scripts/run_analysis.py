#!/usr/bin/env python3
"""
Swiss Olympic Multi-Sport Analysis Launcher
Command-line analysis across all sports
"""

import sys
import os

# Add src to path for imports
sys.path.insert(0, 'src')

def main():
    """Run multi-sport analysis"""
    
    # Change to project root directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    print("🏔️ SWISS OLYMPIC MULTI-SPORT ANALYSIS")
    print("=" * 50)
    print("Command-line analysis across all 6 sports")
    print("\n🚀 Running comprehensive analysis...")
    
    try:
        from multi_sport_analysis import main as run_analysis
        run_analysis()
    except Exception as e:
        print(f"\n❌ Error running analysis: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you have installed all requirements: pip install -r requirements.txt")
        print("2. Ensure all data files are present in data/ folder")

if __name__ == "__main__":
    main()