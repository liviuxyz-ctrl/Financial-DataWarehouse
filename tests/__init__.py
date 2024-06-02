# run_tests.py
import unittest

# Specify the test files
test_files = [
    'tests/test_data_processor.py',
    'tests/test_database.py',
    'tests/test_models.py',
    'tests/test_nasdaq_api_client.py',
]

# Load tests from the specified test files
loader = unittest.TestLoader()
suites_list = []
for test_file in test_files:
    suites_list.append(loader.discover(start_dir='.', pattern=test_file))

# Combine all the test suites into a single test suite
combined_suite = unittest.TestSuite(suites_list)

# Run the combined test suite
runner = unittest.TextTestRunner()
result = runner.run(combined_suite)

# Exit with the appropriate code
if not result.wasSuccessful():
    exit(1)
else:
    exit(0)
