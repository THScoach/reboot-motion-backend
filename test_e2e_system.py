#!/usr/bin/env python3
"""
CATCHING BARRELS - END-TO-END SYSTEM TEST
==========================================
Priority 13: End-to-End Testing
Priority 15: Eric Williams Validation

Tests the complete system flow:
1. CSV Upload → Analysis → Training Plan → Coach Take
2. API endpoint validation
3. Error handling
4. Performance benchmarks
"""

import requests
import json
import time
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8006"
TEST_DATA_DIR = Path(__file__).parent / "catching_barrels_package"

# Color codes for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_header(text):
    """Print formatted header"""
    print(f"\n{BOLD}{BLUE}{'='*80}{RESET}")
    print(f"{BOLD}{BLUE}{text.center(80)}{RESET}")
    print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")

def print_test(name, status, details=""):
    """Print test result"""
    symbol = "✓" if status else "✗"
    color = GREEN if status else RED
    print(f"{color}{symbol} {name}{RESET}")
    if details:
        print(f"  {details}")

def print_metric(name, value):
    """Print metric"""
    print(f"{YELLOW}  • {name}:{RESET} {value}")

class SystemTester:
    """Complete system tester"""
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.results = {
            "passed": 0,
            "failed": 0,
            "total": 0
        }
    
    def test(self, name, func):
        """Run a test"""
        self.results["total"] += 1
        try:
            start_time = time.time()
            result = func()
            elapsed = time.time() - start_time
            
            if result.get("success"):
                self.results["passed"] += 1
                print_test(name, True, f"Time: {elapsed:.2f}s")
                if "metrics" in result:
                    for key, value in result["metrics"].items():
                        print_metric(key, value)
                return True
            else:
                self.results["failed"] += 1
                print_test(name, False, result.get("error", "Test failed"))
                return False
        except Exception as e:
            self.results["failed"] += 1
            print_test(name, False, f"Exception: {str(e)}")
            return False
    
    def test_health_endpoints(self):
        """Test 1: Health Endpoints"""
        print_header("TEST 1: HEALTH ENDPOINTS")
        
        def test_main_health():
            resp = requests.get(f"{self.base_url}/health", timeout=5)
            return {
                "success": resp.status_code == 200,
                "metrics": {
                    "Status Code": resp.status_code,
                    "Service": resp.json().get("service", "N/A")
                }
            }
        
        def test_coach_rick_health():
            resp = requests.get(f"{self.base_url}/api/v1/reboot-lite/coach-rick/health", timeout=5)
            return {
                "success": resp.status_code == 200,
                "metrics": {
                    "Status Code": resp.status_code,
                    "Status": resp.json().get("status", "N/A")
                }
            }
        
        def test_swing_dna_health():
            resp = requests.get(f"{self.base_url}/api/swing-dna/health", timeout=5)
            return {
                "success": resp.status_code == 200,
                "metrics": {
                    "Status Code": resp.status_code,
                    "System Status": resp.json().get("status", "N/A")
                }
            }
        
        self.test("Main API Health", test_main_health)
        self.test("Coach Rick Health", test_coach_rick_health)
        self.test("Swing DNA Health", test_swing_dna_health)
    
    def test_whop_integration(self):
        """Test 2: Whop Integration"""
        print_header("TEST 2: WHOP INTEGRATION")
        
        def test_webhook_status():
            resp = requests.get(f"{self.base_url}/webhooks/whop/status", timeout=5)
            return {
                "success": resp.status_code == 200,
                "metrics": {
                    "Status Code": resp.status_code,
                    "Webhook Ready": "Yes" if resp.status_code == 200 else "No"
                }
            }
        
        def test_subscription_check():
            # Test with dummy user ID
            resp = requests.get(
                f"{self.base_url}/api/subscription/status",
                params={"user_id": "test_user_123"},
                timeout=5
            )
            return {
                "success": resp.status_code in [200, 404],  # 404 is OK for non-existent user
                "metrics": {
                    "Status Code": resp.status_code,
                    "Response": "Valid API response"
                }
            }
        
        self.test("Webhook Status", test_webhook_status)
        self.test("Subscription Check", test_subscription_check)
    
    def test_swing_dna_csv_analysis(self):
        """Test 3: Swing DNA CSV Analysis (Eric Williams Data)"""
        print_header("TEST 3: SWING DNA CSV ANALYSIS - ERIC WILLIAMS")
        
        # Locate Eric Williams CSV files
        momentum_file = TEST_DATA_DIR / "eric_williams_momentum_energy.csv"
        kinematics_file = TEST_DATA_DIR / "eric_williams_inverse_kinematics.csv"
        
        # If not found, try alternate names
        if not momentum_file.exists():
            possible_momentum = list(TEST_DATA_DIR.glob("*momentum*.csv"))
            if possible_momentum:
                momentum_file = possible_momentum[0]
        
        if not kinematics_file.exists():
            possible_kinematics = list(TEST_DATA_DIR.glob("*kinematic*.csv"))
            if possible_kinematics:
                kinematics_file = possible_kinematics[0]
        
        def test_csv_upload():
            """Test CSV file upload and analysis"""
            if not momentum_file.exists() or not kinematics_file.exists():
                return {
                    "success": False,
                    "error": f"CSV files not found. Momentum: {momentum_file.exists()}, Kinematics: {kinematics_file.exists()}"
                }
            
            try:
                # Prepare multipart form data
                files = {
                    "momentum_file": (momentum_file.name, open(momentum_file, "rb"), "text/csv"),
                    "kinematics_file": (kinematics_file.name, open(kinematics_file, "rb"), "text/csv")
                }
                
                data = {
                    "athlete_name": "Eric Williams",
                    "athlete_email": "eric.williams@test.com",
                    "analysis_type": "full"
                }
                
                # Make request
                resp = requests.post(
                    f"{self.base_url}/api/swing-dna/analyze",
                    files=files,
                    data=data,
                    timeout=30
                )
                
                # Close files
                for f in files.values():
                    f[1].close()
                
                if resp.status_code != 200:
                    return {
                        "success": False,
                        "error": f"HTTP {resp.status_code}: {resp.text[:200]}"
                    }
                
                result = resp.json()
                
                # Validate response structure
                required_keys = ["analysis_id", "status", "athlete", "pattern_diagnosis", "training_plan"]
                missing_keys = [k for k in required_keys if k not in result]
                
                if missing_keys:
                    return {
                        "success": False,
                        "error": f"Missing keys: {missing_keys}"
                    }
                
                return {
                    "success": True,
                    "metrics": {
                        "Analysis ID": result.get("analysis_id"),
                        "Status": result.get("status"),
                        "Pattern": result.get("pattern_diagnosis", {}).get("primary_pattern", {}).get("type", "N/A"),
                        "Severity": result.get("pattern_diagnosis", {}).get("primary_pattern", {}).get("severity", "N/A"),
                        "Training Weeks": len(result.get("training_plan", {}).get("weekly_plans", [])),
                        "Coach Take": "Generated" if "coaches_take" in result else "Missing"
                    }
                }
            
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Exception: {str(e)}"
                }
        
        self.test("CSV Upload & Analysis", test_csv_upload)
    
    def test_protocols_endpoint(self):
        """Test 4: Training Protocols"""
        print_header("TEST 4: TRAINING PROTOCOLS")
        
        def test_get_protocols():
            resp = requests.get(f"{self.base_url}/api/swing-dna/protocols", timeout=5)
            if resp.status_code != 200:
                return {"success": False, "error": f"HTTP {resp.status_code}"}
            
            protocols = resp.json()
            return {
                "success": len(protocols) > 0,
                "metrics": {
                    "Total Protocols": len(protocols),
                    "Sample Protocol": protocols[0].get("name", "N/A") if protocols else "N/A"
                }
            }
        
        self.test("Get Training Protocols", test_get_protocols)
    
    def test_error_handling(self):
        """Test 5: Error Handling"""
        print_header("TEST 5: ERROR HANDLING")
        
        def test_invalid_csv():
            """Test with invalid CSV data"""
            files = {
                "momentum_energy_file": ("test.csv", b"invalid,data\n1,2,3", "text/csv"),
                "inverse_kinematics_file": ("test2.csv", b"invalid,data\n1,2,3", "text/csv")
            }
            
            data = {
                "athlete_name": "Test Athlete",
                "athlete_email": "test@test.com"
            }
            
            resp = requests.post(
                f"{self.base_url}/api/swing-dna/analyze",
                files=files,
                data=data,
                timeout=10
            )
            
            # Should return error (4xx or 5xx) or handle gracefully
            return {
                "success": resp.status_code >= 400 or (resp.status_code == 200 and "error" in resp.json()),
                "metrics": {
                    "Status Code": resp.status_code,
                    "Error Handled": "Yes"
                }
            }
        
        def test_missing_file():
            """Test with missing file"""
            files = {
                "momentum_energy_file": ("test.csv", b"data", "text/csv")
                # Missing inverse_kinematics_file
            }
            
            resp = requests.post(
                f"{self.base_url}/api/swing-dna/analyze",
                files=files,
                timeout=10
            )
            
            return {
                "success": resp.status_code >= 400,
                "metrics": {
                    "Status Code": resp.status_code,
                    "Error Type": "Missing Required File"
                }
            }
        
        self.test("Invalid CSV Handling", test_invalid_csv)
        self.test("Missing File Handling", test_missing_file)
    
    def test_performance(self):
        """Test 6: Performance Benchmarks"""
        print_header("TEST 6: PERFORMANCE BENCHMARKS")
        
        def test_health_response_time():
            times = []
            for _ in range(5):
                start = time.time()
                requests.get(f"{self.base_url}/health", timeout=5)
                times.append(time.time() - start)
            
            avg_time = sum(times) / len(times)
            return {
                "success": avg_time < 1.0,  # Should be under 1 second
                "metrics": {
                    "Avg Response Time": f"{avg_time*1000:.0f}ms",
                    "Max Response Time": f"{max(times)*1000:.0f}ms",
                    "Min Response Time": f"{min(times)*1000:.0f}ms"
                }
            }
        
        self.test("Health Endpoint Performance", test_health_response_time)
    
    def print_summary(self):
        """Print test summary"""
        print_header("TEST SUMMARY")
        
        total = self.results["total"]
        passed = self.results["passed"]
        failed = self.results["failed"]
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"{BOLD}Total Tests:{RESET} {total}")
        print(f"{GREEN}Passed:{RESET} {passed}")
        print(f"{RED}Failed:{RESET} {failed}")
        print(f"{YELLOW}Pass Rate:{RESET} {pass_rate:.1f}%")
        
        if pass_rate >= 80:
            print(f"\n{GREEN}{BOLD}✓ SYSTEM READY FOR PRODUCTION{RESET}")
        elif pass_rate >= 60:
            print(f"\n{YELLOW}{BOLD}⚠ SYSTEM NEEDS ATTENTION{RESET}")
        else:
            print(f"\n{RED}{BOLD}✗ SYSTEM NOT READY{RESET}")
        
        return pass_rate >= 80

def main():
    """Run all tests"""
    print_header("CATCHING BARRELS - END-TO-END SYSTEM TEST")
    print(f"Base URL: {BASE_URL}")
    print(f"Test Data: {TEST_DATA_DIR}")
    
    tester = SystemTester(BASE_URL)
    
    # Run test suites
    tester.test_health_endpoints()
    tester.test_whop_integration()
    tester.test_swing_dna_csv_analysis()
    tester.test_protocols_endpoint()
    tester.test_error_handling()
    tester.test_performance()
    
    # Print summary
    ready = tester.print_summary()
    
    return 0 if ready else 1

if __name__ == "__main__":
    exit(main())
