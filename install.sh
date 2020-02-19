#!/bin/bash
pyinstaller --clean -F -n familyViewer --add-binary /System/Library/Frameworks/Tcl.framework/Tcl:Tcl --add-binary /System/Library/Frameworks/Tk.framework/Tk:Tk -w src/tkgui.py
