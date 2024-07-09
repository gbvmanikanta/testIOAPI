from swagger.swagger import metadata_ns, meatdata_model
from utils.llm_configuration import llm
from flask import Flask, request, jsonify, make_response
import os
from flask_restx import Resource
from langchain.schema import HumanMessage, SystemMessage
import zipfile
import tempfile

function_descriptions = [
    {
        "name": "generate_metadata",
        "description": "Generate metadata for a given code file",
        "parameters": {
            "type": "object",
            "properties": {
                "benchmark-version": {
                    "type": "string",
                    "description": "The benchmark version of the test"
                },
                "category": {
                    "type": "string",
                    "description": "The category of the test"
                },
                "test-number": {
                    "type": "string",
                    "description": "The test number"
                },
                "vulnerability": {
                    "type": "string",
                    "description": "Indicates whether the code is vulnerable ('true' or 'false')"
                },
                "cwe": {
                    "type": "string",
                    "description": "The Common Weakness Enumeration (CWE) identifier"
                }
            },
            "required": ["benchmark-version", "category", "test-number", "vulnerability", "cwe"]
        },
    }
]

final_dir = r"C:\Workspace\AI_Workspace"

def extract_zip(file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(output_dir)
    return output_dir

# def generate_metadata(code):
#     response = llm.predict_messages([HumanMessage(content=code)],
#                                           functions=function_descriptions)
#     llm.
#     # prompt = f"Generate metadata for the following code:\n\n{code}\n\nMetadata format:\n<test-metadata>\n    <benchmark-version>1.2</benchmark-version>\n    <category>[category]</category>\n    <test-number>[test-number]</test-number>\n    <vulnerability>[true/false]</vulnerability>\n    <cwe>[cwe]</cwe>\n</test-metadata>\n\nMetadata:"
#     # response = openai.Completion.create(
#     #     engine="text-davinci-003",
#     #     prompt=prompt,
#     #     max_tokens=150,
#     #     temperature=0.5
#     # )
#     print(response)
#     metadata = response.choices[0].text.strip()
#     return metadata

def generate_metadata(code):
    # print(code)
    # chat = ChatOpenAI(model_name="gpt-4")  # or "gpt-3.5-turbo" based on availability and requirements

    # System message to instruct the model about the task
    system_message = SystemMessage(
        content="You are an assistant that generates metadata in XML format for given code snippets. The metadata should include <benchmark-version>, <category>, <test-number>, <vulnerability>, and <cwe>. The <vulnerability> tag should be set to true if the code has any vulnerabilities.")

    # Human message with the code
    human_message = HumanMessage(content=f"Generate metadata in XML format for the following code:\n\n{code}")

    # Generate the metadata
    response = llm([system_message, human_message])
    # print(response)
    return response.content.strip("```xml\n").strip("```").strip()

def save_metadata_to_file(metadata, file_name, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file_path = os.path.join(output_dir, f"{file_name}.xml")
    print("Path ****",output_file_path)
    with open(output_file_path, 'w') as f:
        f.write(metadata)

@metadata_ns.route('')
class GenerateMetadata(Resource):
    @metadata_ns.expect(meatdata_model)
    def post(self):
        if 'projectFolder' not in request.files:
            return jsonify({"error": "No folder part in the request"}), 400

        project_folder = request.files['projectFolder']

        folder = os.path.splitext(project_folder.filename)[0]

        output_dir= os.path.join(final_dir,'Project', folder)

        folder_path = extract_zip(project_folder, output_dir)
        metadata_list = []

        for root, dirs, files in os.walk(folder_path):
            # print("Root:  ",root)
            # # print(type(root))
            #
            # print(root)
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith('.py') or file.endswith('.java'):
                    with open(file_path, 'r') as f:
                        code = f.read()
                        metadata = generate_metadata(code)
                        file_base_name = os.path.splitext(file)[0]
                        test_case_dir = os.path.join(root.replace("Project", "Project\\Testcases"))
                        save_metadata_to_file(metadata, file_base_name, test_case_dir)
                        metadata_list.append({
                            "file_name": file,
                            "metadata": metadata
                        })
        project_folder = ""
        return make_response({'data': metadata_list, 'message': 'Testcase metadata successfully created.', 'status': 200},
                    200)
        # return jsonify(metadata_list)

