"""
Process a markdown line so that it looks nicer when rendered.
"""
from pathlib import Path
import re
from dataclasses import dataclass

import figure


@dataclass
class Asy:
  lines: list[str]

class LineProcessor:
  def __init__(self, text):
    self.mode = None
    self.text = text
    self.figures = []
    self.unrendered_count = 0

  def process(self):
    return '\n'.join(self._process(self.text))

  def _process(self, text):
    for line in text.splitlines():
      result, mode = self.process_line(line, self.mode)
      self.mode = mode
      if result is not None:
        yield result

  def process_line(self, line, mode):
    line = line.strip()

    match mode:
      case Asy(lines):
        if line == '[/asy]':
          return self.get_figure(lines), None
        else:
          lines.append(line)
          return None, Asy(lines)
      case None:
        if line == '[asy]':
          return None, Asy([])
        elif m := re.match(r'Solution(?: (1|2))?\:', line):
          num = m.group(1) if m.group(1) else ''
          return f'\n<b>Solution {num}</b>\n', None
        elif m := re.match(r'(\d+)\.', line):
          return f'<h2>Problem {m.group(1)}.</h2>', None
        elif re.match(r'^(?:Your Answer|Your First Answer|Your Second Answer): .*', line):
          return None, None
        else:
          return line, None

  def get_figure(self, lines):
    code = '\n'.join(lines).strip()
    svg_file = figure.get_svg_file(code)

    number = len(self.figures)
    self.figures.append(code)

    if svg_file.exists() and get_svg_width(svg_file) > 60:
      body = f'<img src="/figures/{svg_file.name}">'
    else:
      self.unrendered_count += 1
      style = 'color: blue; font-size: 2em; border: 1px dashed blue; padding: 0.5em;'
      body = f'<span style="{style}">FIGURE</span>'

    return f'<a href="./figure-debug/{number}/"> {body} </a>'


def get_svg_width(svg_file : Path):
  with svg_file.open() as fp:
    # First two lines are metadata
    fp.readline()
    fp.readline()
    svg_line = fp.readline()
    m = re.match(r".*width='([\d.]+)pt'.*", svg_line)
    return float(m.group(1))

def transform(text):
  proc = LineProcessor(text)
  return proc.process(), proc
