import json
from time import sleep

from IPython.display import display, HTML, Javascript
from pbx_gs_python_utils.utils.Misc import Misc


class Jp_Vis_Js:
    def __init__(self):
        self.require_js = {"paths": {"vis": "https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min" }}
        self.div_id     = Misc.random_string_and_numbers(prefix='network_')
        #self.test = 42
        self.setup_code = """
                                %autoreloadF
    
                                from osbot_jupyter.api_js.Jp_Vis_Js import Jp_Vis_Js
                                jp_vis = Jp_Vis_Js()
                                #jp_vis.js_invoke('element.text(vis)')
                                #jp_vis.test_vis()
                          """
    #def invoke(js_code):

    def add_vis_div(self):
        display(HTML("<div id='{0}'></div>".format(self.div_id)))
        #sleep(0.1)

    def js_invoke(self, js_code):
        display(Javascript(js_code))

    def js_vis_invoke(self, code):
        js_code = "requirejs.config({0});\n".format(json.dumps(self.require_js)) + \
                  "require(['vis'], function(vis) {\n\n" +  code + "\n\n})";
        display(Javascript(js_code))
        return


    def test_vis(self):
        nodes = [{"id": 1, "label": '1st label'},
                 {"id": 2, "label": '2nd label'}]
        edges = [{"from": 1, "to": 2, "arrows": 'to'}]
        options = {"height": "200px", "nodes": {"shape": "box", "color": "lightgreen"}}
        self.show_vis(nodes, edges,options)

    def show_vis(self,nodes, edges, options):
        js_code = """            
                        var container = document.getElementById('{0}');
                        var data= {{
                            nodes: {1},
                            edges: {2}
                        }};
                        var options = {3}         
                        window['_{0}'] = new vis.Network(container, data, options);    
                  """.format(self.div_id, json.dumps(nodes), json.dumps(edges),options)
        self.add_vis_div()
        self.js_vis_invoke(js_code)


    # display(Javascript(data=js_code,lib=['https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js']))
    # #text = Misc.random_string_and_numbers()
    #     html =  """ <h2 id='aaa'> this is html: {0}</h2> ...
    #                 <script>
    #                     $('h2#aaa').text(window.text)
    #                 </script>
    #             """

    # IPython.notebook.kernel.execute("a=42")

    def simple_graph(self):
        self.test_vis()
        self.a = 23


    # tests

    def simple_graph_test(self):
        from time import sleep
        sleep(0.2)
        self.js_invoke('element.text(_{0}.body.data.nodes)'.format(self.div_id))
        return
        assert self.a == 23
        for i in range(10,20):
            node = json.dumps({ "id": str(i), "label" : str(i) })
            edge = json.dumps({"from" : "1", "to": str(i)})
            self.js_invoke('_{0}.body.data.nodes.add({1})'.format(self.div_id, node))
            self.js_invoke('_{0}.body.data.edges.add({1})'.format(self.div_id, edge))


