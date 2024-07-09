from flask_restx import Namespace, fields
vulnerability_ns = Namespace('check-vulnerability', description='API to check the vulnerability of the code')

analysis_model = vulnerability_ns.model('AnalysisModel', {
    'num_test_cases': fields.String(required=True, description='Number of test cases'),
    'base_java_url': fields.String(required=True, description='Base URL for Java files'),
    'base_xml_url': fields.String(required=True, description='Base URL for XML files')
})

approve_model = vulnerability_ns.model("ApproveModel",{
    'path': fields.String(required=True, description='Number of test cases'),
    'content': fields.String(required=True, description='Base URL for Java files'),
})

metadata_ns =  Namespace("generate-metadata", description="API to generate the testcase metadata to the code")
meatdata_model = metadata_ns.model('MetadataModel',{
    'projectFolder': fields.String(required=True, description='Upload project folder')
})

test_cases = Namespace('generate_test_cases', description='Generate test cases for given code')

test_case_model = test_cases.model('TestCase', {
    'code': fields.String(required=True, description='Code to generate test cases for')
})

code_quality_ns = Namespace('code_quality', description='Assess code quality')

code_quality_model = code_quality_ns.model('CodeQuality', {
    'code': fields.String(required=True, description='Code to assess quality for')
})

analyze_test_case = Namespace('analyze_test_cases', description='Analyze and provide suggestions for test cases')

analyze_test_case_model = analyze_test_case.model('AnalyzeTestCase', {
    'test_cases': fields.String(required=True, description='Test cases to analyze')
})

test_case_ns = Namespace('generate_tests', description='Generate unit test cases for given code')

upload_model = test_case_ns.model('UploadModel', {
    'file': fields.String(required=True, description='Zip file containing project(s)')
})

run_test_cases_ns = Namespace('run_tests', description='Generate unit test cases for given code')

code_model = test_cases.model('CodeModel', {
    'code': fields.String(required=True, description='The code to analyze'),
    'language': fields.String(required=True, description='Programming language of the code')
})
