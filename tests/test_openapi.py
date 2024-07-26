"""Unit tests for the spec module."""

import pytest
import yaml

from openapi_spec_validator.validation.exceptions import OpenAPIValidationError

from llm_functools.openapi import convert_spec


@pytest.fixture(scope="session")
def plugin_config():
    with open('tests/__fixtures__/plugins/petstore-v3.yaml', 'r') as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def openapi_spec():
    with open('tests/__fixtures__/openapi_specs/petstore-v3-openapi.yaml', 'r') as f:
        return yaml.safe_load(f)


def test_convert_spec(openapi_spec, plugin_config):
    # Convert the OpenAPI spec to a APIPlugin spec
    new_spec = convert_spec(openapi_spec, plugin_config)

    # Check that the new spec is valid
    assert new_spec is not None

    assert new_spec["openapi"] == "3.0.2"
    assert new_spec["info"]["title"] == "Pet Store plugin"

    assert "paths" in new_spec
    assert len(new_spec["paths"]) == 2

    assert "components" in new_spec

    assert "/pet/{petId}" in new_spec["paths"]
    assert "/pet/findByStatus" in new_spec["paths"]


def test_convert_invalid_spec(openapi_spec, plugin_config):
    # Change the OpenAPI spec to make it invalid
    openapi_spec["info"] = None

    # Convert the OpenAPI spec to a APIPlugin spec
    with pytest.raises(OpenAPIValidationError):
        convert_spec(openapi_spec, plugin_config)
