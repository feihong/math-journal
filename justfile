set dotenv-load := true

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

build_extensions:
    uv run --env-file .env build_extensions.py

publish_extensions: build_extensions
    rsync -avz _build/* $SERVER_LOCATION
