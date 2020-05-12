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
  '~~ CMU/*/*',
  '~~ CMU/*.whtt',
  '~~ CMU/*.gif',
  '~~~ Library-of-Ashurbanipal/',
]

from fnmatch import fnmatch
def ignore(path):
  for ignore in ignores:
    if path.match(ignore):
      return True
  return False
  
def is_archive(dir):
  if dir.parts[-1].endswith(".archive"):
    return True, dir.parts[-1]#[:-8]
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


def print_dir(dir, fdir, ffile, level):  
  indent = ' ' * 4 * (level)
  
  isArchive, dirname = is_archive(dir)
  #print('{}{}'.format(indent, dirname))
  if isArchive:
    return []
  else:
    return [item for item in iter_dir(dir, fdir, ffile, level+1)]

def print_file(file, ffile, level):
  subindent = ' ' * 4 * (level) * 0
  print('{}{}'.format(subindent, file.parts[-1]))


def dir2Tree(dir, fdir, ffile, level):
  isArchive, dirname = is_archive(dir)
  if isArchive:
    return {"name": dirname, "children": []}
  else:
    return {"name": dirname, "children": [item for item in iter_dir(dir, fdir, ffile, level+1)]}

def file2Tree(file, ffile, level):
  return file.parts[-1]


if __name__ == "__main__":
  if '-p' in sys.argv:
    funcs = (print_dir, print_file)
  else:
    funcs = (dir2Tree, file2Tree)
  
  root = sys.argv[1] if len(sys.argv) >= 2 else os.path.dirname(os.path.realpath(__file__))
  p = path.Path(root)
  rst = [item for item in iter_dir(p, *funcs, 0)]
          
  if '-p' in sys.argv:
    pass
  else:
    import datetime
    
    rst = {
      'meta': {
        'last-modified': str(datetime.datetime.today())
      },
      'data': rst
    }
    
    print(json.dumps(
      rst,
      indent=4, ensure_ascii=False))
