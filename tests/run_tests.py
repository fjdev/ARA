"""
Test Runner and Suite Configuration
====================================

Test suite runner with comprehensive coverage reporting and test discovery.
"""

import unittest
import sys
import os
import time

# Add parent directory to path to import ara
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ARATestResult(unittest.TextTestResult):
    """Custom test result class with enhanced reporting."""
    
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.test_start_time = None
        self.test_times = {}
        
    def startTest(self, test):
        super().startTest(test)
        self.test_start_time = time.time()
        
    def stopTest(self, test):
        super().stopTest(test)
        if self.test_start_time:
            elapsed_time = time.time() - self.test_start_time
            self.test_times[str(test)] = elapsed_time
            
    def getDescription(self, test):
        """Get enhanced test description."""
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return '\n'.join((str(test), doc_first_line))
        else:
            return str(test)


class ARATestRunner(unittest.TextTestRunner):
    """Custom test runner with enhanced reporting."""
    
    resultclass = ARATestResult
    
    def __init__(self, stream=None, descriptions=True, verbosity=2, **kwargs):
        super().__init__(stream, descriptions, verbosity, **kwargs)
        
    def _makeResult(self):
        return self.resultclass(self.stream, self.descriptions, self.verbosity)
        
    def run(self, test):
        """Run tests with enhanced reporting."""
        result = super().run(test)
        
        # Print timing information
        if hasattr(result, 'test_times') and result.test_times:
            self.stream.writeln("\n" + "="*70)
            self.stream.writeln("Test Execution Times:")
            self.stream.writeln("="*70)
            
            # Sort tests by execution time
            sorted_times = sorted(result.test_times.items(), key=lambda x: x[1], reverse=True)
            
            for test_name, elapsed_time in sorted_times[:10]:  # Top 10 slowest tests
                self.stream.writeln(f"{test_name}: {elapsed_time:.3f}s")
                
        return result


def load_test_suite():
    """Load the complete test suite."""
    # Get the directory containing test files
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Discover all test files
    loader = unittest.TestLoader()
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    return suite


def run_specific_test_module(module_name):
    """Run tests from a specific module."""
    try:
        module = __import__(f'test_{module_name}', fromlist=[''])
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(module)
        return suite
    except ImportError:
        print(f"Test module 'test_{module_name}' not found")
        return None


def run_specific_test_class(module_name, class_name):
    """Run tests from a specific test class."""
    try:
        module = __import__(f'test_{module_name}', fromlist=[''])
        test_class = getattr(module, class_name)
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(test_class)
        return suite
    except (ImportError, AttributeError) as e:
        print(f"Test class '{class_name}' in module 'test_{module_name}' not found: {e}")
        return None


def run_tests_with_coverage():
    """Run tests with coverage analysis if coverage.py is available."""
    try:
        import coverage
        
        # Start coverage
        cov = coverage.Coverage()
        cov.start()
        
        # Run tests
        suite = load_test_suite()
        runner = ARATestRunner()
        result = runner.run(suite)
        
        # Stop coverage and report
        cov.stop()
        cov.save()
        
        print("\n" + "="*70)
        print("Coverage Report:")
        print("="*70)
        cov.report(show_missing=True)
        
        # Generate HTML report if requested
        try:
            html_dir = os.path.join(os.path.dirname(__file__), 'coverage_html')
            cov.html_report(directory=html_dir)
            print(f"\nHTML coverage report generated in: {html_dir}")
        except Exception as e:
            print(f"Could not generate HTML report: {e}")
            
        return result
        
    except ImportError:
        print("Coverage.py not available. Running tests without coverage analysis.")
        return run_all_tests()


def run_all_tests():
    """Run all tests without coverage."""
    suite = load_test_suite()
    runner = ARATestRunner()
    return runner.run(suite)


def main():
    """Main test runner entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='ARA Test Suite Runner')
    parser.add_argument('--module', '-m', help='Run tests from specific module')
    parser.add_argument('--class', '-c', dest='test_class', help='Run tests from specific class')
    parser.add_argument('--coverage', action='store_true', help='Run with coverage analysis')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--pattern', '-p', default='test_*.py', help='Test file pattern')
    
    args = parser.parse_args()
    
    # Set verbosity
    verbosity = 2 if args.verbose else 1
    
    # Determine which tests to run
    if args.module and args.test_class:
        suite = run_specific_test_class(args.module, args.test_class)
    elif args.module:
        suite = run_specific_test_module(args.module)
    else:
        if args.coverage:
            result = run_tests_with_coverage()
            sys.exit(0 if result.wasSuccessful() else 1)
        else:
            suite = load_test_suite()
    
    if suite is None:
        sys.exit(1)
        
    # Run the selected tests
    runner = ARATestRunner(verbosity=verbosity)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("Test Summary:")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print(f"\nFailed tests:")
        for test, traceback in result.failures:
            print(f"  - {test}")
            
    if result.errors:
        print(f"\nError tests:")
        for test, traceback in result.errors:
            print(f"  - {test}")
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    main()
