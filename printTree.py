import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import pathlib as path

import json

#import re
#lcc_re = re.compile("(([A-Z]+(\\.[A-Z0-9]*)*))( - [^-]*)+")

def traverse_dir(root, fdir, ffile, level):
  # do folders first
  for dir in root.iterdir():
    if dir.is_dir():
      if fdir(dir, level):
        traverse_dir(dir, fdir, ffile, level+1)

  # then do files
  for file in root.iterdir():
    if file.is_file():
      ffile(file, level)


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


def add2dict():
  d = list()
  last_level = 0
  stk = [d]
  
  def add2dict_dir(dir, level):
    nonlocal last_level
    
    isArchive, dirname = is_archive(dir)
    print_dir(dir, level)
    if level > last_level:
      stk.append(stk[-1][-1]["children"])
      last_level = level
      
    while level < last_level:
      stk.pop()
      last_level -= 1
    print(len(stk))
    stk[-1].append({"name": dirname, "children": list()})
    return not isArchive
    
  def add2dict_file(file, level):
    pass
  
  def get_dict():
    return d
    
  return add2dict_dir, add2dict_file, get_dict
  
if __name__ == "__main__":
  p = path.Path(os.path.dirname(os.path.realpath(__file__)))
  #traverse_dir(
  #  p,
  #  print_dir,
  #  print_file,
  #  0)
    
  add2dict_dir, add2dict_file, get_dict = add2dict()
  traverse_dir(
    p,
    add2dict_dir,
    add2dict_file,
    0)
  print(json.dumps(get_dict(), indent=4))