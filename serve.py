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
             for f in sorted(problems_dir.glob('*.md')))
        ]
    )
    return web.Response(text=doc, content_type='html')

async def document(request):
    name = request.match_info.get('name')
    path = problems_dir / (name + '.md')

    proc = normalize.LineProcessor(path.read_text())
    markdown_code = proc.process()

    if proc.unrendered_count > 0:
        caption = div[
            a(href=f"/{name}/render-figures")[f"Render {proc.unrendered_count} figures"]
        ]
    else:
        caption = None

    doc = template.doc(
        name.capitalize().replace('-', ' '),
        caption,
        markdown.render(markdown_code),
    )

    return web.Response(text=doc, content_type='html')

async def render_figures(request : web.Request):
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

    if proc.returncode == 0:
        return web.HTTPPermanentRedirect(f'/{name}/')
    else:
        return web.Response(text=f'{proc.stdout}\n\nReturn code: {proc.returncode}')

async def figure_debug(request):
    name = request.match_info.get('name')
    number = int(request.match_info.get('number'))
    path = problems_dir / (name + '.md')

    proc = normalize.LineProcessor(path.read_text())
    proc.process()

    asy_code = proc.figures[number]
    return web.Response(text=template.figure_debug(name, number, asy_code), content_type='html')

async def render_figure(request : web.Request):
    result = await request.json()
    return web.Response(text=str(figure.generate_svg_code(result['code'])), content_type='html')


app = web.Application()
app.add_routes([
    web.get('/', index),
    web.static('/figures', figure.figures_dir, show_index=True),
    web.static('/pyscript', 'pyscript', show_index=True),
    web.get('/{name}/', document),
    web.get('/{name}/render-figures', render_figures),
    web.get('/{name}/figure-debug/{number}/', figure_debug),
    web.post('/render-figure/', render_figure)
])

if __name__ == '__main__':
    web.run_app(app)
