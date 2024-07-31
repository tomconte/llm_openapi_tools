"""Converts an OpenAPI spec to a APIPlugin spec."""

from openapi_spec_validator import validate


def convert_spec(openapi_spec: dict, plugin_config: dict) -> dict:
    """Converts an OpenAPI spec to a AI-Enabled OpenAPI spec."""
    # Make sure the spec is valid
    validate(openapi_spec)

    # Include plans in the new spec
    plans = plugin_config.get("plans", [])

    # Create a new OpenAPI spec based on the original
    new_spec = {
        "openapi": openapi_spec["openapi"],
        "info": openapi_spec["info"],
        "x-llm-plans": plans,
        "servers": openapi_spec["servers"] if "servers" in openapi_spec else [],
        "paths": {},
        "components": openapi_spec["components"] if "components" in openapi_spec else {},
        "security": openapi_spec["security"] if "security" in openapi_spec else [],
        "tags": openapi_spec["tags"] if "tags" in openapi_spec else [],
    }

    # TODO: remove/reduce docs?

    # Override the properties we want to change
    new_spec["info"]["title"] = plugin_config["info"]["title"]
    new_spec["info"]["description"] = plugin_config["info"]["description"]

    # For each operation in the configuration, add it to the new spec
    for op in plugin_config["operations"]:
        path = op["path"]
        method = op["method"]
        description = op.get("description", "")

        if path in openapi_spec["paths"] and method in openapi_spec["paths"][path]:
            operation = openapi_spec["paths"][path][method]
            operation["description"] = description
            # TODO: rewrite parameters descriptions
            if path not in new_spec["paths"]:
                new_spec["paths"][path] = {}
            new_spec["paths"][path][method] = operation

    # Validate the new spec
    validate(new_spec)

    return new_spec
