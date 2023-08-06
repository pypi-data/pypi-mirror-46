from IPython.core.display import display, HTML, Javascript
from IPython.lib.display import IFrame
from IPython.display import display, Markdown
from ipywidgets import widgets, HBox, Label, VBox, Layout
from ipywidgets import HTML as Html_Widget
from osbot_gsuite.apis.GSheets import GSheets
from osbot_gsuite.apis.sheets.API_Jira_Sheets_Create import API_Jira_Sheets_Create
from osbot_gsuite.apis.sheets.API_Jira_Sheets_Sync import API_Jira_Sheets_Sync
from osbot_jira.api.jira_server.API_Jira_Rest import API_Jira_Rest
from pbx_gs_python_utils.utils.Misc import Misc


class Jp_GSheets():

    def __init__(self, file_ids=None, sheet_name=None):
        self.gsuite_secret_id = 'gsuite_gsbot_user'
        self.file_id          = Misc.array_get(file_ids,0)
        self.other_files      = file_ids
        self.sheet_name       = sheet_name
        self.gsheets          = GSheets               (self.gsuite_secret_id)
        self.gsheets_sync     = API_Jira_Sheets_Sync  (self.file_id,self.gsuite_secret_id)
        self.jira_api_rest    = API_Jira_Rest()
        self.gsheets_create   = API_Jira_Sheets_Create(self.file_id)

    def current_file_id(self):
        print(self.file_id)

    def set_file_id(self,value):
        self.file_id = value
        return self

    def set_other_files(self,other_files):
        self.other_files = other_files

    def metadata(self):
        return self.gsheets.sheets_metadata(self.file_id)

    def values(self):
        return self.gsheets.get_values_as_objects(self.file_id, self.sheet_name)

    def url(self):
        #return '/{0}'.format(self.file_id)
        return self.gsheets.gdrive.file_weblink(self.file_id)

    def load_data(self):
        print('loading data for sheet: {0}'.format(self.file_id))
        self.gsheets_sync.load_data_from_jira()

    def sync_data(self):
        print('syncing data for sheet: {0}'.format(self.file_id))
        self.gsheets_sync.sync_sheet()

    #sdef set_file_id(self, file_id):


    def ui(self,height=400):
        self.ui_add_buttons()
        self.ui_add_iframe(height=height)


    def ui_add_iframe(self,width='100%', height=400):
        iframe = IFrame(self.url(), width=width, height=height)
        display(HTML("<style>.container { width:98% !important; }</style>"))
        display(iframe)

    def ui_load__file_id(self):
        code = "$('iframe').eq(0).attr('src', '{0}')".format(self.url())
        display(Javascript(code))

    def ui_add_buttons(self):
        def add_button(button_text,method, button_style = 'success'):
            button = widgets.Button(description=button_text, button_style=button_style)
            button.on_click(lambda x: method())
            return button
            #display(button)
            # button_load_data = widgets.Button(description="Load Data")
            # button_load_data.on_click(lambda x : self.load_data())
            #
            # button_sync_data = widgets.Button(description="Sync Data")
            # button_sync_data.on_click(lambda x: self.sync_data())
            #
            # display(button_load_data)
            # display(button_sync_data)

        #sheet_link    = self.url()
        #link_to_sheet = Html_Widget("on this <a href='{0}' target='blank'>Google Sheet</a>".format(sheet_link));

        def on_dropdown_change(value):
            text_file_id.value = value.new
            self.ui_load__file_id()

        text_file_id = widgets.Text(value=self.file_id, description='Current file id')
        text_file_id.observe(lambda value: self.set_file_id(value.new),'value')
        #self.other_files.insert(0,self.file_id)
        list_file_ids = widgets.Dropdown(options = self.other_files, description='Other file ids')
        list_file_ids.observe(on_dropdown_change ,'value')
        items = []
        items.append(add_button("Open file", self.ui_load__file_id, button_style='info'))
        items.append(add_button("Load Data", self.load_data))
        items.append(add_button("Sync Data", self.sync_data))

        display(VBox([ HBox([text_file_id,list_file_ids]),
                       HBox(items)         ]))

        display(Javascript("$('.widget-text').width(500);$('.widget-dropdown').width(500)"))

    def ui_show_link(self):
        html = "Here is the <a href='{0}' target='_blank'>link</a> for the sheet with id <i>{1}</i>".format(self.url(), self.file_id)

        display(HTML(html))
        return self

#%autoreload
#from osbot_jupyter.api_notebook.Jp_Helper import Jp_Helper
##Jp_Helper.trace_method(sheets.gsheets_sync.load_data_from_jira)



#sheets.gsheets.set_values(file_id, 'new sheet', [['aaa','123']])