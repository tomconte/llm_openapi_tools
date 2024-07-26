# LLM Function Tools

This project is a collection of tools to work with Function Calling in Large Language Models (LLMs) such as OpenAI's GPT.

## Enriching OpenAPI specs for LLMs

The `llm_functools.openapi` module provides tools to enrich and specialize OpenAPI specs with additional information that can be used by LLMs to generate more accurate function calls. It uses a manifest file to configure the specialization process.

To convert an OpenAPI spec to an LLM-friendly spec from the command line, use the `llm_functools.convert` module:

```bash
python -m llm_functools.convert openapi.json manifest.json output.json
```

The following example specs and manifest are provided in the `tests/__fixtures__` directory:

- `openapi_specs/petstore-v3-openapi.json`: A sample OpenAPI spec for the Petstore API.
- `plugins/petstore-v3.yaml`: A sample manifest file for the Petstore API.
- `plugins/petstore-v3-openapi-plugin.json`: The output of the conversion process.

### Examples

A number of examples are provided to show how to use the specialized OpenAPI specs to generate function calls. They can help to compare the behaviour of the LLM when using the original spec vs. the specialized one.

These examples are located in the `samples` directory.

```bash
# Example using OpenAI API directly
pip install -r samples/python_openai/requirements.txt
python -m samples.python_openai.chat
```

```bash
# Example using LangChain
pip install -r samples/python_langchain/requirements.txt
python -m samples.python_langchain.chat
```

```bash
# Example using Semantic Kernel
cd samples/dotnet-sk
dotnet build
dotnet run
```

To configure these samples, you need to populate `.env` files in each sample directory with the appropriate API keys.

```bash
AZURE_OPENAI_ENDPOINT=https://foo.openai.azure.com/
AZURE_OPENAI_API_KEY=0123456789abcdef0123456789abcdef
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo-1106
OPENAI_API_VERSION=2024-05-01-preview
```
