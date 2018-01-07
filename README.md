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

Given the example .yaml file provided, such a graph is generated:
<p align="center">
  <img src="https://github.com/benedictprintz/YAML-File-Graphviz-Visualizer/blob/master/Example.png" width="750">
</p>
