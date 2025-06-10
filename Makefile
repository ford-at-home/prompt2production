# Makefile to simplify build commands like `make build PROJECT=...`

PROJECT ?= quick-demo

build:
	python -m cli.build_project projects/$(PROJECT)/PROMPT_INPUTS.yaml

clean:
	rm -rf output/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

setup:
	pip install -r requirements.txt
