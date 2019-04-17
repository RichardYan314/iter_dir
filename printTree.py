import sys
#sys.stdout.reconfigure(encoding='utf-8')

import os
import pathlib as path

import re
lcc_re = re.compile("(([A-Z]+(\\.[A-Z0-9]*)*))( - [^-]*)+")

def list_files(root, level):
  for dir in root.iterdir():
    if dir.is_dir():
      indent = ' ' * 4 * (level)
      print('{}{}/'.format(indent, dir.parts[-1]))
      if dir.parts[-1].endswith(".archive"):
        return
      else:
        list_files(dir, level+1)
        
  subindent = ' ' * 4 * (level + 1)
  for file in root.iterdir():
    if file.is_file():
      print('{}{}'.format(subindent, file.parts[-1]))
            
if __name__ == "__main__":
  p = path.Path(os.path.dirname(os.path.realpath(__file__)))
  list_files(p, 0)
  