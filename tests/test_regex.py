import sys

THEIAPATH = '/home/dev0/theia'    # path to access modules of theia
sys.path.insert(0, THEIAPATH)

from theia.helpers.tools import shortRef

def test(string):
    print string + " --> " + shortRef(string)

strings = ["tt-rrr",
            "hello-r",
            "hello-tt",
            "hello-tttrrrt",
            "jim-tttrrt",
            "kile-ttrtttrrt",
            "hj-ttrtt",
            "hi-tttrttt",
            "hello-tt"]

for string in strings:
    test(string)
