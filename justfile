install:
	pip install -r requirements.txt

nb:
	marimo edit scratch.py

publish:
	ghp-import --no-jekyll --push --no-history content

merge:
	python merge_pdfs.py
