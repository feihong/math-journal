import json

from markupsafe import Markup
from htpy import html, head, meta, title as title_tag, style, body as body_tag, h1, div, textarea, button, script

import snippets
import figure


css = """
html {
  max-width: 70ch;
  padding: 3em 1em;
  margin: auto;
  line-height: 1.75;
  font-size: 1.25em;
}
"""

def doc(title, body):
    return str(
        html[
            head[
                meta(charset='utf-8'),
                title_tag[title],
                style[css],
                Markup(snippets.mathjax),
                Markup(snippets.pyscript),
            ],
            body_tag[
                h1[title],
                body,
            ],
        ]
    )

row = div(style='display: flex; gap: 0.5em; padding-bottom: 0.5em;')

def figure_debug(name, number, asy_code):
    data = json.dumps({'name': name, 'old_code': asy_code})
    return doc(
        f'Figure {number} of {name}',
        div[
            script(id='data', type='application/json')[Markup(data)],
            row[
                button(py_click='size_150')['size(150)'],
                button(py_click='import_olympiad')['import olympiad'],
            ],
            textarea(cols=80, rows=10)[asy_code],
            row[
                button(py_click='redraw')['Redraw'],
                button(py_click='save')['Save']
            ],
            div(id='svg')[figure.generate_svg_code(asy_code)],
            script(type='py', src='/pyscript/figure_debug.py'),
        ]
    )
