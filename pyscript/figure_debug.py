import json
from pyscript import document, fetch

async def on_click(_evt):
    code = document.querySelector('textarea').value
    body = json.dumps({'code': code})
    svg_code = await fetch('/render-figure/', method='POST', body=body).text()
    document.querySelector('#svg').innerHTML = svg_code

