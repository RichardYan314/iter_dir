import difflib
import sys

fromfile = sys.argv[1]
tofile = sys.argv[2]
fromlines = open(fromfile, 'r', encoding='UTF8').readlines()
tolines = open(tofile, 'r', encoding='UTF8').readlines()

diff = difflib.HtmlDiff(wrapcolumn=80).make_file(fromlines,tolines,fromfile,tofile)

difffile = sys.argv[3] if len(sys.argv) >= 4 else 'diff.html'
with open(difffile, 'w', encoding='UTF8') as f:
  f.writelines(diff)
