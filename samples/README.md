# Using the samples

The samples use a local instance of the [Swagger Petstore Sample](https://github.com/swagger-api/swagger-petstore). You can start the server by running the following command:

```bash
docker pull swaggerapi/petstore3:unstable
docker run  --name swaggerapi-petstore3 -d -p 8080:8080 swaggerapi/petstore3:unstable
```

The server will be available at `http://localhost:8080`.

The OpenAPI specs used for testing have been modified to use the `http://localhost:8080` base URL. You can find the modified specs in the `tests/__fixtures__/openapi_specs` directory.
