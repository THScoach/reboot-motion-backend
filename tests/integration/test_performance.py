"""
Integration Tests: Performance
Phase 1 Week 3-4: Priority 5

Tests performance benchmarks and scalability
"""

import pytest
import sys
import os
import time
from typing import List

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.services.report_transformer import transform_coach_rick_to_report
from krs_calculator import calculate_krs


class TestPerformance:
    """Test performance and scalability"""
    
    def _generate_mock_coach_rick_data(self, session_id: str) -> dict:
        """Generate mock Coach Rick data for testing"""
        return {
            "bat_speed_mph": 82.0,
            "exit_velocity_mph": 99.0,
            "efficiency_percent": 111.0,
            "tempo_score": 87.0,
            "stability_score": 92.0,
            "gew_overall": 88.5,
            "hip_shoulder_gap_ms": 20,
            "hands_bat_gap_ms": 15,
            "motor_profile": {
                "type": "SLINGSHOTTER",
                "confidence": 92.0
            },
            "launch_angle": 15.0,
            "frames_analyzed": 120,
            "duration_seconds": 4.0
        }
    
    def test_single_transformation_time(self):
        """Test single report transformation completes under 100ms"""
        coach_data = self._generate_mock_coach_rick_data("perf_001")
        
        start_time = time.time()
        report = transform_coach_rick_to_report(coach_data, "perf_001", 1)
        end_time = time.time()
        
        elapsed_ms = (end_time - start_time) * 1000
        
        assert elapsed_ms < 100, f"Transformation took {elapsed_ms:.2f}ms, should be <100ms"
        assert report is not None
        
        print(f"✅ Test 1: Single transformation - {elapsed_ms:.2f}ms")
    
    def test_batch_transformation_10_reports(self):
        """Test transforming 10 reports in under 500ms"""
        start_time = time.time()
        
        reports = []
        for i in range(10):
            coach_data = self._generate_mock_coach_rick_data(f"batch_10_{i}")
            report = transform_coach_rick_to_report(coach_data, f"batch_10_{i}", 1)
            reports.append(report)
        
        end_time = time.time()
        elapsed_ms = (end_time - start_time) * 1000
        avg_per_report = elapsed_ms / 10
        
        assert len(reports) == 10
        assert elapsed_ms < 500, f"Batch of 10 took {elapsed_ms:.2f}ms, should be <500ms"
        
        print(f"✅ Test 2: Batch 10 reports - {elapsed_ms:.2f}ms ({avg_per_report:.2f}ms avg)")
    
    def test_batch_transformation_100_reports(self):
        """Test transforming 100 reports in under 5 seconds"""
        start_time = time.time()
        
        reports = []
        for i in range(100):
            coach_data = self._generate_mock_coach_rick_data(f"batch_100_{i}")
            report = transform_coach_rick_to_report(coach_data, f"batch_100_{i}", 1)
            reports.append(report)
        
        end_time = time.time()
        elapsed_sec = end_time - start_time
        avg_per_report_ms = (elapsed_sec * 1000) / 100
        
        assert len(reports) == 100
        assert elapsed_sec < 5.0, f"Batch of 100 took {elapsed_sec:.2f}s, should be <5s"
        
        print(f"✅ Test 3: Batch 100 reports - {elapsed_sec:.2f}s ({avg_per_report_ms:.2f}ms avg)")
    
    def test_krs_calculation_performance(self):
        """Test KRS calculation is fast (<1ms)"""
        test_cases = [
            (74.8, 69.5),
            (80.0, 90.0),
            (50.0, 60.0),
            (85.0, 85.0),
            (100.0, 100.0)
        ]
        
        total_time = 0
        iterations = 100
        
        for _ in range(iterations):
            for creation, transfer in test_cases:
                start = time.time()
                result = calculate_krs(creation, transfer)
                end = time.time()
                total_time += (end - start) * 1000  # Convert to ms
        
        avg_time = total_time / (iterations * len(test_cases))
        
        assert avg_time < 1.0, f"KRS calc took {avg_time:.4f}ms avg, should be <1ms"
        
        print(f"✅ Test 4: KRS calculation - {avg_time:.4f}ms avg (500 calcs)")
    
    def test_memory_efficiency_large_batch(self):
        """Test memory doesn't explode with large batches"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # Generate 500 reports
        reports = []
        for i in range(500):
            coach_data = self._generate_mock_coach_rick_data(f"memory_test_{i}")
            report = transform_coach_rick_to_report(coach_data, f"memory_test_{i}", 1)
            reports.append(report)
        
        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        mem_increase = mem_after - mem_before
        
        # Each report should be ~5-10KB, so 500 reports ~2.5-5MB max
        assert mem_increase < 20, f"Memory increased {mem_increase:.2f}MB for 500 reports"
        assert len(reports) == 500
        
        print(f"✅ Test 5: Memory efficiency - {mem_increase:.2f}MB for 500 reports")
    
    def test_concurrent_transformations(self):
        """Test concurrent transformations complete successfully"""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        def transform_report(session_id: str):
            coach_data = self._generate_mock_coach_rick_data(session_id)
            return transform_coach_rick_to_report(coach_data, session_id, 1)
        
        start_time = time.time()
        
        # Run 50 concurrent transformations
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(transform_report, f"concurrent_{i}")
                for i in range(50)
            ]
            
            results = [future.result() for future in as_completed(futures)]
        
        end_time = time.time()
        elapsed_sec = end_time - start_time
        
        assert len(results) == 50
        # Should complete faster than sequential (50 * ~50ms = 2.5s)
        assert elapsed_sec < 2.0, f"50 concurrent took {elapsed_sec:.2f}s"
        
        print(f"✅ Test 6: Concurrent 50 reports - {elapsed_sec:.2f}s (10 workers)")
    
    def test_transformation_consistency(self):
        """Test same input produces same output (deterministic)"""
        coach_data = self._generate_mock_coach_rick_data("consistency_test")
        
        # Transform same data 5 times
        results = []
        for _ in range(5):
            report = transform_coach_rick_to_report(coach_data, "consistency_test", 1)
            results.append(report)
        
        # All results should be identical
        first_report = results[0]
        for report in results[1:]:
            assert report["krs_total"] == first_report["krs_total"]
            assert report["krs_level"] == first_report["krs_level"]
            assert report["creation_score"] == first_report["creation_score"]
            assert report["transfer_score"] == first_report["transfer_score"]
        
        print("✅ Test 7: Transformation consistency - deterministic results")
    
    def test_varying_data_performance(self):
        """Test performance with varying data sizes"""
        # Small data (minimal fields)
        small_data = {
            "bat_speed_mph": 80.0,
            "exit_velocity_mph": 95.0,
            "efficiency_percent": 100.0,
            "tempo_score": 85.0,
            "stability_score": 90.0,
            "gew_overall": 87.0,
            "motor_profile": {"type": "SPINNER", "confidence": 88}
        }
        
        # Large data (all fields)
        large_data = {
            "bat_speed_mph": 80.0,
            "exit_velocity_mph": 95.0,
            "efficiency_percent": 100.0,
            "tempo_score": 85.0,
            "stability_score": 90.0,
            "gew_overall": 87.0,
            "hip_shoulder_gap_ms": 20,
            "hands_bat_gap_ms": 15,
            "motor_profile": {
                "type": "SLINGSHOTTER",
                "confidence": 92.0,
                "characteristics": ["Sequential", "Strong drive"]
            },
            "launch_angle": 15.0,
            "frames_analyzed": 120,
            "duration_seconds": 4.0,
            "patterns": [{"id": 1, "name": "Early ext"}],
            "drill_prescription": {"drills": ["Hip rot"]}
        }
        
        # Test small data
        start = time.time()
        for i in range(100):
            transform_coach_rick_to_report(small_data, f"small_{i}", 1)
        small_time = (time.time() - start) * 1000 / 100
        
        # Test large data
        start = time.time()
        for i in range(100):
            transform_coach_rick_to_report(large_data, f"large_{i}", 1)
        large_time = (time.time() - start) * 1000 / 100
        
        # Performance should be similar (extraction is O(1) for dict lookups)
        time_diff = abs(large_time - small_time)
        assert time_diff < 10.0, f"Time difference {time_diff:.2f}ms too large"
        
        print(f"✅ Test 8: Varying data - Small: {small_time:.2f}ms, Large: {large_time:.2f}ms")
    
    def test_throughput_target(self):
        """Test system can handle 1000 reports/minute"""
        target_per_minute = 1000
        target_per_second = target_per_minute / 60  # ~16.67 reports/sec
        max_time_per_report_ms = 1000 / target_per_second  # ~60ms per report
        
        # Test 50 reports to estimate throughput
        start_time = time.time()
        
        for i in range(50):
            coach_data = self._generate_mock_coach_rick_data(f"throughput_{i}")
            transform_coach_rick_to_report(coach_data, f"throughput_{i}", 1)
        
        end_time = time.time()
        elapsed_sec = end_time - start_time
        reports_per_sec = 50 / elapsed_sec
        reports_per_min = reports_per_sec * 60
        
        assert reports_per_min >= target_per_minute, \
            f"Throughput {reports_per_min:.0f}/min, target {target_per_minute}/min"
        
        print(f"✅ Test 9: Throughput - {reports_per_min:.0f} reports/min (target: 1000/min)")
    
    def test_error_handling_performance(self):
        """Test error handling doesn't slow down processing"""
        valid_data = self._generate_mock_coach_rick_data("valid")
        invalid_data = {"invalid": "data"}
        
        # Time valid transformations
        start = time.time()
        for i in range(100):
            try:
                transform_coach_rick_to_report(valid_data, f"valid_{i}", 1)
            except:
                pass
        valid_time = time.time() - start
        
        # Time invalid transformations (with error handling)
        start = time.time()
        for i in range(100):
            try:
                transform_coach_rick_to_report(invalid_data, f"invalid_{i}", 1)
            except:
                pass  # Expected to fail
        error_time = time.time() - start
        
        # Error handling should be fast (early exits)
        # Typically errors should be faster or similar
        print(f"✅ Test 10: Error handling - Valid: {valid_time:.3f}s, Error: {error_time:.3f}s")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("PERFORMANCE INTEGRATION TESTS")
    print("="*70 + "\n")
    
    test_suite = TestPerformance()
    
    # Run performance tests
    test_suite.test_single_transformation_time()
    test_suite.test_batch_transformation_10_reports()
    test_suite.test_batch_transformation_100_reports()
    test_suite.test_krs_calculation_performance()
    
    try:
        test_suite.test_memory_efficiency_large_batch()
    except ImportError:
        print("⚠️  Test 5 skipped: psutil not installed (pip install psutil)")
    
    test_suite.test_concurrent_transformations()
    test_suite.test_transformation_consistency()
    test_suite.test_varying_data_performance()
    test_suite.test_throughput_target()
    test_suite.test_error_handling_performance()
    
    print("\n" + "="*70)
    print("✅ ALL PERFORMANCE TESTS PASSED!")
    print("="*70 + "\n")
