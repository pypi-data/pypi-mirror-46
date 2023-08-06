import json
import textwrap
import uuid
import datetime

from pbx_gs_python_utils.utils.Dev import Dev
from websocket                      import create_connection
from osbot_jupyter.api.Jupyter_API  import Jupyter_API


class Jupyter_Kernel(Jupyter_API):

    def __init__(self, server=None, token=None, kernel_id=None):
        self.kernel_id = kernel_id
        super().__init__(server,token)

    def delete(self):
        if self.exists() is False: return False
        self.http_delete('kernels/{0}'.format(self.kernel_id))
        return self.exists() is False

    def delete_all(self):
        deleted = []
        for kernel_id in self.kernels():
            self.kernel_id = kernel_id
            self.delete()
            deleted.append(kernel_id)
        self.kernel_id = None
        return

    def exists(self):
        return self.info() is not None

    def info(self):
        return self.http_get('kernels/{0}'.format(self.kernel_id))

    def kernels(self):
        items = {}
        for kernel in self.http_get('kernels'):
            items[kernel.get('id')] = kernel
        return items

    def kernels_ids(self):
        return list(set(self.kernels()))

    def kernels_specs(self):
        return self.http_get('kernelspecs').get('kernelspecs')

    def new(self,name=None):
        path = 'kernels'
        data = { "name": name}
        info = self.http_post(path, data)
        self.kernel_id = info.get('id')
        return self

    def set_kernel_id(self,value):
        self.kernel_id = value
        return self


    def execute_get_connection(self,ip, port):
        headers = {'Authorization': 'Token {0}'.format(self.token)}
        url     = "ws://{0}:{1}/api/kernels/{2}/channels".format(ip, port,self.kernel_id)

        #import ssl
        #sslopt = {"cert_reqs": ssl.CERT_NONE}
        return create_connection(url, header=headers)#,sslopt=sslopt)

    def execute_request(self, code):
        msg_type = 'execute_request';
        content = {'code': code, 'silent': False}

        hdr = {'msg_id'  : uuid.uuid1().hex                     ,
               'username': 'test'                               ,
               'session' : uuid.uuid1().hex                     ,
               'data'    : datetime.datetime.now().isoformat()  ,
               'msg_type': msg_type                             ,
               'version' : '5.0'
               }
        msg = {'header'  : hdr, 'parent_header': hdr            ,
               'channel' : 'shell'                              ,
               'metadata': {}                                   ,
               'content' : content                              }
        return json.dumps(msg)


    def execute(self, code, ip = 'localhost', port=8888):
        code    = textwrap.dedent(code)
        #ip      = 'localhost'
        #port    = 8888
        ws      = self.execute_get_connection(ip, port)
        payload = self.execute_request(code)
        result  = {
                    'output'        : None ,
                    'display_data'  : []   ,
                    'error'         : []   ,
                    'stream'        : []   ,
                    'stdout'        : []   ,
                    'unhandled'     : []
                  }

        ws.send(payload)

        while True:                                 # I don't like 'while True' but it seems to be the only option
            response = json.loads(ws.recv())
            content  = response.get("content")
            msg_type = response.get("msg_type")

            #Dev.pprint(response)

            if msg_type == 'execute_input' :
                result['input'] = content.get('code')

            elif msg_type == 'execute_result':
                result['output'] = content.get('data').get('text/plain')

            elif msg_type == 'stream':
                if content.get('name') == 'stdout':
                    result['stdout'].append(content.get('text'))
                else:
                    result['stream'].append(content)

            elif msg_type == 'display_data':
                result['display_data'].append(content)

            elif msg_type == 'error':
                result['error' ].append(content)

            elif msg_type == "execute_reply" :
                result['status'] = content.get('status')
                if result['status'] == 'error':
                    result['error'].append(content)
                break
            elif msg_type == 'status':
                pass                        # don't capture these
            else:
                result['unhandled'] = {'msg_type': msg_type, 'content': content}
                #Dev.pprint(response)        # log the msg_types not currently handled
        ws.close()

        return result

    def first_with_name(self,name):
        for kernel in self.kernels().values():
            if kernel.get('name') == name:
                self.kernel_id = kernel.get('id')
                return self
        return None

    def first_or_new(self, name='python3'):
        first = self.first_with_name(name)
        if first:
            return first
        return self.new(name)

    @staticmethod
    def decode_error(data):
        if data and data.get('error'):
            import re
            lines = []
            ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
            for trackback in data.get('error')[0].get('traceback'):
                lines.append(ansi_escape.sub('', trackback))

            return '\n'.join(lines)
        return None

    # def execute(self,code_to_execute):
    #
    #     kernel_id = list(set(self.kernels())).pop()
    #     headers   = {'Authorization': 'Token {0}'.format(self.token)}
    #     url       = "ws://localhost:8888/api/kernels/{0}/channels".format(self.kernel_id)
    #     ws        = create_connection(url, header=headers)
    #
    #     def send_execute_request(code):
    #         msg_type = 'execute_request';
    #         content = {'code': code, 'silent': False}
    #
    #
    #         hdr = {'msg_id': uuid.uuid1().hex,
    #                'username': 'test',
    #                'session': uuid.uuid1().hex,
    #                'data': datetime.datetime.now().isoformat(),
    #                'msg_type': msg_type,
    #                'version': '5.0'}
    #         msg = {'header': hdr, 'parent_header': hdr,
    #                'metadata': {},
    #                'content': content}
    #         return msg
    #
    #     ws.send(json.dumps(send_execute_request(code_to_execute)))
    #     messages = []
    #     msg_type = ''
    #     while msg_type != "execute_reply":
    #         rsp         = json.loads(ws.recv())
    #         content     = rsp.get("content")
    #         msg_type    = rsp.get("msg_type")
    #         messages.append({'msg_type': msg_type, 'content': content})
    #     ws.close()
    #
    #     return messages