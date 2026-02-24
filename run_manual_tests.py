import unittest
import sys
import os

print("Starting test run...")

# Ensure src modules are importable
sys.path.append(os.getcwd())

try:
    from test.test_fs_tools import TestFSTools

    suite = unittest.TestLoader().loadTestsFromTestCase(TestFSTools)
    unittest.TextTestRunner(verbosity=2).run(suite)
except Exception as e:
    print(f"Error running tests: {e}")
