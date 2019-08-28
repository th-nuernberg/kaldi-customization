import os
import re
import shutil

from .runner import run

# fix responses with content type "text/plain",
# which are parsed as JSON string instead treated as plain string
fix_plain_text_response_re = re.compile(
    r'(?P<pre>const httpHeaderAccepts: string\[\] = \[\s*\'text\/plain\'\s*\];.*?return this.httpClient.\w+)(?P<template><string>)(?P<mid>\(.*?[^\s])(?P<options>\s*}\s*\))',
    flags=re.MULTILINE | re.DOTALL)
fix_plain_text_response_replacement = r'''\g<pre>\g<mid>,\n                responseType: 'text'\g<options>'''


def fix_service(file_path):
    with open(file_path, 'r') as fp:
        service_source = fp.read()

    fixed_service_source = fix_plain_text_response_re.sub(
        fix_plain_text_response_replacement, service_source)

    if fixed_service_source != service_source:
        with open(file_path, 'w') as fp:
            fp.write(fixed_service_source)

        print('Fixed', file_path)


def generate(executable, api_definition, output, destination=None):
    ret_code = run(executable, api_definition, output, 'typescript-angular', props={
        'modelPropertyNaming': 'snake_case'  # don't use camelCase (default for TypeScript)
    })

    if ret_code != 0:
        return ret_code

    api_output = os.path.join(output, 'api')

    for file_name in os.listdir(api_output):
        file_path = os.path.join(api_output, file_name)
        if file_name.endswith('.service.ts') and os.path.isfile(file_path):
            fix_service(file_path)

    if destination:
        # move generated code to destination
        print('Move {} to {}'.format(output, destination))

        if os.path.exists(destination):
            shutil.rmtree(destination)

        os.mkdir(destination)

        files = os.listdir(output)

        for f in files:
            shutil.move(os.path.join(output, f), destination)

        os.rmdir(output)

    return 0
