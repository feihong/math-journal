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

def doc(title, prebody, body):
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
                prebody,
                body,
            ],
        ]
    )

def figure_debug(name, number, asy_code):
    return doc(
        f'Figure {number} of {name}',
        None,
        div[
            textarea(cols=80, rows=10)[asy_code],
            button(py_click='on_click')['Redraw'],
            div(id='svg')[figure.generate_svg_code(asy_code)],
            script(type='py', src='/pyscript/figure_debug.py'),
        ]
    )
