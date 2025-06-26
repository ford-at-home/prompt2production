# Makefile to simplify build commands like `make build PROJECT=...`

PROJECT ?= iam-possible

build:
	python -m cli.build_project projects/$(PROJECT)/PROMPT_INPUTS.yaml

video:
	@# Check if venv exists, create if not
	@if [ ! -d "venv" ]; then \
		echo "📦 Creating virtual environment..."; \
		python3 -m venv venv; \
		. venv/bin/activate && pip install -r requirements.txt; \
	fi
	@# Check if .env exists, create from example if not
	@if [ ! -f ".env" ]; then \
		echo "📝 Creating .env file from template..."; \
		cp env.example .env; \
		echo "⚠️  Note: Add your API keys to .env for real video generation"; \
	fi
	@# Check for AWS credentials
	@if ! grep -q "\[personal\]" ~/.aws/credentials 2>/dev/null; then \
		echo ""; \
		echo "⚠️  AWS credentials not found!"; \
		echo "Please add your AWS credentials to ~/.aws/credentials:"; \
		echo ""; \
		echo "[personal]"; \
		echo "aws_access_key_id = YOUR_ACCESS_KEY"; \
		echo "aws_secret_access_key = YOUR_SECRET_KEY"; \
		echo ""; \
	fi
	@# Prompt for video topic
	@echo ""
	@echo "🎬 What would you like to explain in your video?"
	@echo "Examples: 'how wifi works', 'what is machine learning', 'how vaccines work'"
	@echo ""
	@read -p "Enter your topic: " topic; \
	. venv/bin/activate && AWS_PROFILE=personal python -m cli.build_project "$$topic"
