function_descriptions = [
    {
        "name": "find_security_issues_and_generate_fix",
        "description": "Scan the code and find any security vulnerabilities and generate code fix",
        "parameters": {
            "type": "object",
            "properties": {
                "vulnerability found": {
                    "type": "string",
                    "description": " 'Yes' if there is a security vulnerability in code or 'No' if the code doesn't have security vulnerability",
                },
                "vulnerabilities": {
                    "type": "array",
                    "description": "list down all types of vulnerabilities",
                    "items": {
                        "type": "object",
                        "properties": {
                            "vulnerability": {
                                "type": "string",
                                "description": "The type of vulnerability found in the code or 'None'"
                            },
                            "vulnerable code": {
                                "type": "string",
                                "description": "The code that is vulnerable to the security issue or 'None'"
                            },
                            "code fix": {
                                "type": "string",
                                "description": "Code fix for the vulnerable code or 'None'"
                            },
                            "comment": {
                                "type": "string",
                                "description": "Comment that describes the issue and fix or 'No issues found'"
                            }
                        },
                        "required": ["vulnerability", "vulnerable code", "code fix", "comment"]
                    }
                }
            },
            "required": ["vulnerability found", "vulnerabilities"],
        },
    }
]