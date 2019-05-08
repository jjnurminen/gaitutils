# -*- coding: utf-8 -*-
"""
Clean up configparser cfg file:
-remove extra whitespace
-sort sections by headers
-sort variable defs by variable, keeping comment lines for each var
-properly indent list and dict type variables

"""

from __future__ import print_function
import re




def is_comment(s):
    """Match line comment starting with # or ;"""
    p = re.compile('[\s]*[#;].*')
    return bool(p.match(s))        


def is_var_def(s):
    """Match var definition"""
    p = re.compile('[\s]*[\S]+[\s]*=[\s]*[\S]+[\s]*')
    return bool(p.match(s))


def is_list_def(s):
    """Match list or dict definition"""
    p = re.compile('[\s]*[\S]+[\s]*=[\s]*[\[,\{][\S]+[\s]*')
    return bool(p.match(s))


def is_section_header(s):
    """Match section headers of form [string]"""
    p = re.compile('^\[[\w]*\]$')
    return bool(p.match(s))


def not_whitespace(s):
    """Non-whitespace line, should be a continuation of definition"""
    p = re.compile('[\s]*[\S]+')  # match whitespace-only lines
    return bool(p.match(s))



def clean_cfg(lines):
    
    # parse file
    var_comments = list()
    di = dict()
    for li in lines:
        if is_section_header(li):
            this_section = li
            di[this_section] = dict()
        elif is_comment(li):
            var_comments.append(li)
        elif is_var_def(li):
            var = li.split('=')[0]
            di[this_section][var] = dict()
            di[this_section][var]['comments'] = var_comments
            di[this_section][var]['def_lines'] = list()
            di[this_section][var]['def_lines'].append(li)
            var_comments = list()
            # figure out indentation for list-type defs
            if is_list_def(li):
                idnt = max(li.find('['), li.find('{'))
        elif not_whitespace(li):  # continuation line
            if var in di[this_section]:
                if idnt is not None and idnt > 0:  # indent also def continuation lines
                    li = (idnt + 1) * ' ' + li.strip()
                di[this_section][var]['def_lines'].append(li)
            
    # compose output
    for sect in sorted(di.keys()):
        yield ''
        yield sect
        # whether section has var definitions spanning multiple lines
        has_multiline_defs = any(len(di[sect][var]['def_lines']) > 1
                                 for var in di[sect])
        for var in sorted(di[sect].keys()):
            # print comments and definition for this var
            if di[sect][var]['comments']:
                yield '\n'.join(di[sect][var]['comments'])
            def_this = di[sect][var]['def_lines']
            yield '\n'.join(def_this)
            # output extra whitespace for sections that have multiline defs
            if has_multiline_defs:
                yield ''
            
        
with open(r"C:\Users\hus20664877\gaitutils\gaitutils\data\default.cfg", 'r') as f:
    lines = f.read().splitlines()

for li in clean_cfg(lines):
    print(li)

