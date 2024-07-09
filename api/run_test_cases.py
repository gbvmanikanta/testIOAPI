import io
import unittest
from flask_restx import Resource
from swagger.swagger import run_test_cases_ns
import importlib
import os
import sys
import tempfile
@run_test_cases_ns.route('/<string:test_filename>/<string:test_function>')
class RunTests(Resource):
    @run_test_cases_ns.response(200, 'Success')
    @run_test_cases_ns.response(400, 'Validation Error')
    def get(self, test_filename, test_function):
        # Run the specified test function within the test file
        test_output, analysis = run_specific_test_function(test_filename, test_function)
        return {'test_output': test_output, 'analysis': analysis}, 200


def run_specific_test_function(test_filename, test_function):
    try:
        # Set the correct working directory and add the necessary paths to PYTHONPATH
        test_dir = os.path.dirname(test_filename)
        project_root = os.path.abspath(os.path.join(test_dir, os.pardir, os.pardir))
        sys.path.insert(0, project_root)

        # Dynamically load the test module
        spec = importlib.util.spec_from_file_location("test_module", test_filename)
        test_module = importlib.util.module_from_spec(spec)
        print(test_module)
        spec.loader.exec_module(test_module)

        # Capture the test output
        stream = io.StringIO()
        runner = unittest.TextTestRunner(stream=stream)

        # Create a test suite for the specified test function
        suite = unittest.TestSuite()
        print(suite)
        for name, obj in vars(test_module).items():
            print("Name : ", name)

            if isinstance(obj, type) and issubclass(obj, unittest.TestCase):
                print("Obj : ", obj(test_function))
                suite.addTest(obj(test_function))

        print("Suite : ",suite)
        result = runner.run(suite)

        # Analyze the results
        test_output = stream.getvalue()
        analysis = analyze_results(test_output)

        return test_output, analysis
    except Exception as e:
        return str(e), 'Failed to run tests.'


def analyze_results(test_output):
    # Analyze the test output to provide recommendations
    if 'FAIL' in test_output or 'ERROR' in test_output:
        return 'There are test failures. Please check the test cases and the code.'
    else:
        return 'All tests passed successfully.'