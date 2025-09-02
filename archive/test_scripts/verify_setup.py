#!/usr/bin/env python3
"""
Setup Verification Script for Swiss Olympic Biathlon Analysis System
Verifies that all dependencies are correctly installed and the system is ready to use
"""

import sys
import importlib
from datetime import datetime

def check_python_version():
    """Check if Python version meets requirements"""
    version = sys.version_info
    min_version = (3, 8)
    
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version >= min_version:
        print("✅ Python version requirement met")
        return True
    else:
        print(f"❌ Python {min_version[0]}.{min_version[1]}+ required")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed and importable"""
    if import_name is None:
        import_name = package_name
    
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', 'Unknown')
        print(f"✅ {package_name}: {version}")
        return True
    except ImportError:
        print(f"❌ {package_name}: Not installed")
        return False

def check_data_files():
    """Check if required data files are present"""
    import os
    
    required_files = [
        'Results_Test_Version.csv',
        'criterias/Biathlon_Hauptkriterien.txt',
        'Task_description.pdf'
    ]
    
    all_present = True
    print("\n📁 Data Files:")
    
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✅ {file} ({size:,} bytes)")
        else:
            print(f"❌ {file}: Missing")
            all_present = False
    
    return all_present

def check_system_components():
    """Check if our custom modules can be imported"""
    print("\n🔧 System Components:")
    
    components = [
        'biathlon_analysis',
        'qualification_checker',
        'athlete_lookup',
        'app'
    ]
    
    all_working = True
    
    for component in components:
        try:
            importlib.import_module(component)
            print(f"✅ {component}.py: Working")
        except ImportError as e:
            print(f"❌ {component}.py: Error - {e}")
            all_working = False
    
    return all_working

def main():
    """Main verification function"""
    
    print("🏔️ SWISS OLYMPIC BIATHLON ANALYSIS SYSTEM")
    print("=" * 55)
    print("🔍 Setup Verification - Milano Cortina 2026")
    print(f"⏰ Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n📋 SYSTEM REQUIREMENTS CHECK:")
    print("-" * 35)
    
    # Check Python version
    python_ok = check_python_version()
    
    # Check required packages
    print("\n📦 Package Dependencies:")
    packages = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('streamlit', 'streamlit'),
        ('plotly', 'plotly'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn')
    ]
    
    packages_ok = True
    for package, import_name in packages:
        if not check_package(package, import_name):
            packages_ok = False
    
    # Check data files
    files_ok = check_data_files()
    
    # Check system components
    components_ok = check_system_components()
    
    # Overall status
    print(f"\n{'=' * 55}")
    print("📊 VERIFICATION SUMMARY:")
    
    all_checks = [
        ("Python Version", python_ok),
        ("Package Dependencies", packages_ok),
        ("Data Files", files_ok),
        ("System Components", components_ok)
    ]
    
    all_passed = True
    for check_name, status in all_checks:
        icon = "✅" if status else "❌"
        print(f"{icon} {check_name}: {'PASSED' if status else 'FAILED'}")
        if not status:
            all_passed = False
    
    print(f"\n🎯 OVERALL STATUS: {'✅ READY' if all_passed else '❌ NEEDS ATTENTION'}")
    
    if all_passed:
        print("\n🚀 READY TO LAUNCH:")
        print("• Athlete Lookup: python run_lookup.py")
        print("• Analytics Dashboard: python run_dashboard.py")
        print("• Command Line: python run_analysis.py")
        print("\n🏔️ Milano Cortina 2026 Olympics - Team Selection Ready!")
    else:
        print("\n🔧 NEXT STEPS:")
        if not python_ok:
            print("• Upgrade Python to 3.8+")
        if not packages_ok:
            print("• Install missing packages: pip install -r requirements.txt")
        if not files_ok:
            print("• Ensure data files are in project directory")
        if not components_ok:
            print("• Check for syntax errors in Python files")

if __name__ == "__main__":
    main()
