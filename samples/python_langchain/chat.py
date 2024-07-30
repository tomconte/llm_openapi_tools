import os
from pprint import pprint as pp

import jsonref
import yaml
from dotenv import load_dotenv
from langchain_community.agent_toolkits.openapi import planner
from langchain_community.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain_community.utilities import RequestsWrapper
from langchain_openai import AzureChatOpenAI

from llm_openapi_tools.openapi import convert_spec

load_dotenv()

USER_INSTRUCTION = """
Find a friendly available savanna pet and display its full details
"""


def main():
    # Base OpenAPI spec
    with open('tests/__fixtures__/openapi_specs/petstore-v3-openapi.json', 'r') as f:
        base_openapi_spec = jsonref.loads(f.read())
    reduced_base_openapi_spec = reduce_openapi_spec(base_openapi_spec)

    # GenAI plugin config
    with open('tests/__fixtures__/manifests/petstore-v3.yaml', 'r') as f:
        plugin_config = yaml.safe_load(f)

    requests_wrapper = RequestsWrapper()

    llm = AzureChatOpenAI(model_name=os.getenv(
        "AZURE_OPENAI_DEPLOYMENT_NAME"), temperature=0.0)

    # Test using the base OpenAPI spec
    print("### Testing base functions:")

    base_agent = planner.create_openapi_agent(
        reduced_base_openapi_spec,
        requests_wrapper,
        llm,
        allow_dangerous_requests=True,
        handle_parsing_errors=True,
    )

    pp(base_agent.tools)

    try:
        base_agent.invoke(USER_INSTRUCTION)
    except Exception as exc:
        print(f"Error: {exc}")

    # Same test using the plugin registry
    print("\n\n### Testing GenAI functions:")

    # Convert the OpenAPI spec to a GenAI OpenAPI spec
    genai_openapi_spec = convert_spec(base_openapi_spec, plugin_config)
    reduced_genai_openapi_spec = reduce_openapi_spec(genai_openapi_spec)

    genai_agent = planner.create_openapi_agent(
        reduced_genai_openapi_spec,
        requests_wrapper,
        llm,
        allow_dangerous_requests=True,
        handle_parsing_errors=True,
    )

    pp(genai_agent.tools)

    try:
        genai_agent.invoke(USER_INSTRUCTION)
    except Exception as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
