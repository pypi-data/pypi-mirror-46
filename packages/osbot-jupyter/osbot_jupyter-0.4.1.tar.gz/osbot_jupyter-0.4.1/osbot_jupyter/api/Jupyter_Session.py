from osbot_jupyter.api.Jupyter_API import Jupyter_API


class Jupyter_Session(Jupyter_API):

    def __init__(self, server=None, token=None, session_id=None):
        self.session_id = session_id
        super().__init__(server,token)

    def get(self, notebook_path):
        path = 'sessions'
        data = { 'path': notebook_path  ,
                 'type': 'python3' }
        return self.http_post(path, data)

    def set_to_notebook(self, notebook_path):
        self.session_id = self.get(notebook_path).get('id')
        return self

    def delete(self):
        if self.exists() is False: return False
        self.http_delete('sessions/{0}'.format(self.session_id))
        return self.exists() is False

    def delete_all(self):
        for session_id in self.sessions_ids():
            self.delete(session_id)
        return self

    def exists(self):
        return self.info() is not None

    def info(self):
        return self.http_get('sessions/{0}'.format(self.session_id))

    def rename(self, name):
        path = 'sessions/{0}'.format(self.session_id)
        data = { 'name': name}

        return self.http_patch(path, data)

    def sessions(self):
        items = {}
        for session in self.http_get('sessions'):
            items[session.get('id')] = session
        return items

    def sessions_ids(self):
        return list(set(self.sessions()))

    def set_session_id(self,value):
        self.session_id = value
        return self

