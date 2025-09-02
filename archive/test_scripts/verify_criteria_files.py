#!/usr/bin/env python3
"""
Verification script for Swiss Olympic qualification criteria files
Checks that all sport criteria files are properly formatted and complete
"""

import os
from datetime import datetime

def check_criteria_file(filename):
    """Check if a criteria file exists and has proper structure"""
    
    if not os.path.exists(filename):
        return False, f"File {filename} not found"
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for required sections
        required_sections = [
            'Sport:',
            'Is Olympic Discipline:',
            'Class:',
            'Team Members:',
            'selection_paths:',
            'any_of:',
            '# Route 1:',
            '# Route 2:',
            '# Route 3:',
            '# Route 4:',
            '# Route 5:'
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            return False, f"Missing sections: {', '.join(missing_sections)}"
        
        # Check file size (should be substantial)
        if len(content) < 1000:
            return False, "File appears too short"
        
        return True, f"Valid criteria file ({len(content.split())} words)"
        
    except Exception as e:
        return False, f"Error reading file: {e}"

def main():
    """Main verification function"""
    
    print("🏔️ SWISS OLYMPIC QUALIFICATION CRITERIA VERIFICATION")
    print("=" * 65)
    print("🔍 Milano Cortina 2026 - Criteria Files Check")
    print(f"⏰ Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # List of all sports criteria files
    criteria_files = [
        ("Biathlon", "criterias/Biathlon_Hauptkriterien.txt"),
        ("Alpine Skiing", "criterias/Alpine_Skiing_Hauptkriterien.txt"),
        ("Cross-Country Skiing", "criterias/Cross_Country_Skiing_Hauptkriterien.txt"),
        ("Freestyle Skiing", "criterias/Freestyle_Skiing_Hauptkriterien.txt"),
        ("Bobsleigh", "criterias/Bobsleigh_Hauptkriterien.txt"),
        ("Figure Skating", "criterias/Figure_Skating_Hauptkriterien.txt")
    ]
    
    print(f"\n📋 CHECKING {len(criteria_files)} SPORTS CRITERIA FILES:")
    print("-" * 50)
    
    all_valid = True
    
    for sport_name, filename in criteria_files:
        is_valid, message = check_criteria_file(filename)
        
        status_icon = "✅" if is_valid else "❌"
        print(f"{status_icon} {sport_name:20} | {message}")
        
        if not is_valid:
            all_valid = False
    
    # Check overview file
    print(f"\n📊 CHECKING OVERVIEW DOCUMENTATION:")
    print("-" * 35)
    
    overview_valid, overview_msg = check_criteria_file("criterias/Swiss_Olympic_Qualification_Overview.txt")
    overview_icon = "✅" if overview_valid else "❌"
    print(f"{overview_icon} Overview Document    | {overview_msg}")
    
    if not overview_valid:
        all_valid = False
    
    # Summary
    print(f"\n{'=' * 65}")
    print("📊 VERIFICATION SUMMARY:")
    
    total_files = len(criteria_files) + 1  # +1 for overview
    valid_files = sum(1 for _, f in criteria_files if check_criteria_file(f)[0])
    if overview_valid:
        valid_files += 1
    
    print(f"📁 Total Files: {total_files}")
    print(f"✅ Valid Files: {valid_files}")
    print(f"❌ Invalid Files: {total_files - valid_files}")
    
    overall_status = "✅ ALL CRITERIA FILES READY" if all_valid else "❌ SOME FILES NEED ATTENTION"
    print(f"\n🎯 OVERALL STATUS: {overall_status}")
    
    if all_valid:
        print("\n🚀 READY FOR IMPLEMENTATION:")
        print("• All sports have qualification criteria defined")
        print("• Files follow consistent structure")
        print("• Milano Cortina 2026 Olympics preparation complete")
        
        print("\n📈 NEXT STEPS:")
        print("• Implement qualification checkers for other sports")
        print("• Integrate multi-sport analysis into athlete lookup")
        print("• Create sport-specific dashboards")
    else:
        print("\n🔧 ACTIONS NEEDED:")
        print("• Fix missing or invalid criteria files")
        print("• Ensure all sports have complete qualification paths")
        print("• Verify file formatting and structure")
    
    print(f"\n🏔️ Swiss Olympic Team Selection - Milano Cortina 2026")

if __name__ == "__main__":
    main()
