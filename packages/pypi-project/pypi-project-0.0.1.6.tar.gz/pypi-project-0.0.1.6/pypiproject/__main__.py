"""pypr - PyPi Project by the1bit
Usage:
  pypr --version
  pypr core --input TEXT
  pypr core -i TEXT -o string
  pypr core -i TEXT --output json
  

Arguments:
  PATH  destination path
Options:
  -h --help            show this help message and exit
  -v --version         show version and exit
  --verbose            print status messages
  -i --input           set input and exit
  -o --output          output format default is string. Possible values: string, json
"""



from docopt import docopt
from pypiproject.version import __version__
__author__ = "the1bit"


arguments = docopt(__doc__, version=__version__)


if __name__ == '__main__':
  # Core module  
  if docopt(__doc__)["core"]:
      from .core.pypiproject_core import *
      # Input text
      if docopt(__doc__)["--input"]:
        # Get your text
        yourText = docopt(__doc__)["TEXT"]
        # Check outputs - if exists and json
        if docopt(__doc__)["--output"] and docopt(__doc__)["json"]:
          print([getText(yourText, 'json')])
        else:
          # default output
          print(getText(yourText))



# Help for you
#print(arguments)





