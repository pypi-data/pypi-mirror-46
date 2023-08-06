from osbot_aws.apis.Lambda import load_dependency


def run(event, context):
    load_dependency('requests')
    from osbot_jupyter.api.Live_Notebook import Live_Notebook

    short_id = event.get('short_id')
    path     = event.get('path')
    width    = event.get('width')
    notebook = Live_Notebook()

    notebook.set_build_from_short_id(short_id)

    return notebook.screenshot(path=path,width=width)
