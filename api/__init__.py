from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from .vulnerability_check import vuln
from .generate_testcase_metadata import metadata_ns as metadata
from .generate_testcases import test_cases
from .code_quality import code_quality_ns
from .analyze_test_cases import analyze_test_case
from .generate_unit_tests import test_case_ns
from .run_test_cases import run_test_cases_ns
# import config



def create_app():
    app = Flask(__name__)
    with app.app_context():
        print("Test1")
        # app.config.from_object(config)
        # app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
        # db.init_app(app)
        CORS(app, origins='*')

        # migrate = Migrate(app, db)
        api = Api(app, version='1.0', title='Test Case generator', description='bucket list API', doc='/swagger/')
        api.add_namespace(vuln)
        api.add_namespace(metadata)
        api.add_namespace(test_cases)
        api.add_namespace(code_quality_ns)
        api.add_namespace(analyze_test_case)
        api.add_namespace(test_case_ns)
        api.add_namespace(run_test_cases_ns)

        return app

app = create_app()