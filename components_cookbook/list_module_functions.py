# https://stackoverflow.com/questions/139180/how-to-list-all-functions-in-a-python-module
import ast
import sys

def functions_from_ast(body):
    return (f for f in body if isinstance(f, ast.FunctionDef))

def parse_ast(filename):
    with open(filename, "rt") as file:
        return ast.parse(file.read(), filename=filename)

def functions_from_module(mod):
    tree = parse_ast(mod.__file__)
    return functions_from_ast(tree.body)

def print_module(mod):
    print(mod.__file__)
    for func in functions_from_module(mod):
        print(" %s" % func.name)

if __name__ == "__main__":
    for module_name in sys.argv[1:]:
        mod = __import__(module_name)
        print_module(mod)
