from markupsafe import Markup
from htpy import html, head, meta, title as title_tag, style, body, h1

import katex

css = """
html {
  max-width: 70ch;
  padding: 3em 1em;
  margin: auto;
  line-height: 1.75;
  font-size: 1.25em;
}
"""

def doc(title, caption, *children):
    return str(
        html[
            head[
                meta(charset='utf-8'),
                title_tag[title],
                style[css],
                Markup(katex.snippet),
            ],
            body[
                h1[title],
                caption,
                *children,
            ],
        ]
    )
