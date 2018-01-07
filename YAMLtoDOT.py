#!/usr/bin/python
# vim: fileencoding=utf-8


'''
Translate YAML written text to graphviz dot

Author: Benedict Printz
Usage: python YAMLtoDOT.py input.yaml > output.gv
'''

import yaml
import sys


def quote(s):
    return u'"{}"'.format(s.replace(u'"', u'\\"'))


def add_graph_directives_input_output(a, b):
    global p
    global h
    global graph_directives

    # Case for a -> b (1)
    if a == b:
        if a == 'premise':
            graph_directives.append(a+str(p+1)+' [label = "premise"]')
            graph_directives.append('%s -> %s' % (a+str(p),a+str(p+1)))
            p += 1

        elif a == 'hypothesis':
            graph_directives.append(a+str(h+1)+' [label = "hypothesis"]')
            graph_directives.append('%s -> %s' % (a+str(h),a+str(h+1)))
            h += 1
    else:
        if a == 'premise':
            graph_directives.append('%s -> %s' % (a+str(p), quote(b)))
        elif b == 'premise':
            graph_directives.append('%s -> %s' % (quote(a), b + str(p)))
        elif a == 'hypothesis':
            graph_directives.append('%s -> %s' % (a + str(h), quote(b)))
        elif b == 'hypothesis':
            graph_directives.append('%s -> %s' % (quote(a), b + str(h)))
        else:
            graph_directives.append('%s -> %s' % (quote(a), quote(b)))


def add_graph_directives_input_module(a, b):
    global p
    global h
    global graph_directives

    # Case for a -> a (2)
    if a == 'premise':
        graph_directives.append(a + str(p + 1) + ' [label = "premise"]')
        graph_directives.append('%s -> %s [ label=%s ]' % (a + str(p), a + str(p + 1), quote(b)))
        p += 1

    elif a == 'hypothesis':
        graph_directives.append(a + str(h + 1) + ' [label = "hypothesis"]')
        graph_directives.append('%s -> %s [ label=%s ]' % (a + str(h), a + str(h + 1), quote(b)))
        h += 1


def add_graph_directives_input_dependent(a, b):
    global p
    global h
    global graph_directives

    if a == 'premise':
        graph_directives.append('%s -> %s [ style=dashed ]' % (a + str(p), quote(b)))
    elif a == 'hypothesis':
        graph_directives.append('%s -> %s [ style=dashed ]' % (a + str(h), quote(b)))
    else:
        graph_directives.append('%s -> %s [ style=dashed ]' % (quote(a), quote(b)))


if __name__ == '__main__':
    with open(sys.argv[1], 'r') as stream:
        try:
            yml = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    graph_directives = []
    p = 0
    h = 0

    # Preliminary title, premise, and hypothesis declarations
    graph_directives.append('label="%s"' % ('Graphical Visualization of \''+sys.argv[1]+'\''))
    graph_directives.append('premise'+str(p)+' [label = "premise"]')
    graph_directives.append('hypothesis'+str(h)+' [label = "hypothesis"]')

    for key, val in yml.items():
        if key == 'model':
            for k, v in val.items():
                for i in v:
                    # Account for cases with neither 'input' nor 'output' key
                    if 'input' not in i:
                        if 'output' not in i:
                            continue

                    # Account for cases without an 'output' key
                    elif 'output' not in i:
                        add_graph_directives_input_module(i['input'], i['module'])

                    # Account for cases with multiple input
                    elif len(i['input']) == 2 or len(i['input']) == 4:
                        j = 0
                        while j < len(i['input']):
                            add_graph_directives_input_output(i['input'][j], i['output'])
                            j += 1

                    # Default case
                    else:
                        add_graph_directives_input_output(i['input'], i['output'])

                    # Account for case with dependencies
                    if 'dependent' in i:
                        add_graph_directives_input_dependent(i['dependent'], i['output'])

    tmpl = """digraph {
    node [shape=rectangle];
    rankdir=LR;
    splines=polyline;
    labelloc="t";
    fontsize=20;
    %s
    }
        """
    gv = tmpl % ";\n    ".join(graph_directives)

    print(gv.encode('utf-8'))