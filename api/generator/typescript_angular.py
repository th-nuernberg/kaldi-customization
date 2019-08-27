from .runner import run


def generate(executable, api_definition, output):
    return run(executable, api_definition, output, 'typescript-angular', props={
        'modelPropertyNaming': 'snake_case'  # don't use camelCase (default for TypeScript)
    })
