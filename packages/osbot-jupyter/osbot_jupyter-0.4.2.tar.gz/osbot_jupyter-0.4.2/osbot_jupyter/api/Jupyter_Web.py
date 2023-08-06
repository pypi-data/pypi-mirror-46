import base64

from osbot_aws.apis.Lambda import load_dependency

class Jupyter_Web:

    def __init__(self, token=None,server=None, headless=True):
        self.headless       = headless
        #self.server         = {'schema':'http', 'ip':  '127.0.0.1' , 'port' : 8888 }
        self.token          = token
        self.tmp_screenshot = '/tmp/jupyter_screenshot.png'
        self.server         = server
        self._browser       = None  # API_Browser(headless=headless)

    def browser(self):
        if self._browser is None:
            from osbot_browser.browser.Browser_Lamdba_Helper import Browser_Lamdba_Helper
            browser_helper  = Browser_Lamdba_Helper(headless=self.headless).setup()
            self._browser    = browser_helper.api_browser
        return self._browser

    def browser_width(self,width):
        if width:
            self.browser().sync__browser_width(width=width)
        return self

    def current_page(self):
        return self.browser().sync__url()

    def login(self):
        return self.open('?token={0}'.format(self.token))

    def logout(self):
        return self.open('logout')

    def open(self, path=None):
        if path:
            if path and path.startswith('http'):
                url = path
            else:
                url = self.resolve_url(path)
            self.browser().sync__open(url)
        return self

    def open_notebook(self,notebook_path):
        return self.open(self.resolve_url_notebook_preview(notebook_path))

    def open_notebook_edit(self, notebook_path):
        return self.open('notebooks/{0}.ipynb'.format(notebook_path))

    def open_tree(self):
        return self.open('tree')

    def screenshot(self,url=None):
        self.browser().sync__screenshot(url=url,full_page=True, file_screenshot=self.tmp_screenshot)
        return self.tmp_screenshot

    def screenshot_base64(self,url=None):
        return self.browser().sync__screenshot_base64(full_page=True,url=url)


    def resolve_url(self,path=None):
        #if self._server is None:
        #    self._server = "{0}://{1}:{2}".format(self.server.get('schema'), self.server.get('ip'), self.server.get('port'))

        if   path is None or len(path) == 0: path = '/'
        elif path[0] != '/'                : path = '/' + path

        return "{0}{1}".format(self.server, path)

    def resolve_url_notebook_preview(self, notebook_path):
        if '.ipynb' not in notebook_path:
            notebook_path += '.ipynb'
        return 'nbconvert/html/{0}?download=false'.format(notebook_path)

    def ui_hide_input_boxes(self):
        self.browser().sync__js_execute("$('div.input').hide()")
        return self
    def url(self):
        return self.browser().sync__url()

    def set_url  (self, value): self._server   = value; return self
    def set_token(self, value): self.token  = value; return self