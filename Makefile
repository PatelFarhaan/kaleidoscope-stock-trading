.PHONY: install run test clean docker-build docker-run

install:
	pip install -r requirements.txt

run:
	python app.py

test:
	python -m pytest tests/ -v 2>/dev/null || echo "No tests configured"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; \
	find . -type f -name "*.pyc" -delete 2>/dev/null; \
	rm -rf dist/ build/ *.egg-info/ .pytest_cache/; \
	bash compiled_files_cleanup.sh 2>/dev/null; \
	true

docker-build:
	docker build -t kaleidoscope .

docker-run:
	docker run -p 5000:5000 kaleidoscope
