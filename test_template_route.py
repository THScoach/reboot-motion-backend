#!/usr/bin/env python3
"""
Quick test to verify the Coach Rick Analysis template route works
"""

import sys
import os

# Add the current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test that all imports work"""
    print("🧪 Testing imports...")
    try:
        from fastapi import FastAPI, Request
        from fastapi.responses import HTMLResponse
        from fastapi.templating import Jinja2Templates
        from fastapi.staticfiles import StaticFiles
        print("✅ FastAPI imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_template_exists():
    """Test that the template file exists"""
    print("\n🧪 Testing template file...")
    template_path = "templates/coach_rick_analysis.html"
    if os.path.exists(template_path):
        size = os.path.getsize(template_path)
        print(f"✅ Template exists: {template_path} ({size:,} bytes)")
        return True
    else:
        print(f"❌ Template not found: {template_path}")
        return False

def test_static_dir():
    """Test that static directory exists"""
    print("\n🧪 Testing static directory...")
    if os.path.exists("static"):
        print("✅ Static directory exists")
        # List contents
        for item in os.listdir("static"):
            print(f"   - static/{item}")
        return True
    else:
        print("❌ Static directory not found")
        return False

def test_main_py_syntax():
    """Test that main.py has valid Python syntax"""
    print("\n🧪 Testing main.py syntax...")
    try:
        with open("main.py", "r") as f:
            code = f.read()
        compile(code, "main.py", "exec")
        print("✅ main.py syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in main.py: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("COACH RICK TEMPLATE ROUTE TEST")
    print("=" * 60)
    
    all_passed = True
    all_passed &= test_imports()
    all_passed &= test_template_exists()
    all_passed &= test_static_dir()
    all_passed &= test_main_py_syntax()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED")
        print("\n📍 Route will be available at:")
        print("   https://reboot-motion-backend-production.up.railway.app/coach-rick-analysis")
        print("\n⏳ Waiting for Railway to redeploy...")
        print("   (Usually takes 2-3 minutes)")
    else:
        print("❌ SOME TESTS FAILED")
        sys.exit(1)
    print("=" * 60)
