#!/usr/bin/env python3
"""
Swiss Olympic Biathlon Analysis Runner

This script runs the complete biathlon analysis and qualification checking system.
"""

import sys
import os

def run_basic_analysis():
    """Run the basic biathlon data analysis"""
    print("🏔️ STEP 1: RUNNING BASIC DATA ANALYSIS")
    print("=" * 45)
    
    try:
        # Import and run the basic analysis
        from biathlon_analysis import main as run_basic
        df = run_basic()
        
        if df is not None:
            print("\n✅ Basic analysis completed successfully!")
            return df
        else:
            print("\n❌ Basic analysis failed!")
            return None
            
    except Exception as e:
        print(f"❌ Error in basic analysis: {e}")
        return None

def run_qualification_analysis():
    """Run the qualification checking analysis"""
    print("\n🎯 STEP 2: RUNNING QUALIFICATION ANALYSIS")
    print("=" * 45)
    
    try:
        # Import and run qualification analysis
        from qualification_checker import main as run_qualification
        run_qualification()
        
        print("\n✅ Qualification analysis completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error in qualification analysis: {e}")
        return False

def main():
    """Run the complete Swiss Olympic Biathlon analysis pipeline"""
    
    print("🇨🇭 SWISS OLYMPIC BIATHLON ANALYSIS PIPELINE")
    print("=" * 55)
    print("This analysis system evaluates Swiss biathlon athletes")
    print("against the 5 Olympic qualification routes defined by")
    print("Swiss Olympic for the 2026 Milano Cortina Olympics.")
    print("=" * 55)
    
    # Step 1: Basic analysis
    df = run_basic_analysis()
    if df is None:
        print("❌ Cannot proceed without basic analysis. Exiting.")
        return False
    
    # Step 2: Qualification analysis  
    success = run_qualification_analysis()
    if not success:
        print("❌ Qualification analysis failed!")
        return False
    
    # Summary
    print("\n🏆 ANALYSIS PIPELINE COMPLETE!")
    print("=" * 35)
    print("✅ Basic data analysis: Complete")
    print("✅ Qualification checking: Complete")
    print("✅ Reports generated: Complete")
    print("\n📄 Generated Files:")
    print("  • cleaned_biathlon_results.csv - Processed dataset")
    print("  • Console output - Detailed qualification reports")
    
    print("\n🎯 NEXT STEPS:")
    print("  • Review qualification reports above")
    print("  • Analyze individual athlete performance")
    print("  • Generate visualization dashboards")
    print("  • Prepare final team selection recommendations")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)