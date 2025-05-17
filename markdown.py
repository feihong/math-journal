# https://mdit-py-plugins.readthedocs.io/en/latest/#math

from markupsafe import Markup
from markdown_it import MarkdownIt
from mdit_py_plugins import texmath, dollarmath, amsmath

def latex_renderer(s, opt):
  "Rewrite dollar-delimited math to use brackets instead"
  start, end = (r'\[', r'\]') if opt['display_mode'] else (r'\(', r'\)')
  return start + s + end

md = MarkdownIt('commonmark', {'linkify': True})

md.use(texmath.texmath_plugin, delimiters='brackets')
md.use(dollarmath.dollarmath_plugin, renderer=latex_renderer)
md.use(amsmath.amsmath_plugin, renderer=lambda s: r'\[' + s + r'\]')
md.enable(['linkify'])

def render(code):
    return Markup(md.render(code))
