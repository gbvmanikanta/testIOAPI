from flask import Flask, request, jsonify, send_file
from flask_restx import Api, Resource, fields
import openai  # Assuming OpenAI's GPT-4
import io
import sys
import unittest
import zipfile
import os
import tempfile
import shutil
from swagger.swagger import test_case_ns, code_model
from config import rootpath
import json
from services.openai_services import OpenAIService
@test_case_ns.route('')
class GenerateTests(Resource):
    @test_case_ns.expect(code_model)
    @test_case_ns.response(200, 'Success')
    @test_case_ns.response(400, 'Validation Error')
    def post(self):
        data = request.json
        code = data.get('code')
        language = data.get('language')
        if not code or not language:
            return {'message': 'Code and language are required'}, 400

        # Generate test cases and detailed response using GPT-4
        response_data = OpenAIService.generate_unit_tests_with_langchain(code, language)
        print("Response Data:", response_data)
        # return json.dumps(response_data, indent=4), 200
        return response_data, 200


def generate_unit_tests_for_directory(directory):
    test_dir = os.path.join(directory, 'Test')
    os.makedirs(test_dir, exist_ok=True)
    print("***********")
    print("Test directory at first: ", test_dir)
    # Define a mapping of file extensions to languages and test file extensions
    language_mapping = {
        '.py': ('python', 'py'),
        '.js': ('javascript', 'js'),
        '.java': ('java', 'java'),
    }

    for root, _, files in os.walk(directory):
        for file in files:
            print("Root Path: ", root)
            if 'Test' in root:
                continue
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1]

            if file_extension in language_mapping:
                language, test_extension = language_mapping[file_extension]
                print("*************")
                print("filePath: ", file_path)
                # test_cases = OpenAIService.generate_unit_tests_with_langchain(file_path, language)
                test_cases = replace_module_name(test_cases, file_path)
                save_test_cases(test_cases, test_dir, root, file, test_extension)


# def generate_unit_tests_with_gpt4(file_path, language):
#     with open(file_path, 'r') as f:
#         code = f.read()
#
#     prompt = f"""
#     You are an expert in {language}. Write unit tests for the following {language} code using the appropriate testing framework:
#
#     {code}
#
#     The unit tests should cover various edge cases, typical cases, and should include both positive and negative test cases.
#     """
#
#     response = openai.Completion.create(
#         engine="text-davinci-003",  # Use the appropriate engine for your model
#         prompt=prompt,
#         max_tokens=1000
#     )
#
#     return response.choices[0].text.strip()


def replace_module_name(test_cases, file_path):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    print("Module Name: ", module_name)
    return test_cases.replace('your_module', module_name)

def save_test_cases(test_cases, test_dir, root, file, extension):
    print("********")
    print(f"Executing from save_test_cases: {test_dir} ---- {root} ----- ")
    relative_path = os.path.relpath(root, os.path.dirname(test_dir))
    print("********")
    print("Relative Path: ", relative_path)
    test_subdir = os.path.join(test_dir, relative_path)
    os.makedirs(test_subdir, exist_ok=True)
    print("******")
    print(test_subdir)
    test_filename = f'test_{os.path.splitext(file)[0]}.{extension}'
    test_file_path = os.path.join(test_subdir, test_filename)
    print("Test File Path: ",test_file_path)
    with open(test_file_path, 'w') as f:
        f.write(test_cases)
