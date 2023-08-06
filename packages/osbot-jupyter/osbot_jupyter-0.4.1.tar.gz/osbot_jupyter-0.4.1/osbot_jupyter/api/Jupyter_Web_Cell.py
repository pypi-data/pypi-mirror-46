import base64
import json
import textwrap
from time import sleep

from pbx_gs_python_utils.utils.Dev import Dev

from osbot_jupyter.api.Jupyter_Web import Jupyter_Web


class Jupyter_Web_Cell(Jupyter_Web):

    def __init__(self, token=None, server=None, headless=True):
        super().__init__(token=token, server=server, headless=headless)

    def execute_html(self, html_code, new_cell=True, delete_after=False):
        python_code = "%%HTML \n{0}".format(html_code)
        return self.execute_python(python_code=python_code,new_cell=new_cell,delete_after=delete_after)

    def execute_javascript(self, javascript_code, new_cell=True, delete_after=False):
        python_code = "%%javascript \n\n{0}".format(javascript_code)
        return self.execute_python(python_code=python_code,new_cell=new_cell,delete_after=delete_after)


    def execute_javascript_with_libs(self, libs, javascript_code, new_cell=True, delete_after=False):
        paths      = {'paths': {} }
        libs_names = []
        var_names  = []
        for lib in libs:
            lib_name        = lib.get('lib_name')
            #var_name        = lib.get('var_name')
            paths['paths'][lib_name] = lib.get('url')
            libs_names.append(lib_name)
            var_names.append(lib_name)
        var_names = ",".join(var_names)
        require_js = "requirejs.config({0})\n".format(json.dumps(paths))
        #libs_names = json.dumps(list(set(libs)))
#         require_js   = """requirejs.config({
#     paths: {
#         "jquery": "https://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min",
#     }
# });

        js_with_libs = "{0}require({1}, function({2}){{ \n\n{3}\n\n  }})".format(require_js, libs_names,var_names,javascript_code)

        python_code = "%%javascript \n\n{0}".format(js_with_libs)
        return self.execute_python(python_code=python_code,new_cell=new_cell,delete_after=delete_after)

    def execute_python(self,python_code, new_cell=True, delete_after=False):
        python_code = textwrap.dedent(python_code)                  # dedent code based on first set of spaces/tabs
        if new_cell:
            self.new();
        self.text(python_code)
        self.execute_cell()
        if delete_after:
            self.delete()
        return self

    def execute(self, code=None):
        if code is None:
            return self.execute_cell()
        return ( self.new_top()
                     .execute_python(code,new_cell=False))

    def js_invoke(self,js_code):
        return self.browser().sync__js_execute(js_code)

    def new_top(self):
        js_code = """Jupyter.notebook.select(0)
                     Jupyter.notebook.insert_cell_above();
                     Jupyter.notebook.select(0);
                     Jupyter.notebook.focus_cell();"""
        self.browser().sync__js_execute(js_code)
        return self

    def new(self):
        js_code = """Jupyter.notebook.insert_cell_below();
                     Jupyter.notebook.select_next(true);
                     Jupyter.notebook.focus_cell();"""
        self.browser().sync__js_execute(js_code)
        return self

    def text_dedent(self, value):
        value = textwrap.dedent(value).strip()
        return self.text(value)

    def text(self,value=None):
        if value is None:
            js_code = "Jupyter.notebook.get_selected_cell().get_text()"
            return self.browser().sync__js_execute(js_code)
        else:
            encoded_text = base64.b64encode(value.encode()).decode()
            js_code = """cell = Jupyter.notebook.get_selected_cell();
                         cell.set_text(atob('{0}'));""".format(encoded_text)
            self.browser().sync__js_execute(js_code)
            return self


    def wait(self,seconds):
        sleep(seconds)
        return self

    # fluent methods
    def clear       (self       ): self.js_invoke("Jupyter.notebook.get_cells().forEach(function (cell) { Jupyter.notebook.delete_cell(cell.id) }) "); return self
    def delete      (self       ): self.js_invoke("Jupyter.notebook.delete_cell()"                                   ); return self
    def execute_cell(self       ): self.js_invoke("Jupyter.notebook.execute_cell()"                                  ); return self
    def select      (self,index ): self.js_invoke("Jupyter.notebook.select({0})".format(index )                      ); return self
    def to_markdown (self       ): self.js_invoke("Jupyter.notebook.cells_to_markdown()"                             ); return self
    def to_code     (self       ): self.js_invoke("Jupyter.notebook.cells_to_code()"                                 ); return self
    def input_hide  (self       ): self.js_invoke("Jupyter.notebook.get_selected_cell().input.hide()"                ); return self
    def input_show  (self       ): self.js_invoke("Jupyter.notebook.get_selected_cell().input.show()"                ); return self
    def output_hide (self       ): self.js_invoke("Jupyter.notebook.get_selected_cell().output_area.element.hide()"  ); return self
    def output_show (self       ): self.js_invoke("Jupyter.notebook.get_selected_cell().output_area.element.show()"  ); return self
    def output_clear(self       ): self.js_invoke("Jupyter.notebook.get_selected_cell().clear_output()"              ); return self
    def unselect    (self       ): self.js_invoke("Jupyter.notebook.get_selected_cell().unselect()"                  ); return self

    # methods that return values
    def input_prompt(self):
        return self.js_invoke("Jupyter.notebook.get_selected_cell().input.find('.input_prompt').text()")

    def output(self):
        return self.js_invoke("Jupyter.notebook.get_selected_cell().output_area.element.find('.output_result').text()");

    def output_html(self):
        return self.js_invoke("Jupyter.notebook.get_selected_cell().output_area.outputs[0].data['text/html']")

    def output_wait_for_data(self, sleep_seconds = 0.5, max_attempts=30):
        for i in range(1,max_attempts):
            if self.input_prompt() != 'In\xa0[*]:':        # the [*] means the kernel is executing the current cells
                return self.output()

            self.wait(sleep_seconds)
        return None