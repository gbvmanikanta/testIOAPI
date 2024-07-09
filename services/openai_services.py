import openai
from langchain import ConversationChain
from langchain.schema import SystemMessage, HumanMessage
from utils.llm_configuration import llm
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
import json
class OpenAIService:
    # def __init__(self):
    #     self.api_key = current_app.config['OPENAI_API_KEY']
    #     openai.api_key = self.api_key

    def generate_test_cases(self, code):
        # conversation = ConversationChain()

        system_message = SystemMessage(
            content="You are an AI assistant specialized in generating comprehensive and detailed test cases for Python functions.")
        human_message = HumanMessage(content=f"""
        Generate comprehensive and detailed test cases for the following Python function. Include test cases for typical inputs, edge cases, invalid inputs, and boundary conditions. Provide explanations for each test case.

        Function:
        {code}

        Test cases:
        """)

        # conversation.add_message(system_message)
        # conversation.add_message(human_message)
        response = llm([system_message, human_message])
        # response = conversation.run()
        print(response)
        return response.content
        # result = response.messages[0].additional_kwargs['function_call']['arguments']
        # return json.loads(result)
        # return response.strip()

    def assess_code_quality(self, code):
        # conversation = ConversationChain()

        system_message = SystemMessage(content="You are an AI assistant specialized in assessing code quality.")
        human_message = HumanMessage(
            content=f"Assess the quality of the following code and provide suggestions for improvement:\n\n{code}")

        # conversation.add_message(system_message)
        # conversation.add_message(human_message)
        #
        # response = conversation.run()
        response = llm([system_message, human_message])
        print(response)
        return response.content

    def check_compliance(self, code, standards):
        conversation = ConversationChain()

        system_message = SystemMessage(
            content="You are an AI assistant specialized in checking code compliance with coding standards.")
        human_message = HumanMessage(
            content=f"Check the following code for compliance with the following standards:\n\nCode:\n{code}\n\nStandards:\n{standards}")

        # conversation.add_message(system_message)
        # conversation.add_message(human_message)
        #
        # response = conversation.run()
        response = llm([system_message, human_message])
        return response.strip()

    def analyze_test_cases(self, test_cases):
        # conversation = ConversationChain()

        system_message = SystemMessage(
            content="You are an AI assistant specialized in analyzing test cases and providing suggestions for improvement.")
        human_message = HumanMessage(content=f"""
        Analyze the following test cases and provide suggestions for improving their coverage and effectiveness. Identify any missing edge cases and recommend best practices.

        Test Cases:
        {test_cases}

        Analysis and Suggestions:
        """)

        response = llm([system_message, human_message])
        print(response)
        return response.content

    def generate_unit_tests_with_langchain(code, language):
        try:
            print("LLM:*******", llm)

            # Define the system message for the assistant
            system_message = SystemMessage("You are a helpful assistant.")
            human_message = HumanMessage(f"""
            You are an expert in {language}. Generate comprehensive test cases for the following {language} code and provide detailed explanations:

            {code}

            The response should include:
            - A list of all possible behavior coverages for the code.
            - Generate comprehensive and detailed test cases for the following {language} function. Include test cases for all mentioned behavior coverages as actual code.
            - Summary of the code.
            - Example usage of the code.
            - Detailed code analysis including:
              - Inputs and their explanations.
              - Complete flow of the code.
              - Output explanation.

            Respond in the following JSON format:
            {{
                "test_suite": {{
                    "behavior_coverage": ["list of behavior coverages"],
                    "tests": "generated test cases as code"
                }},
                "code_explanation": {{
                    "summary": "Summary of the code",
                    "sample_usage": "Example usage of the code",
                    "code_analysis": {{
                        "inputs": ["list of inputs and explanations"],
                        "flow": "Complete flow of the code",
                        "outputs": "Output explanation"
                    }}
                }}
            }}
            """)

            # Get the response from the LLM
            response = llm([system_message, human_message])

            # Print the response for debugging purposes
            print(response.content)

            # Ensure the response content is properly formatted as JSON
            response_content = response.content.strip()

            # Attempt to parse the response as JSON
            data = json.loads(response_content)

            return data

        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print("Response content was:")
            print(response_content)
            return response_content
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
