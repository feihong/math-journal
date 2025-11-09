"""
Merge all homework PDFs into a single PDF that has a table of contents

Reference: https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/examples/import-toc/import.py

"""
from pathlib import Path
import pymupdf

output_file = Path('homework.pdf')
homework_dir = Path('homework')


def main():
  # Copy all homework ##.pdf files into this project's homework directory
  downloaded_files = Path('~/Downloads').expanduser().glob('homework ??.pdf')
  for downloaded_file in downloaded_files:
    dest = homework_dir / downloaded_file.name
    downloaded_file.replace(dest)
    print(f'Move {downloaded_file} to {dest}')
  print(list(downloaded_files))

  # Treat the number at the end of filename as an int instead of a string
  def key_function(path: Path):
    name, num = path.stem.rsplit(' ', maxsplit=1)
    return (name, int(num))

  # Get all PDF files in order
  pdf_files = list(sorted(homework_dir.glob('*.pdf'), key=key_function))
  merge(pdf_files)


def merge(pdf_files):
  doc = pymupdf.open()

  curr_page = 1
  toc = []

  for i, pdf_file in enumerate(pdf_files, 1):
    new_doc = pymupdf.open(pdf_file)
    doc.insert_pdf(new_doc)

    toc_item = [1, f'Homework {i}', curr_page]
    print(toc_item)
    toc.append(toc_item)

    curr_page += len(new_doc)

  doc.set_toc(toc)

  doc.save(output_file)
  print(f'Saved {output_file}')

if __name__ == '__main__':
  main()
