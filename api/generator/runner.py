import subprocess


def run(executable, api_definition, output, generator, props=None):
    cmd = [
        'java', '-jar', executable,
        'generate', '-i', api_definition, '-g', generator, '-o', output]

    if props:
        cmd.append('--additional-properties')
        cmd.append(' '.join(['{}={}'.format(k, v) for k, v in props.items()]))

    return subprocess.call(cmd)
