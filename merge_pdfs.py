"""
Merge all homework PDFs into a single PDF that has a table of contents

Reference: https://github.com/pymupdf/PyMuPDF-Utilities/blob/master/examples/import-toc/import.py

"""
from pathlib import Path
import fitz

pdf_files = list(sorted(Path('homework').glob('*.pdf')))

doc = fitz.open()

curr_page = 1
toc = []

for i, pdf_file in enumerate(pdf_files, 1):
  new_doc = fitz.open(pdf_file)
  doc.insert_pdf(new_doc)

  toc_item = [1, f'Homework {i}', curr_page]
  print(toc_item)
  toc.append(toc_item)

  curr_page += len(new_doc)

doc.set_toc(toc)
print(doc.get_toc())

doc.save('homework.pdf')
