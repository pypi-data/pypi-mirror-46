import base64

from IPython.display                 import display_html
from osbot_aws.apis.Lambda           import Lambda
from pbx_gs_python_utils.utils.Files import Files
from osbot_jupyter.utils.Trace_Call  import Trace_Call


class Jp_Helper:

    @staticmethod
    def show_png(png_data):
        html = '<img style="border:1px solid black" align="left" src="data:image/png;base64,{}"/>'.format(png_data)
        display_html(html, raw=True)

    @staticmethod
    def graph(graph_name):
        print('creating plantuml graph for: {0}'.format(graph_name))
        from osbot_jira.api.graph.Lambda_Graph import Lambda_Graph
        png_data = Lambda_Graph().get_graph_png___by_name(graph_name).get('png_base64')
        Jp_Helper.show_png(png_data)

    @staticmethod
    def mindmap(graph_name):
        print('creating mindmap graph for: {0}'.format(graph_name))
        payload = {"params": ['go_js', graph_name, 'mindmap']}
        png_data = Lambda('osbot_browser.lambdas.lambda_browser').invoke(payload)
        Jp_Helper.show_png(png_data)

    @staticmethod
    def viva_graph(graph_name):
        print('creating viva graph for: {0}'.format(graph_name))
        payload = {"params": ['viva_graph', graph_name, 'default']}
        png_data = Lambda('osbot_browser.lambdas.lambda_browser').invoke(payload)
        Jp_Helper.show_png(png_data)

    @staticmethod
    def screenshot(url):
        print('taking screenshot of: {0}'.format(url))
        payload = {"params": ['screenshot', url]}
        png_data = Lambda('osbot_browser.lambdas.lambda_browser').invoke(payload)
        Jp_Helper.show_png(png_data)

    @staticmethod
    def screenshot_save(url,target_file):
        print('taking screenshot of: {0}'.format(url))
        payload = {"params": ['screenshot', url]}
        png_data = Lambda('osbot_browser.lambdas.lambda_browser').invoke(payload)
        #Files.write(target_file,png_data)
        print('png_data with size {0} saved to {1}'.format(len(png_data),target_file))

    @staticmethod
    def show_png_file_base_64(png_file):
        png_data = open(png_file, 'r').read()
        Jp_Helper.show_png(png_data)

    @staticmethod
    def show_png_file_binary(png_file):
        #png_data = base64.encodestring(open(png_file, 'rb').read())
        png_data = base64.b64encode(open(png_file, 'rb').read()).decode('utf-8')
        #print(png_data)
        Jp_Helper.show_png(png_data)

    @staticmethod
    def trace_method(method,*params,**kwargs):
        trace_call = Trace_Call().invoke_method(method, *params,**kwargs)
        if trace_call.get('status') == 'ok':
            Jp_Helper.show_png_file_binary(trace_call.get('img_file'))

        return trace_call
