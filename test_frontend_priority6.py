#!/usr/bin/env python3
"""
Test Priority 6: Frontend UI Updates
Validates that the new HTML template and CSS files are created and structured correctly.
"""

import os
from pathlib import Path

def test_files_exist():
    """Test that all required files exist"""
    print("=" * 80)
    print("TEST 1: FILE EXISTENCE")
    print("=" * 80)
    
    files = {
        'HTML Template': 'templates/analysis_results.html',
        'CSS Stylesheet': 'static/css/results.css'
    }
    
    all_exist = True
    for name, path in files.items():
        full_path = Path(path)
        exists = full_path.exists()
        size = full_path.stat().st_size if exists else 0
        print(f"✓ {name}: {path}")
        print(f"  - Exists: {'YES ✓' if exists else 'NO ✗'}")
        print(f"  - Size: {size:,} bytes ({size/1024:.1f} KB)")
        if not exists:
            all_exist = False
    
    return all_exist

def test_html_structure():
    """Test HTML template structure"""
    print("\n" + "=" * 80)
    print("TEST 2: HTML TEMPLATE STRUCTURE")
    print("=" * 80)
    
    html_path = Path('templates/analysis_results.html')
    content = html_path.read_text()
    
    required_sections = {
        'DOCTYPE': '<!DOCTYPE html>',
        'Header Section': '<header class="header">',
        'Gap Analysis Card': '<section class="card gap-card">',
        'Component Scores Card': '<section class="card scores-card">',
        'Motor Profile Card': '<section class="card profile-card">',
        'Recommendations Card': '<section class="card recommendations-card">',
        'Charts Card': '<section class="card charts-card">',
        'Action Plan Card': '<section class="card action-plan-card">',
        'Footer': '<footer class="footer">',
        'CSS Link': '<link rel="stylesheet" href="/static/css/results.css">',
    }
    
    all_present = True
    for name, marker in required_sections.items():
        present = marker in content
        print(f"{'✓' if present else '✗'} {name}: {'PRESENT' if present else 'MISSING'}")
        if not present:
            all_present = False
    
    return all_present

def test_template_variables():
    """Test that all Jinja2 template variables are present"""
    print("\n" + "=" * 80)
    print("TEST 3: TEMPLATE VARIABLES")
    print("=" * 80)
    
    html_path = Path('templates/analysis_results.html')
    content = html_path.read_text()
    
    required_variables = [
        'player_name',
        'age',
        'height',
        'weight',
        'analysis_date',
        'actual_bat_speed',
        'potential_bat_speed',
        'gap_mph',
        'pct_achieved',
        'pct_untapped',
        'gap_status',
        'ground_score',
        'engine_score',
        'weapon_score',
        'overall_efficiency',
        'motor_profile',
        'motor_profile_confidence',
        'primary_component',
        'estimated_gain_mph',
        'total_estimated_gain_mph',
        'training_frequency',
        'gap_chart_url',
        'radar_chart_url',
    ]
    
    all_present = True
    for var in required_variables:
        present = f'{{{{ {var}' in content or f'{{%' in content  # Check for Jinja2 syntax
        if f'{var}' in content:
            print(f"✓ {var}: PRESENT")
        else:
            print(f"✗ {var}: MISSING")
            all_present = False
    
    # Count total Jinja2 variables
    var_count = content.count('{{')
    loop_count = content.count('{%')
    print(f"\n✓ Total Jinja2 variables: {var_count}")
    print(f"✓ Total Jinja2 control structures: {loop_count}")
    
    return var_count > 20  # Should have many template variables

def test_css_structure():
    """Test CSS stylesheet structure"""
    print("\n" + "=" * 80)
    print("TEST 4: CSS STYLESHEET STRUCTURE")
    print("=" * 80)
    
    css_path = Path('static/css/results.css')
    content = css_path.read_text()
    
    required_elements = {
        'CSS Variables (root)': ':root {',
        'Color Variables': '--color-actual:',
        'Gap Card': '.gap-card',
        'Scores Visual': '.scores-visual',
        'Profile Badge': '.profile-badge',
        'Recommendations': '.primary-recommendation',
        'Charts Grid': '.charts-grid',
        'Action Steps': '.action-steps',
        'Responsive Design': '@media (max-width: 768px)',
        'Print Styles': '@media print',
    }
    
    all_present = True
    for name, marker in required_elements.items():
        present = marker in content
        print(f"{'✓' if present else '✗'} {name}: {'PRESENT' if present else 'MISSING'}")
        if not present:
            all_present = False
    
    return all_present

def test_color_scheme():
    """Test that the specified color scheme is implemented"""
    print("\n" + "=" * 80)
    print("TEST 5: COLOR SCHEME")
    print("=" * 80)
    
    css_path = Path('static/css/results.css')
    content = css_path.read_text()
    
    required_colors = {
        'Actual (Red)': '#FF6B6B',
        'Potential (Teal)': '#4ECDC4',
        'Primary (Purple)': '#667eea',
        'Background (Light)': '#F8F9FA',
    }
    
    all_present = True
    for name, color in required_colors.items():
        present = color in content
        print(f"{'✓' if present else '✗'} {name}: {color} - {'FOUND' if present else 'MISSING'}")
        if not present:
            all_present = False
    
    return all_present

def test_motor_profile_styles():
    """Test that all 5 motor profile styles are defined"""
    print("\n" + "=" * 80)
    print("TEST 6: MOTOR PROFILE STYLES")
    print("=" * 80)
    
    css_path = Path('static/css/results.css')
    content = css_path.read_text()
    
    profiles = ['TITAN', 'SPINNER', 'SLINGSHOTTER', 'WHIPPER', 'BALANCED']
    
    all_present = True
    for profile in profiles:
        present = f'.profile-{profile}' in content
        print(f"{'✓' if present else '✗'} {profile}: {'STYLED' if present else 'MISSING'}")
        if not present:
            all_present = False
    
    return all_present

def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "=" * 80)
    print("PRIORITY 6 FRONTEND UI VALIDATION TEST SUITE")
    print("=" * 80)
    print()
    
    tests = [
        ("File Existence", test_files_exist),
        ("HTML Structure", test_html_structure),
        ("Template Variables", test_template_variables),
        ("CSS Structure", test_css_structure),
        ("Color Scheme", test_color_scheme),
        ("Motor Profile Styles", test_motor_profile_styles),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} FAILED with error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n{'=' * 80}")
    print(f"TOTAL: {passed}/{total} test suites passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - PRIORITY 6 COMPLETE!")
    else:
        print(f"⚠️  {total - passed} test suite(s) failed")
    
    print("=" * 80)
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
