from flask_restx import Resource
from services.openai_services import OpenAIService
from swagger.swagger import code_quality_ns, code_quality_model
from flask import request
import os
from utils.utils import read_file
rootpath =r"C:\Workspace\AI_Workspace\Project"

@code_quality_ns.route('/')
class CodeQuality(Resource):
    @code_quality_ns.expect(code_quality_model)
    @code_quality_ns.marshal_with(code_quality_model, code=201)
    def post(self):
        path = request.args.get('path')
        local_path = os.path.join(rootpath, path)
        code = read_file(local_path)
        service = OpenAIService()
        quality_report = service.assess_code_quality(code)
        return {'code': quality_report}, 201
