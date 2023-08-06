from osbot_aws.apis.Lambda import load_dependency


# NOT working at the moment
# screenshot works ok
# execution returns
# ('[js eval error]: Evaluation failed: ReferenceError: Jupyter is not defined\n'
#  '    at __pyppeteer_evaluation_script__:1:1')
def run(event, context):
    load_dependency('requests')
    from osbot_jupyter.api.Live_Notebook import Live_Notebook

    short_id      = event.get('short_id'     )
    code          = event.get('code'         )
    target        = event.get('target'       )
    keep_contents = event.get('keep_contents')
    notebook      = Live_Notebook(short_id)
    notebook.login()
    return notebook.execute_python(python_code=code, target=target, keep_contents=keep_contents)
    return notebook.jupyter_web().screenshot_base64()
