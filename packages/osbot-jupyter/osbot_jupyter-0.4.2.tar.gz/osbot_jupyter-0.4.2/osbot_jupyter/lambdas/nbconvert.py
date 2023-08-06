from osbot_aws.apis.Lambda import load_dependency
from pbx_gs_python_utils.utils.Process import Process


#Not working: throwing issue: Cannot import name 'constants'",
def run(event, context):
    load_dependency('jupyter')
    #result = Process.run('jupyter')

    from runipy.notebook_runner import NotebookRunner
    from IPython.nbformat.current import read

    notebook = read(open("MyNotebook.ipynb"), 'json')
    return notebook
