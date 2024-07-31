"""Helper functions for the OpenAPI tools.

The tools array has the following shape:

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        }
    ]

"""


def pretty_print_tools(tools):
    """Pretty print the tools array."""
    for tool in tools:
        if tool["type"] == "function":
            function = tool["function"]
            print(f"Function: {function['name']}")
            print(f"Description: {function['description']}")
            print("Parameters:")
            for param_name, param_schema in function["parameters"]["properties"].items():
                print(f"  {param_name} ({param_schema.get('type')}): {param_schema.get('description', '')}")
            print()


def generate_tools_pseudocode(tools):
    """Generate pseudocode for the tools array."""
    pseudocode = []
    for tool in tools:
        if tool["type"] == "function":
            function = tool["function"]
            args = ", ".join(function["parameters"]["properties"].keys())
            pseudocode.append(f"{function['name']}({args})")
    return pseudocode
