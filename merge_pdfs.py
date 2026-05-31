"""
Merge all homework PDFs into a single PDF that has a table of contents

Reference: https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/examples/import-toc/import.py

"""
import re
from pathlib import Path
import functools
import typing
import pymupdf


input_dir = Path('~/Downloads/aops intro physics').expanduser()
output_file = input_dir / 'AoPS Intro Physics Homework.pdf'


# Specifies relative ordering of files within a week as well as what their titles are in the TOC
file_order_title = [
  ('reading', 'Prep Work'),
  ('homework', 'Homework'),
  ('solution', 'Homework Solutions')
]


title_map = dict(file_order_title)
order_map = dict((p[0], i) for i, p in enumerate(file_order_title))


@functools.total_ordering
class PdfFile(typing.NamedTuple):
  filename: str
  name: str
  num: int

  @staticmethod
  def make(filename):
    if m := re.match(r'([a-z]+) (\d{2})\.pdf', filename):
      name, num = m.groups()
      return PdfFile(filename=filename, name=name, num=int(num))
    else:
      raise ValueError

  @property
  def title(self):
    title_suffix = title_map[self.name]
    return f'Week {self.num} {title_suffix}'

  @property
  def path(self):
    return input_dir / self.filename

  def __eq__(self, other):
    return (self.num, self.name) == (other.num, other.name)

  def __lt__(self, other):
    return (self.num, order_map[self.name]) < (other.num, order_map[other.name])


def get_input_pdf_files():
  valid_names = {name for name, _title in file_order_title}

  for f in input_dir.glob('*.pdf'):
    try:
      pf = PdfFile.make(f.name)
      if pf.name in valid_names:
        yield pf
    except ValueError:
      pass # filename doesn't have correct format


def main():
  # Get all PDF files in the correct order
  pdf_files = sorted(get_input_pdf_files())
  merge(pdf_files)


def merge(pdf_files):
  doc = pymupdf.open()

  curr_page = 1
  toc = []

  for pdf_file in pdf_files:
    new_doc = pymupdf.open(pdf_file.path)
    doc.insert_pdf(new_doc)

    toc_item = [1, pdf_file.title, curr_page]
    print(toc_item)
    toc.append(toc_item)

    curr_page += len(new_doc)

  doc.set_toc(toc)

  doc.save(output_file)
  print(f'Saved {output_file.absolute()}')


if __name__ == '__main__':
  main()
