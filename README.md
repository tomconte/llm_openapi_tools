# LLM Function Tools

This project is a collection of tools to work with Function Calling in Large Language Models (LLMs) such as OpenAI's GPT.

## Enriching OpenAPI specs for LLMs

The `llm_functools.openapi` module provides tools to enrich and specialize OpenAPI specs with additional information that can be used by LLMs to generate more accurate function calls. It uses a manifest file to configure the specialization process. 

We call the resulting enriched OpenAPI spec an "LLM-friendly" spec. These specs can be thought of as a "plugin" for the LLM, providing additional information that can be used to generate function calls.

To convert an OpenAPI spec to an LLM-friendly spec from the command line, use the `llm_functools.convert` module:

```bash
python -m llm_functools.convert openapi.json manifest.json output.json
```

The following example specs and manifest are provided in the `tests/__fixtures__` directory:

- `openapi_specs/petstore-v3-openapi.json`: A sample OpenAPI spec for the Petstore API.
- `manifests/petstore-v3.yaml`: A sample manifest file for the Petstore API.
- `llm_friendly_specs/petstore-v3-openapi-plugin.json`: The output of the conversion process.

### Examples

A number of examples are provided to show how to use the specialized OpenAPI specs to generate function calls. They can help to compare the behaviour of the LLM when using the original spec vs. the specialized one.

These examples are located in the `samples` directory. See the README there for more information.
