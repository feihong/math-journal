# /// script
# requires-python = ">=3.13"
# dependencies = ["pymupdf"]
# ///
"""
Create a new PDF by interleaving sections from two PDFs together
"""

import re
from collections import namedtuple
from dataclasses import dataclass
from pathlib import Path

import pymupdf

first_file = Path("~/Downloads/number-theory/book.pdf").expanduser()
second_file = Path("~/Downloads/number-theory/solutions.pdf").expanduser()
output_file = Path(__file__).parent / "output.pdf"


InsertRange = namedtuple("InsertRange", ["start", "end"])


@dataclass
class TocItem:
    file: pymupdf.Document
    page: int
    title: str
    level: int
    insert_range: InsertRange = None
    doc_page: int = None

    def __str__(self):
        ir = (
            f"({self.insert_range.start}, {self.insert_range.end})"
            if self.insert_range
            else "None"
        )
        return f"page: {self.page}, title: {self.title}, insert_range: {ir}, toc_page: {self.toc_page} "


TABLE_OF_CONTENTS = """
1 1 Frontmatter
1 12 Table of Contents

1 16 Chapter 1 Integers: The Basics
1 16 1.1 Introduction
1 18 1.2 Making Integers Out of Integers
1 22 1.3 Integer Multiples
1 26 1.4 Divisibility of Integers
1 29 1.5 Divisors
1 33 1.6 Using Divisors
1 35 1.7 Mathematical Symbols
1 36 1.8 Summary
1 38 Review Problems
1 39 Challenge Problems
2 1 Section Exercise Solutions
2 4 Review Problem Solutions
2 5 Challenge Problem Solutions

1 40 Chapter 2 Primes and Composites
1 40 2.1 Introduction
1 40 2.2 Primes and Composites
1 43 2.3 Identifying Primes I
1 46 2.4 Identifying Primes II
1 51 2.5 Summary
1 52 Review Problems
1 53 Challenge Problems
2 8 Section Exercise Solutions
2 10 Review Problem Solutions
2 11 Challenge Problem Solutions

1 54 Chapter 3 Multiples and Divisors
1 54 3.1 Introduction
1 54 3.2 Common Divisors
1 56 3.3 Greatest Common Divisors (GCDs)
1 58 3.4 Common Multiples
1 61 3.5 Remainders
1 65 3.6 Multiples, Divisors, and Arithmetic
1 68 3.7 The Euclidean Algorithm
1 75 3.8 Summary
1 76 Review Problems
1 77 Challenge Problems
2 13 Section Exercise Solutions
2 18 Review Problem Solutions
2 19 Challenge Problem Solutions

1 78 Chapter 4 Prime Factorization
1 78 4.1 Introduction
1 79 4.2 Factor Trees
1 83 4.3 Factorization and Multiples
1 87 4.4 Factorization and DiVisors
1 90 4.5 Rational Numbers and Lowest Terms
1 93 4.6 Prime Factorization and Problem Solving
1 95 4.7 Relationships Between LCMs and GCDs
1 99 4.8 Summary
1 102 Review Problems
1 103 Challenge Problems
2 21 Section Exercise Solutions
2 25 Review Problem Solutions
2 28 Challenge Problem Solutions

1 106 Chapter 5 Divisor Problems
1 106 5.1 Introduction
1 106 5.2 Counting Divisors
1 109 5.3 * Divisor Counting Problems
1 116 5.4 * Divisor Products
1 119 5.5 Summary
1 121 Review Problems
1 122 Challenge Problems
2 34 Section Exercise Solutions
2 38 Review Problem Solutions
2 39 Challenge Problem Solutions

1 124 Chapter 6 Special Numbers
1 124 6.1 Introduction
1 124 6.2 Some Special Primes
1 126 6.3 Factorials, Exponents and Divisibility . .
1 130 6.4 Perfect, Abundant, and Deficient Numbers
1 132 6.5 Palindromes
1 135 6.6 Summary
1 137 Review Problems
1 138 Challenge Problems
2 44 Section Exercise Solutions
2 47 Review Problem Solutions
2 50 Challenge Problem Solutions

1 140 Chapter 7 Algebra With Integers
1 140 7.1 Introduction
1 140 7.2 Problems
1 152 7.3 Summary
1 153 Challenge Problems
2 57 Challenge Problem Solutions

1 156 Chapter 8 Base Numbers
1 156 8.1 Introduction
1 156 8.2 Counting in Bundles
1 160 8.3 Base Numbers
1 163 8.4 Base Number Digits
1 165 8.5 Converting Integers Between Bases
1 170 8.6 * Unusual Base Number Problems
1 176 8.7 Summary
1 177 Review Problems
1 178 Challenge Problems
2 63 Section Exercise Solutions
2 70 Review Problem Solutions
2 72 Challenge Problem Solutions

1 180 Chapter 9 Base Number Arithmetic
1 180 9.1 Introduction
1 180 9.2 Base Number Addition
1 183 9.3 Base Number Subtraction
1 185 9.4 Base Number Multiplication
1 187 9.5 Base Number Division and Divisibility
1 190 9.6 Summary
1 190 Review Problems
1 191 Challenge Problems
2 76 Section Exercise Solutions
2 79 Review Problem Solutions
2 81 Challenge Problem Solutions

1 192 Chapter 10 Units Digits
1 192 10.1 Introduction
1 192 10.2 Units Digits in Arithmetic
1 199 10.3 Base Number Units Digits
1 202 10.4 Unit Digits Everywhere!
1 205 10.5 Summary
1 206 Review Problems
1 207 Challenge Problems
2 84 Section Exercise Solutions
2 88 Review Problem Solutions
2 90 Challenge Problem Solutions

1 210 Chapter 11 Decimals and Fractions
1 210 11.1 Introduction
1 210 11.2 Terminating Decimals
1 216 11.3 Repeating Decimals
1 220 11.4 Converting Decimals to Fractions
1 224 11.5 * Base Numbers and Decimal Equivalents
1 227 11.6 Summary
1 228 Review Problems
1 229 Challenge Problems
2 94 Section Exercise Solutions
2 98 Review Problem Solutions
2 98 Challenge Problem Solutions

1 232 Chapter 12 Introduction to Modular Arithmetic
1 232 12.1 Introduction
1 233 12.2 Congruence
1 239 12.3 Residues
1 242 12.4 Addition and Subtraction
1 247 12.5 Multiplication and Exponentiation
1 253 12.6 Patterns and Exploration
1 257 12.7 Summary
1 258 Review Problems
1 259 Challenge Problems
2 101 Section Exercise Solutions
2 107 Review Problem Solutions
2 109 Challenge Problem Solutions

1 262 Chapter 13 Divisibility Rules
1 262 13.1 Introduction
1 262 13.2 Divisibility Rules
1 270 13.3 * Divisibility Rules With Algebra
1 273 13.4 Summary
1 274 Review Problems
1 275 Challenge Problems
2 113 Section Exercise Solutions
2 116 Review Problem Solutions
2 117 Challenge Problem Solutions

1 276 Chapter 14 Linear Congruences
1 276 14.1 Introduction
1 277 14.2 Modular Inverses and Simple Linear Congruences
1 282 14.3 Solving Linear Congruences
1 287 14.4 Systems of Linear Congruences
1 293 14.5 Summary
1 295 Review Problems
1 296 Challenge Problems
2 123 Section Exercise Solutions
2 126 Review Problem Solutions
2 129 Challenge Problem Solutions

1 298 Chapter 15 Number Sense
1 298 15.1 Introduction
1 298 15.2 Familiar Factors and Divisibility
1 302 15.3 Algebraic Methods of Arithmetic
1 307 15.4 Useful Forms of Numbers
1 309 15.5 Simplicity
1 312 15.6 Summary
1 314 Review Problems
2 132 Review Problem Solutions

1 318 Hints to Selected Problems
1 326 Index
"""


def main():
    files = [pymupdf.open(first_file), pymupdf.open(second_file)]
    toc_items = get_toc_items(files)

    doc = pymupdf.open()

    # Build pdf
    for item in toc_items:
        # print(item)
        match item.insert_range:
            case InsertRange(start=start, end=end):
                doc.insert_file(item.file, from_page=start - 1, to_page=end - 1)

    toc = [[item.level, item.title, item.toc_page] for item in toc_items]
    doc.set_toc(toc)
    doc.save(output_file)


def _get_toc_items(files):
    prevs = {file: None for file in files}

    for line in TABLE_OF_CONTENTS.strip().splitlines():
        line = line.strip()
        if not line:
            continue

        file_index, page_start, title = line.split(" ", maxsplit=2)
        file_index = int(file_index) - 1
        file = files[file_index]
        page = int(page_start)
        level = get_toc_level(title)
        item = TocItem(file, page, title, level)

        if (prev := prevs[file]) is not None:
            if prev.page == item.page:
                if prev.insert_range is not None:
                    prev.insert_range = InsertRange(prev.page, prev.page)

                item.insert_range = None
            else:
                prev.insert_range = InsertRange(prev.page, item.page - 1)

        prevs[file] = item
        yield item

    # Set the item_range for the very last items
    for item in prevs.values():
        item.insert_range = InsertRange(item.page, item.file.page_count)


def get_toc_items(files):
    items = list(_get_toc_items(files))

    # Computer TOC pages because insert_ranges are not available until first loop finishes
    curr_page = 1
    for item in items:
        item.toc_page = curr_page
        print("  " * (item.level - 1), item.title, item.toc_page)

        if (ir := item.insert_range) is not None:
            curr_page += ir.end - ir.start + 1

    return items


def get_toc_level(title):
    if re.match(r"^(\d+\.\d+|Section|Review|Challenge) ", title):
        return 2
    else:
        return 1


if __name__ == "__main__":
    main()
