.PHONY: requirements

help:
	@echo "make requirements - install requirements"

requirements:
	pip install -r requirements.txt
	pip install -r requirements_dev.txt
	pip install -r samples/python_openai/requirements.txt
	pip install -r samples/python_langchain/requirements.txt
