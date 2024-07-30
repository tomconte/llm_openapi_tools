import argparse
import json
import yaml

from llm_openapi_tools.openapi import convert_spec


def main(input, manifest):
    with open(input, 'r') as f:
        base_openapi_spec = json.loads(f.read())

    with open(manifest, 'r') as f:
        plugin_config = yaml.safe_load(f)

    genai_openapi_spec = convert_spec(base_openapi_spec, plugin_config)

    print(json.dumps(genai_openapi_spec))


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input file path")
    parser.add_argument("manifest", help="Manifest file path")
    args = parser.parse_args()

    main(args.input, args.manifest)
