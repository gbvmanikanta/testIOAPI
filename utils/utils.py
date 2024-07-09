import json
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from langchain.schema import HumanMessage
import io
from utils.function_descriptions import function_descriptions
from utils.llm_configuration import llm
from lxml import etree
import mimetypes
import xml.etree.ElementTree as ET


def split_code_into_chunks(code, chunk_size=500):
    lines = code.split('\n')
    for i in range(0, len(lines), chunk_size):
        yield '\n'.join(lines[i:i + chunk_size])

# Function to do the analysis
def static_analysis_tool(code_chunk):
    messages = [HumanMessage(
        content=f"Analyze the following code for all possible security vulnerabilities and provide detailed information including the type of vulnerability, vulnerable code, suggested fix, and comments. Code:\n\n{code_chunk}")]
    try:
        response = llm.invoke(messages, functions=function_descriptions)
        print(response)
        analysis_result = response.messages[0].additional_kwargs['function_call']['arguments']
        return json.loads(analysis_result)
    except Exception as e:
        print(f"Error analyzing chunk: {e}")
        return {'vulnerability found': 'No', 'vulnerabilities': []}

# Function to fetch web content
def fetch_webpage_content(url):
    response = requests.get(url)
    return response.text

# Function to fetch and parse xml
def fetch_and_parse_xml(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def compare_results(analysis_result, metadata):
    # print(metadata)
    # print("TYPE : ", type(metadata))
    vuln_found = analysis_result['vulnerability found'].lower() == 'yes'
    root = ET.fromstring(metadata)
    category = root.find('category').text.lower()
    vuln_matches = fuzz.partial_ratio(category, analysis_result['vulnerability'].lower()) > 80
    metadata_vuln_exists = root.find('vulnerability').text.lower() == 'true'
    actual_vuln_type = analysis_result['vulnerability']
    expected_vuln_type = category

    combined_result = {
        'vulnerability_found': vuln_found,
        'vulnerability_type_matches': vuln_matches,
        'metadata_vulnerability_exists': metadata_vuln_exists,
        'expected_vuln_type': expected_vuln_type
    }

    combined_result.update(analysis_result)

    return combined_result

def compare_results(analysis_result, metadata):
    print(metadata)
    vuln_found = analysis_result['vulnerability found'].lower() == 'yes'
    root = ET.fromstring(metadata)
    category = root.find('category').text.lower()
    metadata_vuln_exists = root.find('vulnerability').text.lower() == 'true'
    vulnerabilities = analysis_result['vulnerabilities']

    combined_results = []

    for vulnerability in vulnerabilities:
        vuln_matches = fuzz.partial_ratio(metadata.category.string.lower(), vulnerability['vulnerability'].lower()) > 80
        actual_vuln_type = vulnerability['vulnerability']
        expected_vuln_type = metadata.category.string

        result = {
            'vulnerability_found': vuln_found,
            'vulnerability_type_matches': vuln_matches,
            'metadata_vulnerability_exists': metadata_vuln_exists,
            'expected_vuln_type': expected_vuln_type
        }
        result.update(vulnerability)
        combined_results.append(result)

    return combined_results

def construct_url(base_url, test_case_number, file_extension):
    return f"{base_url}{test_case_number}.{file_extension}"

def run_test_case(test_case_number, base_java_url, base_xml_url):
    java_url = construct_url(base_java_url, test_case_number, "java")
    xml_url = construct_url(base_xml_url, test_case_number, "xml")

    # code = fetch_webpage_content(java_url)
    # metadata = fetch_and_parse_xml(xml_url)
    code = read_file(base_java_url)
    print(code)
    metadata = read_file(base_xml_url)
    return code
    # all_vulnerabilities = []
    # for chunk in split_code_into_chunks(code):
    #     analysis_result = static_analysis_tool(chunk)
    #     all_vulnerabilities.extend(analysis_result['vulnerabilities'])
    #
    # analysis_result = {
    #     'vulnerability found': 'Yes' if all_vulnerabilities else 'No',
    #     'vulnerabilities': all_vulnerabilities
    # }
    #
    # # analysis_result_json = static_analysis_tool(code)
    # # analysis_result = json.loads(analysis_result_json)
    # # print(analysis_result)
    # result = compare_results(analysis_result, metadata)
    # print(result)
    # result['code'] = code
    # return result


def read_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    try:
        if mime_type and mime_type.startswith('text'):
            # Read as text file
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return content
        else:
            # Read as binary file
            with open(file_path, 'rb') as file:
                content = file.read()
                return content
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
    return None

