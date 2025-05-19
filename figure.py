"""
Render asymptote code into svg files
"""
from pathlib import Path
import subprocess
import os
import hashlib


figures_dir = Path('figures')
asymptote_dir = Path('asymptote_dir').absolute()


def get_hash(code):
    return hashlib.md5(code.encode('utf-8')).hexdigest()


def get_svg_file(code):
    return figures_dir / f'{get_hash(code)}.svg'

def get_asy_file(code):
   return figures_dir / f'{get_hash(code)}.asy'

def generate_svg_files(asy_files):
    os.environ['ASYMPTOTE_DIR'] = str(asymptote_dir)
    cmd = [
        'asy',
        '-outformat', 'svg',
        *(f.name for f in asy_files),
    ]
    print(cmd)
    return subprocess.run(cmd, cwd=figures_dir, env=os.environ, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          encoding='utf-8')
