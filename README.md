# YAML-File-Graphviz-Visualizer

A tool which generates a graphical visualization of .yaml config files using graphviz. Please install graphviz and pyyaml in order to use this tool.

Usage:
1. Convert .yaml file to DOT format
```
$ python YAMLtoDOT input.yaml > output.gv
```
2. Visualize using graphvis
```
$ python visualizer.py example.gv
```

