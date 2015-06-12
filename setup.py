#For use with py2exe to convert this to a standalone executable
#http://www.py2exe.org/

from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 1}},
    console = [{'script': "EventScrape.py"}],
    zipfile = None,
)