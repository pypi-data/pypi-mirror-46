import inspect
import importlib
import glob
import os, sys
import importlib.util

project_name = os.getcwd().split('/')[-1]
project_icon = "code" # https://material.io/tools/icons/?style=baseline

code_path = os.path.abspath(sys.argv[1])
package_name = code_path.split('/')[-1]
sys.path.insert(0, os.path.dirname(code_path))

doc_path = os.path.join(os.path.abspath(sys.argv[2]), 'docs')

print(code_path)
print(doc_path)

class fun:
    def __init__(self, op):
        self.op = op
        self.name = op.__name__
        self.doc = inspect.getdoc(op)
        if self.doc is None:
            self.doc = ""
        self.source = inspect.getsource(op)
        self.args = inspect.signature(op)
        self.module = op.__module__

    def write_doc(self, file, clas):
        # name and args of the function
        file.writelines('### **{}**`#!py3 {}`'.format(self.name, self.args))
        file.writelines(' {' + ' #{0} data-toc-label={0} '.format(self.name) + '}\n\n')
        # docstring of the function
        file.writelines(self.doc + '\n')
        # source code
        file.writelines("""\n\n??? info "Source Code" \n\t```py3 linenums="1 1 2" \n""")
        source = self.source.split('"""')
        del source[1] # remove doc
        source = ''.join(source)
        # to handle intendation inside function and class
        source = source.split('\n')
        nb_indent = len(source[0]) - len(source[0].lstrip())
        for i in range(len(source)):
            source[i] = '\t' + source[i][nb_indent:]
        source = '\n'.join(source)
        file.writelines(source)
        file.writelines("""\n\t```""")
        # end of the line
        file.writelines("""\n______\n""")
        return


class meth:
    def __init__(self, op):
        self.op = op
        self.name = op.__name__
        self.doc = inspect.getdoc(op)
        if self.doc is None:
            self.doc = ""
        self.source = inspect.getsource(op)
        self.args = inspect.signature(op)
        self.module = op.__module__

    def write_doc(self, file, clas):
        # name and args of the function
        file.writelines('### *{}*.**{}**`#!py3 {}`'.format(clas.name, self.name, self.args))
        file.writelines(' {' + ' #{0} data-toc-label={0} '.format(self.name) + '}\n\n')
        # docstring of the function
        file.writelines(self.doc + '\n')
        # source code
        file.writelines("""\n\n??? info "Source Code" \n\t```py3 linenums="1 1 2" \n""")
        source = self.source.split('"""')
        del source[1] # remove doc
        source = ''.join(source)
        # to handle intendation inside function and class
        source = source.split('\n')
        nb_indent = len(source[0]) - len(source[0].lstrip())
        for i in range(len(source)):
            source[i] = '\t' + source[i][nb_indent:]
        source = '\n'.join(source)
        file.writelines(source)
        file.writelines("""\n\t```""")
        # end of the line
        file.writelines("""\n______\n""")
        return


class clas:
    def __init__(self, name, op, funs, meths):
        self.name = name
        self.op = op
        self.funs = funs
        self.meths = meths
        if name is not None:
            self.module = op.__module__
            self.doc = inspect.getdoc(op)
            if self.doc is None:
                self.doc = ""
            self.source = inspect.getsource(op)
            self.args = inspect.signature(op)
        else:
            self.module = None
            self.doc = ""
            self.source = None
            self.args = None

    def write_doc(self, file):
        # name and args of the class
        file.writelines('## **{}**`#!py3 class`'.format(self.name))
        file.writelines(' {' + ' #{0} data-toc-label={0} '.format(self.name) + '}\n\n')
        # docstring of the class
        file.writelines(self.doc + '\n')
        # list of methods
        if len(self.meths) > 0:
            file.writelines("\n**class methods:** \n\n")
            for m in self.meths:
                file.writelines(' - [`{0}`](#{0})\n'. format(m.name))

                # list of functions
        if len(self.funs) > 0:
            file.writelines("\n**class functions & static methods:** \n\n")
            for f in self.funs:
                file.writelines(' - [`{0}`](#{0})\n'. format(f.name))

        file.writelines("""\n______\n""")
        return



if not os.path.isdir(doc_path):
    os.makedirs(doc_path)
# Write the index file
if not os.path.isfile(os.path.join(doc_path, "index.md")):
    with open(os.path.join(doc_path, "index.md"), 'w') as md_out:
        md_out.writelines("# Welcome!\n")
        md_out.writelines("Welcome to the documentation of the {} project \n".format(project_name))
        md_out.writelines("Use this file (aka docs/index.md) to describe your project!  \n")
        md_out.writelines("Make it interesting, don't forget that is the first thing people see on your doc\n")

package = importlib.import_module(package_name)
# first list all the classes and then add an empty class for the functions
src = [clas(name, op, [], []) for name, op in inspect.getmembers(package, inspect.isclass)]
src.append(clas(None, package, [], []))

module_set = set()
# list functions for each class
for iclas in src:
    meths = inspect.getmembers(iclas.op, inspect.ismethod)
    for _, meth_op in meths:
        iclas.meths.append(meth(meth_op))

    funs = inspect.getmembers(iclas.op, inspect.isfunction)
    for _, fun_op in funs:
        iclas.funs.append(fun(fun_op))
        module_set.add(iclas.funs[-1].module)

# write in MD files
for module in module_set:
    # open the md file that correspond to the module
    md_file = module.split('.')
    md_file[0] = doc_path
    md_file = '/'.join(md_file) + '.md'
    if os.path.isfile(md_file): # remove the md_file that already exist
        os.remove(md_file)
    if not os.path.isdir(os.path.dirname(md_file)):
        os.makedirs(os.path.dirname(md_file))
    with open(md_file, 'a') as out:
        # name of the module
        out.writelines("# **" + module + '**\n\n')
        # write class doc first
        for c in src:
            if c.module is module:
                c.write_doc(out)
            elif c.module is None:
                out.writelines('\n## \n')

            for m in c.meths:
                if m.module is module:
                    m.write_doc(out, c)

            for f in c.funs:
                if f.module is module:
                    f.write_doc(out, c)


# Write the yaml file
if not os.path.isfile(os.path.join(sys.argv[2], 'mkdocs.yml')):
    with open(os.path.join(sys.argv[2], 'mkdocs.yml'), 'w') as yaml_out:
        yaml_out.writelines("site_name: {}\n".format(project_name))
        yaml_out.writelines("theme:\n")
        yaml_out.writelines("  name: 'material'\n")
        yaml_out.writelines("  logo:\n")
        yaml_out.writelines("     icon: '{}'\n".format(project_icon))
        yaml_out.writelines("nav:\n")
        yaml_out.writelines("  - Home: index.md\n")
        yaml_out.writelines("  - Doc:\n")
        modules = sorted(module_set)
        prev_lvls = []
        for i, k in enumerate(modules):
            lvls = k.split('.')[1:] # remove the src directory
            for ilvl, lvl in enumerate(lvls):
                if ilvl >= len(prev_lvls) or lvl != prev_lvls[ilvl]:
                    if ilvl < len(lvls)-1:
                        yaml_out.writelines("    "*(ilvl+1) + "- {0}:\n".format(lvl))
                    else:
                        path_md = '/'.join(k.split('.')[1:])
                        yaml_out.writelines("    "*(ilvl+1) + "- {}: {}.md\n".format(lvl, path_md))
            prev_lvls = lvls
        yaml_out.writelines("markdown_extensions:\n")
        yaml_out.writelines("    - toc:\n")
        yaml_out.writelines("        toc_depth: 3\n")
        yaml_out.writelines("        permalink: True\n")
        yaml_out.writelines("    - extra\n")
        yaml_out.writelines("    - smarty\n")
        yaml_out.writelines("    - codehilite\n")
        yaml_out.writelines("    - admonition\n")
        yaml_out.writelines("    - pymdownx.details\n")
        yaml_out.writelines("    - pymdownx.superfences\n")
        yaml_out.writelines("    - pymdownx.emoji\n")
        yaml_out.writelines("    - pymdownx.inlinehilite\n")
        yaml_out.writelines("    - pymdownx.magiclink\n")
