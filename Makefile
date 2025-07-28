# Makefile

.PHONY: help clean build test lint docker-run precommit

help:
	@echo "Usage:"
	@echo "  make build          - Build Docker image"
	@echo "  env-install         - Installs dependencies using Poetry"
	@echo "  make test           - Run unit tests"
	@echo "  make lint-check     - Run ruff/black formatting checks"
	@echo "  make lint-fix       - Run ruff/black formatting fixes"
	@echo "  make clean          - Remove build artifacts and output"
	@echo "  make docker-run     - Run pipeline locally in Docker (CPU only)"
	@echo "  make precommit      - Run all pre-commit hooks"

env-install:
	poetry install

test:
	poetry run pytest -v

test-coverage:
	poetry run pytest --cov=pipeline --cov-report=xml --cov-fail-under=90 --cov-report=html -v

lint-check:
	poetry run ruff check
	poetry run black . --check

lint-fix:
	poetry run ruff check --fix
	poetry run black .

precommit:
	poetry run pre-commit run --all-files

clean:
	rm -rf .pytest_cache __pycache__ .mypy_cache dist .ruff_cache outputs/* *.egg-info

build:
	docker build -t dataset-pipeline .

docker-run:
	docker run --rm -t\
		-v $(PWD)/data/videos:/data/videos \
		-v $(PWD)/outputs:/outputs \
		-v $(PWD)/reports:/reports \
		dataset-pipeline \
		--video /data/videos/timelapse_test.mp4 \
		--output /outputs/frames \
		--coco_output /outputs/detections/detections.coco.json \
		--pretag \
		--blur-detection \
  		--dedup-detection
