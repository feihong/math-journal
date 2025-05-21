import json
from pyscript import document, fetch


async def size_150(_evt):
    textarea = document.querySelector('textarea')
    textarea.value = 'size(150);\n' + textarea.value

async def import_olympiad(_evt):
    textarea = document.querySelector('textarea')
    textarea.value = 'import olympiad;\n' + textarea.value

async def redraw(_evt):
    code = document.querySelector('textarea').value
    body = json.dumps({'code': code})
    svg_code = await fetch('/render-figure/', method='POST', body=body).text()
    document.querySelector('#svg').innerHTML = svg_code

async def save(_evt):
    data = json.loads(document.querySelector('#data').textContent)
    data['new_code'] = document.querySelector('textarea').value
    body = json.dumps(data)
    result = await fetch('/save-figure/', method='POST', body=body).text()
    print(result)
