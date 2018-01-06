#!/usr/bin/python
# vim: fileencoding=utf-8


'''
Translate YAML written text to graphviz dot

Author: Benedict Printz
Usage: python YAMLtoDOT.py input.yaml > output.gv
'''

import yaml

def quote(s):
    return u'"{}"'.format(s.replace(u'"', u'\\"'))

def edge_str(a, b, c):
    global p
    global h
    global edges

    # Case for a -> b
    if c == 1:
        # If a == b
        if a == b:
            # If a is 'premise'
            if a == 'premise':
                edges.append(a+str(p+1)+' [label = "premise"]')
                edges.append('%s -> %s' % (a+str(p),a+str(p+1)))
                p += 1

            elif a == 'hypothesis':
                edges.append(a+str(h+1)+' [label = "hypothesis"]')
                edges.append('%s -> %s' % (a+str(h),a+str(h+1)))
                h += 1
        else:
            if a == 'premise':
                edges.append('%s -> %s' % (a+str(p), quote(b)))
            elif b == 'premise':
                edges.append('%s -> %s' % (quote(a), b + str(p)))
            elif a == 'hypothesis':
                edges.append('%s -> %s' % (a + str(h), quote(b)))
            elif b == 'hypothesis':
                edges.append('%s -> %s' % (quote(a), b + str(h)))
            else:
                edges.append('%s -> %s' % (quote(a), quote(b)))

    # Case for a -> a
    elif c == 2:
        if a == 'premise':
            edges.append(a + str(p + 1) + ' [label = "premise"]')
            edges.append('%s -> %s [ label=%s ]' % (a + str(p), a + str(p + 1), quote(b)))
            p += 1

        elif a == 'hypothesis':
            edges.append(a + str(h + 1) + ' [label = "hypothesis"]')
            edges.append('%s -> %s [ label=%s ]' % (a + str(h), a + str(h + 1), quote(b)))
            h += 1


if __name__ == '__main__':
    with open("text.yaml", 'r') as stream:
        try:
            yml = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    edges = []
    p = 0
    h = 0

    # Preliminary premise and hypothesis declarations
    edges.append('premise'+str(p)+' [label = "premise"]')
    edges.append('hypothesis'+str(h)+' [label = "hypothesis"]')

    for key, val in yml.items():
        if key == 'model':
            for k, v in val.items():
                for i in v:
                    # Account for cases with neither 'input' or 'output' key
                    if 'input' not in i:
                        if 'output' not in i:
                            continue

                    # Account for cases without an 'output' key
                    elif 'output' not in i:
                        edge_str(i['input'], i['module'], 2)

                    # Account for cases with multiple input
                    elif len(i['input']) == 2 or len(i['input']) == 4:
                        j = 0
                        while j < len(i['input']):
                            edge_str(i['input'][j], i['output'], 1)
                            j += 1

                    # Default case
                    else:
                        edge_str(i['input'], i['output'], 1)


    tmpl = """digraph {
    node [shape=rectangle];
    rankdir=LR;
    splines=false;
        %s
    }
        """
    gv = tmpl % ";\n    ".join(edges)

    print(gv.encode('utf-8'))