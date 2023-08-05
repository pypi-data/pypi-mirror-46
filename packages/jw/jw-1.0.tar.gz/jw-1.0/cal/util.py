from os import path


def script_path(*p):
    return path.join(path.dirname(path.abspath(__file__)), *p)
