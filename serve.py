from pathlib import Path

from aiohttp import web
from htpy import ul, li, a, div

import template
import markdown
import normalize
import figure


problems_dir = Path('problems')


async def index(_request):
    doc = template.doc('Index', None,
        ul[
            (li[a(href=f'/{f.stem}/')[f.stem]]
             for f in problems_dir.glob('*.md'))
        ]
    )
    return web.Response(text=doc, content_type='html')

async def document(request):
    name = request.match_info.get('name')
    path = problems_dir / (name + '.md')

    proc = normalize.LineProcessor(path.read_text())
    markdown_code = proc.process()

    if len(proc.figures) == 0:
        caption = None
    else:
        caption = div[
            a(href=f"/{name}/render-figures")["Render figures"]
        ]

    doc = template.doc(
        name.capitalize().replace('-', ' '),
        caption,
        markdown.render(markdown_code),
    )

    return web.Response(text=doc, content_type='html')

async def render_figures(request):
    name = request.match_info.get('name')
    path = problems_dir / (name + '.md')

    proc = normalize.LineProcessor(path.read_text())
    proc.process()

    asy_files = []
    for code in proc.figures:
        asy_file = figure.get_asy_file(code)
        if not asy_file.exists():
            asy_file.write_text(code)
        asy_files.append(asy_file)

    proc = figure.generate_svg_files(asy_files)

    return web.Response(text=proc.stdout)

app = web.Application()
app.add_routes([
    web.get('/', index),
    web.static('/figures', figure.figures_dir, show_index=True),
    web.get('/{name}/', document),
    web.get('/{name}/render-figures', render_figures),
])

if __name__ == '__main__':
    web.run_app(app)
