# Using the samples

The samples use a local instance of the [Swagger Petstore Sample](https://github.com/swagger-api/swagger-petstore). You can start the server by running the following command:

```bash
docker pull swaggerapi/petstore3:unstable
docker run  --name swaggerapi-petstore3 -d -p 8080:8080 swaggerapi/petstore3:unstable
```

The server will be available at `http://localhost:8080`.

The OpenAPI specs used for testing have been modified to use the `http://localhost:8080` base URL. You can find the modified specs in the `tests/__fixtures__/openapi_specs` directory.

## Configuration

To configure these samples, you need to populate `.env` files in each sample directory with the appropriate API keys.

```bash
AZURE_OPENAI_ENDPOINT=https://foo.openai.azure.com/
AZURE_OPENAI_API_KEY=0123456789abcdef0123456789abcdef
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-35-turbo-1106
OPENAI_API_VERSION=2024-05-01-preview
```

## Running the examples

From the root of the repository, you can run the examples as follows:

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
