import os
import shutil

from .runner import run


def generate(executable, api_definition, output, destination=None):
    ret_code = run(executable, api_definition, output, 'python')

    if ret_code != 0:
        return ret_code

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
