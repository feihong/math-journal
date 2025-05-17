from pathlib import Path

from aiohttp import web
from htpy import ul, li, a

import template
import markdown


problems_dir = Path('problems')


async def index(_request):
    doc = template.doc('Index',
        ul[
            (li[a(href=f'/' + f.stem)[f.stem]]
             for f in problems_dir.glob('*.md'))
        ]
    )
    return web.Response(text=doc, content_type='html')

async def doc(request):
    name = request.match_info.get('name')
    path = problems_dir / (name + '.md')

    doc = template.doc(
        name.replace('-', ' '),
        markdown.render(path.read_text()),
    )

    return web.Response(text=doc, content_type='html')

app = web.Application()
app.add_routes([
    web.get('/', index),
    web.get('/{name}', doc)])

if __name__ == '__main__':
    web.run_app(app)
