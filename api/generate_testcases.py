from flask_restx import Namespace, Resource, fields
from services.openai_services import OpenAIService
from flask import request
from swagger.swagger import test_cases, test_case_model
import os
from utils.utils import read_file

rootpath =r"C:\Workspace\AI_Workspace\Project"
@test_cases.route('/')
class GenerateTestCases(Resource):
    @test_cases.expect(test_case_model)
    # @test_cases.marshal_with(test_case_model, code=201)
    def post(self):
        path = request.args.get('path')
        local_path = os.path.join(rootpath, path)
        code = read_file(local_path)
        # data = request.json
        # code = data['code']
        service = OpenAIService()
        test_cases = service.generate_test_cases(code)
        print(test_cases)
        # return test_cases
        return {'code': test_cases}, 201
