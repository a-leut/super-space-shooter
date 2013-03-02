from distutils.core import setup
import py2exe, glob, os

SCRIPT_MAIN = "main.py"
 
MODULE_EXCLUDES =[
'email',
'AppKit',
'Foundation',
'bdb',
'difflib',
'tcl',
'Tkinter',
'Tkconstants',
'curses',
'distutils',
'setuptools',
'urllib',
'urllib2',
'urlparse',
'BaseHTTPServer',
'_LWPCookieJar',
'_MozillaCookieJar',
'ftplib',
'gopherlib',
'_ssl',
'htmllib',
'httplib',
'mimetools',
'mimetypes',
'rfc822',
'tty',
'webbrowser',
'socket',
'hashlib',
'base64',
'compiler',
'pydoc']

INCLUDE_STUFF = ['encodings',"encodings.latin_1",]

extra_files = [ ("data",glob.glob(os.path.join('data','*.png'))),
                ("data",glob.glob(os.path.join('data','*.wav'))),
                ("data",glob.glob(os.path.join('data','*.ttf')))]
 
setup (
    windows=[
             {'script': SCRIPT_MAIN,}],
    options = {"py2exe": {
                  "optimize": 2,
                  "includes": INCLUDE_STUFF,
                  "compressed": 1,
                  "ascii": 1,
                  "bundle_files": 2,
                  "ignores": ['tcl','AppKit','Numeric','Foundation'],
                  "excludes": MODULE_EXCLUDES} },
    data_files = extra_files,
    name = "ALEX IS RADICAL"
      )