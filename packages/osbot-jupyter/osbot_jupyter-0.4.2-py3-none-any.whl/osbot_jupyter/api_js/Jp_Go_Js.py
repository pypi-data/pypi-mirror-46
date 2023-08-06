import json
from time import sleep
from IPython.display import display, HTML, Javascript,IFrame
from pbx_gs_python_utils.utils.Misc import Misc


class Jp_Go_Js:

    def __init__(self, width="100%", height=800):
        self.frame_id   = Misc.random_string_and_numbers(prefix='go_view_')
        self.frame_id   = 'go_view_12345'
        self.src        = '/view/html/go-js/incremental-tree.html'
        self.nodes      = []                                          # keep track of nodes added
        self.edges      = []
        self.link_types = []
        self.width      = width
        self.height     = height
        self.verbose    = False
        pass

    def add_iframe(self):
        iframe_code = "<iframe id='{0}' src='{1}' width='{2}' height='{3}'></iframe>".format(
                        self.frame_id, self.src, self.width, self.height)
        display(HTML(iframe_code))
        display(Javascript("$('.output_stderr').hide()"))

        #display(IFrame(src=self.src, width=800, height=300,id=self.frame_id, abc="aaaaa" ))
        return self

    def add_event_listerner(self):
        js_code = """
                        if(window.message_listener) {
                            console.log('removing event listener')
                            window.removeEventListener('message', window.message_listener)
                        }
                        console.log('adding event listener')
                        window.message_listener = function(event) {
                         
                            console.log('message: ' + JSON.stringify(event.data))
                            if (event.data.action == 'expand') {
                                Jupyter.notebook.select_next().select_next()        
                                var nb = Jupyter.notebook.insert_cell_below()
                                nb.select()
                                Jupyter.notebook.get_selected_cell().unselect()                                
                                nb.set_text("jp_go_js.add_nodes_from_issue('"+event.data.key+"')")
                                nb.execute()     
                                Jupyter.notebook.delete_cell()      
                                console.log('cell created and deleted')                 
                              }
                          }
                            
                        window.addEventListener('message', window.message_listener)
                  """
        display(Javascript(js_code))
        return self

    def invoke_method(self, js_method, params=None):
        data = json.dumps({'method': js_method, 'params': params})

        js_code = "{0}.contentWindow.iframe.contentWindow.postMessage({1}, '*')".format(self.frame_id, data)
        #print(self.frame_id)s
        #print(js_code)
        display(Javascript(js_code))

    def clear_diagram(self):
        self.nodes = []
        self.edges = []
        self.invoke_method('clear_diagram')
        return self

    def add_node(self,key, label=None, color=None):
        if key in self.nodes:                                   # don't add duplicate nodes
            print('skipped node', key)
            return self
        if self.verbose:
            print('adding node', key)
        if label is None: label = key
        if color is None: color = '#E1F5FE'
        node = {'key': key, 'label': label, 'color': color ,'font': '8pt'}    #'rootdistance':2}

        self.invoke_method('add_node', node)
        self.nodes.append(key)
        return self


    def add_link(self, from_key,to_key,label=None):
        edge = (from_key,to_key,label)
        if edge in self.edges:
            print('skipped edge', edge)
            return self
        if self.verbose:
            print('adding edge', from_key,to_key,label)
        self.invoke_method('add_link', {'from': from_key, 'to': to_key, 'text':label})
        self.edges.append(edge)
        return self

    def expand_all  (self): self.invoke_method('expand_all'); return self
    def collapse_all(self): self.invoke_method('collapse_all'); return self

    def expand_node(self,key):
        self.invoke_method('expand_node', key)
        return self

    def zoom_to_fit(self):
        self.invoke_method('zoom_to_fit')
        #jp_go_js.invoke_method('add_node', {'key': 'RISK-1', 'parent': 'RISK-12'})
        #jp_go_js.invoke_method('add_node', {'key': 'RISK-2', 'parent': 'RISK-12'})
        #jp_go_js.invoke_method('add_node', {'key': 'RISK-3', 'parent': 'RISK-12'})
        #jp_go_js.invoke_method('expand_node', 'RISK-12')

    def wait(self,seconds):
        sleep(seconds)
        return self

    def test_123(self):
        print('abc')



    ## helper issue methods

    def add_nodes_from_issue(self, issue_key):

        self.add_node(issue_key)  # .expand_node(issue_key)

        from osbot_jira.api.API_Issues import API_Issues
        api_issues =  API_Issues()
        issue = api_issues.issue(issue_key)
        if issue is None:
            print('no data received for key: {0}'.format(issue_key))
            return self

        links = issue.get('Issue Links')
        if links:
            available_links     = "{0}".format('\n'.join(list(set(links))))
            available_links_key = "links_for_{0}".format(issue_key)
            self.add_node(available_links_key,available_links,color='#C0C0C0')
            self.add_link(issue_key, available_links_key)

            #print('handling {0} with {1} links'.format(issue_key, len(links)))
            for link_type,values in links.items():
                if (self.link_types is not []) and (link_type not in self.link_types):
                    #print('skipping links')
                    continue
                link_type_key = '{0}::{1}'.format(link_type, issue_key)
                self.add_node(link_type_key, link_type, color='yellow')
                self.add_link(issue_key, link_type_key)
                if values:
                    for link_key in values:
                        link_issue = api_issues.issue(link_key)
                        summary    = "{0} \n{1}".format(link_issue.get('Summary'),link_key)
                        self.add_node(link_key,summary)
                        self.add_link(link_type_key,link_key, )
        else:
            print('no links for {0}'.format(issue_key))

        # usefull JS queries

    # myDiagram.model.addNodeData({'key':'RISK-12'})
    # node = myDiagram.findNodeForKey("RISK-12");
    # node.diagram.commandHandler.expandTree(node)
    # node.diagram.commandHandler.collapseTree()


    # window.addEventListener('message', function(event) {
    #         console.log('message from child....: ' + JSON.stringify(event.data))
    # nb = Jupyter.notebook.insert_cell_below()
    # nb.set_text("jp_go_js.test_123('aaa')").execute()
    # nb.execute()
    #     })

    # %%javascript
    #
    # window.addEventListener('message', function(event) {
    #         console.log('message from child....: ' + JSON.stringify(event.data))
    # var nb = Jupyter.notebook.insert_cell_below()
    # nb.set_text("jp_go_js.add_nodes_from_issue('"+event.data.key+"')")
    # nb.execute()
    #     //console.log(Jupyter.notebook)
    #     //console.log(nb)
    #     })