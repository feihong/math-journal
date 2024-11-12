"""
Given a directory of screenshots, concatenate the screenshots to assemble a PDF
"""
import re
from pathlib import Path
import sys
import fitz

input_dir = Path(sys.argv[1])
cover_file = next(input_dir.glob('*-cover.png'))


def get_chapters():
  sort_fn = lambda d: int(re.match(r'Chapter (\d+)', d.stem).group(1))
  chapters = list(sorted(input_dir.glob('Chapter *'), key=sort_fn))

  epilogue = input_dir / 'Epilogue'
  if epilogue.exists():
    chapters.append(epilogue)

  references = input_dir / 'References'
  if references.exists():
    chapters.append(references)

  return chapters

def validate_screenshots():
  result = True

  for chapter in get_chapters():
    for png_file in sorted(chapter.glob('*.png')):
      if re.match(r'.*\(\d\)$', png_file.stem):
        print(f'\033[93mInvalid file name: {png_file}')
        result = False

  return result

def get_screenshot_name(screenshot):
  return re.match(r'Screenshot_\d{4}-\d{2}-\d{2} (.*) - Art of Problem Solving', screenshot.stem).group(1)

def get_screenshots(chapter):
  """
  Get screenshots for the given chapter in the correct order
  """
  # Make sure review problems come before challenge problems
  def sort_fn(f):
    name = get_screenshot_name(f)
    if name.startswith('Review Problems'):
      return 'A' + name
    elif name.startswith('Challenge Problems'):
      return 'B' + name
    else:
      return name

  screenshots = list(chapter.glob('*.png'))
  screenshots.sort(key=sort_fn)

  return screenshots

if not validate_screenshots():
  sys.exit(1)

out_file = Path('output.pdf')
if out_file.exists():
  out_file.unlink()

doc = fitz.open()
doc.insert_file(cover_file)

curr_page = 2
toc = []

for chapter in get_chapters():
  toc.append([1, chapter.name, curr_page])

  for png_file in get_screenshots(chapter):
    page_name = get_screenshot_name(png_file)
    print(f'{chapter.name}: {page_name}')
    doc.insert_file(png_file)
    toc.append([2, page_name, curr_page])

    curr_page += 1

doc.set_toc(toc)
doc.save(out_file)
