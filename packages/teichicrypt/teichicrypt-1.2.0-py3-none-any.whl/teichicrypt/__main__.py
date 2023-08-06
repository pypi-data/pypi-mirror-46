"""Main entry point"""

import sys
if sys.argv[0].endswith("__main__.py"):
    sys.argv[0] = "python -m teichicrypt"

from . import main
from tkinter import filedialog
from tkinter import messagebox as mb
from tkinter import Tk, Entry, Button, Radiobutton, BooleanVar, Label, Text
from tkinter.ttk import Progressbar
main()
