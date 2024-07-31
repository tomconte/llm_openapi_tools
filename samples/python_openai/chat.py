"""Sample chatbot using OpenAPI spec.

All this code is based on this cookbook sample:
https://cookbook.openai.com/examples/function_calling_with_an_openapi_spec
"""

import json
import os
from pprint import pprint as pp

import jsonref
import requests
import yaml
from dotenv import load_dotenv
from openai import AzureOpenAI

from llm_openapi_tools.openapi import convert_spec
from llm_openapi_tools.tools import (generate_tools_pseudocode,
                                     pretty_print_tools)

load_dotenv()

SYSTEM_MESSAGE = """
You are a helpful assistant.
Respond to the following prompt by using function calls and then summarize actions.
Ask for clarification if a user request is ambiguous.
"""

USER_INSTRUCTION = """
Find a friendly available savanna pet and display its full details
"""

# Maximum number of function calls allowed to prevent infinite or lengthy loops
MAX_CALLS = 5

# Initialize the OpenAI client
client = AzureOpenAI()


def openapi_to_functions(openapi_spec):
    """Converts an OpenAPI spec to a list of functions."""
    functions = []

    for path, methods in openapi_spec["paths"].items():
        for method, spec_with_ref in methods.items():
            # 1. Resolve JSON references.
            spec = jsonref.replace_refs(spec_with_ref)

            # 2. Extract a name for the functions.
            function_name = spec.get("operationId")

            # 3. Extract a description and parameters.
            desc = spec.get("description") or spec.get("summary", "")

            schema = {"type": "object", "properties": {}}

            req_body = (
                spec.get("requestBody", {})
                .get("content", {})
                .get("application/json", {})
                .get("schema")
            )
            if req_body:
                schema["properties"]["requestBody"] = req_body

            params = spec.get("parameters", [])
            if params:
                param_properties = {
                    param["name"]: param["schema"]
                    for param in params
                    if "schema" in param
                }
                schema = {
                    "type": "object",
                    "properties": param_properties,
                }

            functions.append(
                {"type": "function", "function": {"name": function_name,
                                                  "description": desc, "parameters": schema}}
            )

    return functions


def get_openai_response(functions, messages):
    chat_completion = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        tools=functions,
        # "auto" means the model can pick between generating a message or calling a function.
        tool_choice="auto",
        temperature=0,
        messages=messages,
    )

    # Print all token usage statistics
    pp(chat_completion.usage)

    return chat_completion


def process_user_instruction(functions, instruction):
    num_calls = 0
    messages = [
        {"content": SYSTEM_MESSAGE, "role": "system"},
        {"content": instruction, "role": "user"},
    ]

    while num_calls < MAX_CALLS:
        response = get_openai_response(functions, messages)
        message = response.choices[0].message

        print(message)
        print(message.content)

        print(f"Finished: {response.choices[0].finish_reason}")
        if response.choices[0].finish_reason == "stop":
            break

        try:
            print(f"\n>> Function call #: {num_calls + 1}\n")
            pp(message.tool_calls)
            messages.append(message)

            # For the sake of this example, we'll simply add a message to simulate success.
            # Normally, you'd want to call the function here, and append the results to messages.
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    # Insert responses
                    if tool_call.function.name == "findPetsByStatus":
                        # Send query to local petstore server
                        tool_params = json.loads(tool_call.function.arguments)
                        tool_response = requests.get(
                            f"http://localhost:8080/api/v3/pet/findByStatus?status={tool_params.get('status')}").json()
                        messages.append(
                            {
                                "role": "tool",
                                "content": json.dumps(tool_response),
                                "tool_call_id": tool_call.id,
                            }
                        )
                    else:
                        messages.append(
                            {
                                "role": "tool",
                                "content": "success",
                                "tool_call_id": tool_call.id,
                            }
                        )

            num_calls += 1
        except Exception as exc:
            print(f"Error: {exc}")
            break

    if num_calls >= MAX_CALLS:
        print(f"Reached max chained function calls: {MAX_CALLS}")


def main():
    # Base OpenAPI spec
    with open('tests/__fixtures__/openapi_specs/petstore-v3-openapi.json', 'r') as f:
        base_openapi_spec = jsonref.loads(f.read())

    # GenAI plugin config
    with open('tests/__fixtures__/manifests/petstore-v3.yaml', 'r') as f:
        plugin_config = yaml.safe_load(f)

    # Convert the base OpenAPI spec to a list of functions
    base_functions = openapi_to_functions(base_openapi_spec)

    print("\n\n### Testing base functions:")
    pp(base_functions)
    print(f"\n\n### Number of functions in base API: {len(base_functions)}")

    process_user_instruction(base_functions, USER_INSTRUCTION)

    ################################################################################
    # Here the AI Plugin Registry library is used to convert the original OpenAPI
    # spec to a GenAI OpenAPI spec

    # Convert the OpenAPI spec to a GenAI OpenAPI spec
    genai_openapi_spec = convert_spec(base_openapi_spec, plugin_config)

    # The generated GenAI OpenAPI spec is used to create a list of functions
    ################################################################################

    # Convert the GenAI OpenAPI spec to a list of functions
    genai_functions = openapi_to_functions(genai_openapi_spec)

    print("\n\n### Testing GenAI functions:")
    pretty_print_tools(genai_functions)
    print(f"\n\n### Number of functions in GenAI API: {len(genai_functions)}")

    # Add the plans to the user instructions
    plans = genai_openapi_spec.get("x-llm-plans", [])
    user_instruction = "Possible execution plans:\n"
    for p in plans:
        user_instruction += f"\n{p['intent']}:\n{p['plan']}\n"
    user_instruction += "\nUser instructions:\n"
    user_instruction += USER_INSTRUCTION

    process_user_instruction(genai_functions, user_instruction)


if __name__ == "__main__":
    main()
