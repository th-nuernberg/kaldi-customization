from .runner import run


def generate(executable, api_definition, output):
    return run(executable, api_definition, output, 'python-flask')
