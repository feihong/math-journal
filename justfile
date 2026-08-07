# You need to get this manually if you're not using a virtualenv
scripts_path := `python -c 'import sysconfig; print(sysconfig.get_path("scripts"))'`

help:
	just --list

install:
	pip install -r requirements.txt

# Merge all pdfs in the homework directory
merge:
	python merge_pdfs.py

clean:
	rm figures/*.{asy,svg}

# Launches a server on localhost:8080
serve:
	{{scripts_path}}/aiohttp-devtools runserver serve.py

zip_extension:
    zip alcumus-review-extension.zip alcumus-review-extension/*
