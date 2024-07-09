from flask_restx import Namespace, Resource, fields
from services.openai_services import OpenAIService
from swagger.swagger import analyze_test_case, analyze_test_case_model


@analyze_test_case.route('/')
class AnalyzeTestCases(Resource):
    @analyze_test_case.expect(analyze_test_case_model)
    @analyze_test_case.marshal_with(analyze_test_case_model, code=201)
    def post(self):
        data = analyze_test_case.payload
        test_cases = data['test_cases']
        service = OpenAIService()
        analysis_report = service.analyze_test_cases(test_cases)
        return {'test_cases': analysis_report}, 201
