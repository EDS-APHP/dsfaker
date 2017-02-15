install:
	pip install -r requirements.txt
	pip install .

uninstall:
	pip uninstall -y dsfaker

reinstall: uninstall install

.ONESHELL:
doc:
	pip install -r requirements.doc.txt
	cd docs
	rm -r _build
	make html

open-doc-chrome: doc
	google-chrome-stable docs/_build/html/index.html

test: install
	pip install -r requirements.test.txt
	python -m pytest --cov=dsfaker tests


test-with-coverage: install
	pip install -r requirements.test.txt
	python -m pytest --cov=dsfaker tests --cov-report=html

all: install
