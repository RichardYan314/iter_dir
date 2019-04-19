# python printTree.py > /d/My\ Document/Documents/blog/source/_posts/Library-of-Ashurbanipal/tree.json

import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import pathlib as path

import json

#import re
#lcc_re = re.compile("(([A-Z]+(\\.[A-Z0-9]*)*))( - [^-]*)+")

def iter_dir(root, fdir, ffile, level):
  # do folders first
  for dir in root.iterdir():
    if dir.is_dir():
      yield fdir(dir, level)

  # then do files
  for file in root.iterdir():
    if file.is_file():
      yield ffile(file, level)


def is_archive(dir):
  if dir.parts[-1].endswith(".archive"):
    return True, dir.parts[-1][:-8]
  else:
    return False, dir.parts[-1]

def print_dir(dir, level):
  indent = ' ' * 4 * (level)
  
  isArchive, dirname = is_archive(dir)
  print('{}{}'.format(indent, dirname))
  return not isArchive


def print_file(file, level):
  subindent = ' ' * 4 * (level)
  print('{}{}'.format(subindent, file.parts[-1]))


def dir2Tree(dir, level):
  isArchive, dirname = is_archive(dir)
  if isArchive:
    return dirname
  else:
    return {"name": dirname, "children": [item for item in iter_dir(dir, dir2Tree, file2Tree, level+1)]}


def file2Tree(file, level):
  return file.parts[-1]


if __name__ == "__main__":
  p = path.Path(os.path.dirname(os.path.realpath(__file__)))
  print(json.dumps(
    [item for item in iter_dir(p, dir2Tree, file2Tree, 0)
          if not ((item["name"] if isinstance(item, dict) else item) in [".git", ".gitignore", __file__])],
    indent=4, ensure_ascii=False))
