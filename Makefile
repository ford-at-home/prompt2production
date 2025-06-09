# Makefile to simplify build commands like `make build PROJECT=...`

PROJECT ?= iam-possible

build:
	python -m cli.build_project projects/$(PROJECT)/PROMPT_INPUTS.yaml
