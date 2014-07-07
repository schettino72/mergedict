DOIT_CONFIG = {'default_tasks': []}


def task_manifest():
    """create manifest file for distutils """

    cmd = "git ls-tree --name-only -r HEAD > MANIFEST"
    return {'actions': [cmd]}


def task_pypi():
    """upload package to pypi"""
    return {
        'actions': ["python setup.py sdist upload"],
        'task_dep': ['manifest'],
        }
