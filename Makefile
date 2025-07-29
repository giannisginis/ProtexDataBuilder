# Makefile

.PHONY: help clean build test lint docker-run precommit precommit-install

help:
	@echo "Usage:"
	@echo "  make build          - Build Docker image"
	@echo "  make env-install         - Installs dependencies using Poetry"
	@echo "  make test           - Run unit tests"
	@echo "  make test-coverage  - Run tests with coverage report"
	@echo "  make lint-check     - Run ruff/black formatting checks"
	@echo "  make lint-fix       - Run ruff/black formatting fixes"
	@echo "  make clean          - Remove build artifacts and output"
	@echo "  make build		     - Build the Docker image for the dataset pipeline"
	@echo "  make docker-run     - Run pipeline locally in Docker (CPU only)"
	@echo "  make precommit      - Run all pre-commit hooks"
	@echo "  make run            - Run the pipeline with default parameters"
	@echo "  make run-comet      - Run the pipeline with Comet-ML logging"

env-install:
	poetry install
	poetry run pre-commit install

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
	rm -rf .pytest_cache __pycache__ .mypy_cache dist .ruff_cache outputs/* *.egg-info .coverage htmlcov

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
		--reports_output /reports \
		--pretag \
		--blur-detection \
  		--dedup-detection

run:
	poetry run python -m pipeline.cli --video data/videos/timelapse_test.mp4 \
		--output outputs/frames \
		--coco_output outputs/annotations.coco.json \
		--reports_output reports \
		--pretag \
		--blur-detection \
  		--dedup-detection

run-comet:
	poetry run python -m pipeline.cli --video data/videos/timelapse_test.mp4 \
		--output outputs/frames \
		--coco_output outputs/annotations.coco.json \
		--reports_output reports \
		--pretag \
		--blur-detection \
  		--dedup-detection \
		--comet \
		--experiment-name dataset-generation
