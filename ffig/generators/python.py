# Generator module for Python 2 and 3.

import generators
import os


def generator(module_name, binding, api_classes, env, output_dir):
    module_dir = os.path.join(output_dir, module_name)
    if not os.path.exists(module_dir):
        os.makedirs(module_dir)

    output_templates = {'__init__.py': '__init__.py.tmpl',
                        'interop_py2.py': 'py2.tmpl',
                        'interop_py3.py': 'py3.tmpl'}

    for filename, template in output_templates.items():
        o = os.path.join(module_dir, filename)
        generators.generate_single_output_file(
            module_name, template, api_classes, env, o)

    return output_templates.keys()


def setup_plugin(context):
    context.register(generator, ['python'])
