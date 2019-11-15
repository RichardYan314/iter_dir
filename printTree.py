# python printTree.py > /d/My\ Document/Documents/blog/source/_posts/Library-of-Ashurbanipal/tree.json

import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import pathlib as path

import json

#import re
#lcc_re = re.compile("(([A-Z]+(\\.[A-Z0-9]*)*))( - [^-]*)+")

ignores = [
  '.git/',
  '.gitignore',
  'diff*',
  'printTree.py',
  'Library-of-Ashurbanipal/',
  '**/*.archive/',
]

from fnmatch import fnmatch, translate
def ignore(path):
  for ignore in ignores:
    if path.match(ignore):
      return True
  return False
  
def is_archive(dir):
  if dir.parts[-1].endswith(".archive"):
    return True, dir.parts[-1][:-8]
  else:
    return False, dir.parts[-1]

def iter_dir(root, fdir, ffile, level):
  # do folders first
  for dir in root.iterdir():
    if dir.is_dir() and not ignore(dir):
      yield fdir(dir, fdir, ffile, level)

  # then do files
  for file in root.iterdir():
    if file.is_file() and not ignore(file):
      yield ffile(file, ffile, level)


def is_archive(dir):
  if dir.parts[-1].endswith(".archive"):
    return True, dir.parts[-1][:-8]
  else:
    return False, dir.parts[-1]

def print_dir(dir, fdir, ffile, level):  
  indent = ' ' * 4 * (level)
  
  isArchive, dirname = is_archive(dir)
  print('{}{}'.format(indent, dirname))
  if isArchive:
    return []
  else:
    return [item for item in iter_dir(dir, fdir, ffile, level+1)]

def print_file(file, ffile, level):
  subindent = ' ' * 4 * (level)
  print('{}{}'.format(subindent, file.parts[-1]))


def dir2Tree(dir, fdir, ffile, level):
  isArchive, dirname = is_archive(dir)
  if isArchive:
    return dirname
  else:
    return {"name": dirname, "children": [item for item in iter_dir(dir, fdir, ffile, level+1)]}

def file2Tree(file, ffile, level):
  return file.parts[-1]


if __name__ == "__main__":
  if '-p' in sys.argv:
    funcs = (print_dir, print_file)
  else:
    funcs = (dir2Tree, file2Tree)
  
  p = path.Path(os.path.dirname(os.path.realpath(__file__)))
  rst = [item for item in iter_dir(p, *funcs, 0)]
          
  if '-p' in sys.argv:
    pass
  else:
    print(json.dumps(
      rst,
      indent=4, ensure_ascii=False))
