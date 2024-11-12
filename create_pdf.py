"""
Given a directory of screenshots, concatenate the screenshots to assemble a PDF
"""
import re
from pathlib import Path
import sys
import fitz

input_dir = Path(sys.argv[1])

sort_fn = lambda d: int(re.match(r'Chapter (\d+)', d.stem).group(1))
chapters = list(sorted(input_dir.glob('Chapter *'), key=sort_fn))

epilogue = input_dir / 'Epilogue'
if epilogue.exists():
  chapters.append(epilogue)

cover_file = next(input_dir.glob('*-cover.png'))

out_file = Path('output.pdf')
if out_file.exists():
  out_file.unlink()

doc = fitz.open()
doc.insert_file(cover_file)

curr_page = 2
toc = []

for chapter in chapters:
  toc.append([1, chapter.name, curr_page])

  for png_file in sorted(chapter.glob('*.png')):
    m = re.match(r'Screenshot_\d{4}-\d{2}-\d{2} (.*) - Art of Problem Solving', png_file.stem)
    page_name = m.group(1)
    print(f'{chapter.name}: {page_name}')
    doc.insert_file(png_file)
    toc.append([2, page_name, curr_page])

    curr_page += 1

doc.set_toc(toc)
doc.save(out_file)
