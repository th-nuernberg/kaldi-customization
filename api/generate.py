#!/usr/bin/python3
import os

from generator.downloader import download_file
from generator.python_flask import generate as generate_server
from generator.python import generate as generate_python_client
from generator.typescript_angular import generate as generate_typescript_client


script_dir = os.path.dirname(os.path.realpath(__file__))
tools_dir = os.path.join(script_dir, 'tools')
out_dir = os.path.join(script_dir, 'out')

tools = {
    'openapi-generator-cli.jar': 'http://central.maven.org/maven2/org/openapitools/openapi-generator-cli/4.0.3/openapi-generator-cli-4.0.3.jar'
}


def update_tools():
    if not os.path.exists(tools_dir):
        os.mkdir(tools_dir)

    for file_name, url in tools.items():
        file_path = os.path.join(tools_dir, file_name)

        if not os.path.exists(file_path):
            download_file(url, file_path)


if __name__ == "__main__":
    update_tools()

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    generator_executable = os.path.join(tools_dir, 'openapi-generator-cli.jar')
    api_definition = os.path.join(script_dir, 'openapi.yaml')

    generate_server(
        generator_executable, api_definition,
        os.path.join(out_dir, 'server'))
    generate_python_client(
        generator_executable, api_definition,
        os.path.join(out_dir, 'python_client'))
    generate_typescript_client(
        generator_executable, api_definition,
        os.path.join(out_dir, 'typescript_client'))
