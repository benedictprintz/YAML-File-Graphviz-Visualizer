#!/usr/bin/python
# vim: fileencoding=utf-8

'''
Visualize DOT file

Author: Benedict Printz
Usage: python visualizer.py example.gv
'''


import sys
from graphviz import render

render('dot', 'png', sys.argv[1])



