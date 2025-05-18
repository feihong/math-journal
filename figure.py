"""
Render asymptote code into svg files
"""
from pathlib import Path
import subprocess
import hashlib


figures_dir = Path('figures')


def get_hash(code):
    return hashlib.md5(code.encode('utf-8')).hexdigest()


def get_svg_file(code):
    return figures_dir / f'{get_hash(code)}.svg'

def get_asy_file(code):
   return figures_dir / f'{get_hash(code)}.asy'

def generate_svg_files(asy_files):
    cmd = [
        'asy',
        '-outformat', 'svg',
        *(f.name for f in asy_files),
    ]
    print(cmd)
    return subprocess.run(cmd, cwd=figures_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='utf-8')
