from osbot_jupyter.api.Jupyter_API import Jupyter_API


class Jupyter_API_Actions(Jupyter_API):
    def __init__(self,server, token):
        #self.api = Jupyter_API()
        super().__init__(server, token)

    def create_notebook(self,notebook_name):
        notebook_name += '.ipynb'
        code = """
        import nbformat as nbf
        nb = nbf.v4.new_notebook()
        nbf.write(nb, '{0}')
        """.format(notebook_name)
        result = self.kernel_code_execute(code)
        return result

