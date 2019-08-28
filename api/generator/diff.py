import ast
import dictdiffer
import os
import yaml

script_dir = os.path.dirname(os.path.realpath(__file__))
old_dir = os.path.join(script_dir, r'../../server/api/src/openapi_server')
new_dir = os.path.join(script_dir, r'../out/server/openapi_server')


class DiffVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()

        self.functions = {}
        self._function_args = []

    def generic_visit(self, node):
        if isinstance(node, ast.FunctionDef):
            self._function_args = []
            ast.NodeVisitor.generic_visit(self, node.args)
            self.functions[node.name] = self._function_args

        if isinstance(node, ast.arg):
            self._function_args.append(node.arg)


        if isinstance(node, ast.Module):
            # only step down to global scope
            ast.NodeVisitor.generic_visit(self, node)


class OpenAPIDefinition:
    def __init__(self, openapi):
        with open(openapi, 'r') as fp:
            self.d = yaml.safe_load(fp)
            self._tags = set([t['name'] for t in self.d['tags']])

    @property
    def tags(self):
        return self._tags


class Controller:
    def __init__(self, name, openapi, controller):
        self._name = name
        self._openapi = openapi

        with open(controller, 'r') as fp:
            self.code = fp.read()

        self._tree = ast.parse(self.code)

        self._visitor = DiffVisitor()
        self._visitor.visit(self._tree)

        self._operations = set()

        for path in self.openapi['paths'].values():
            for method in path.values():
                if self.name == method['tags'][0]:
                    self._operations.add(method['operationId'])

    @property
    def name(self):
        return self._name

    @property
    def openapi(self):
        return self._openapi.d

    @property
    def functions(self):
        return {k: v for k,v in self._visitor.functions.items() if k in self.operations}

    @property
    def operations(self):
        return self._operations

    @property
    def additional_functions(self):
        return set(self._visitor.functions.keys()) - self.operations


class ControllerComparator:
    def __init__(self, old, new):
        self.old = old
        self.new = new

        self._delta_operations = old.operations - new.operations
        self._delta_functions = dictdiffer.diff(old.functions, new.functions)

    @property
    def delta_operations(self):
        return self._delta_operations

    @property
    def delta_functions(self):
        return self._delta_functions


openapi_old = OpenAPIDefinition(os.path.join(old_dir, r'openapi/openapi.yaml'))
openapi_new = OpenAPIDefinition(os.path.join(new_dir, r'openapi/openapi.yaml'))

# completely added or removed controllers
tags_diff = openapi_old.tags - openapi_new.tags

for tag in tags_diff:
    print('- delete, move or rename the {}_controller.py'.format(tag))

tags_diff = openapi_new.tags - openapi_old.tags

for tag in tags_diff:
    print('+ add, move or rename the {}_controller.py'.format(tag))


for tag in openapi_new.tags:
    if tag in tags_diff:
        # completely new controller, no need to diff
        continue

    cc = ControllerComparator(
        Controller(tag, openapi_old,
                controller=os.path.join(old_dir, r'controllers/{}_controller.py'.format(tag))),
        Controller(tag, openapi_new,
                controller=os.path.join(new_dir, r'controllers/{}_controller.py'.format(tag))))

    print()
    print('#############################')
    print('# diff {}_controller.py'.format(cc.old.name))

    # operation diff
    for operation in cc.delta_operations:

        if operation in cc.old.operations:
            print(' - remove, move or rename required:', operation)
        else:
            print(' + add, move or rename operation:', operation)

    # parameter diff
    for d in cc.delta_functions:
        print(' *', d)
