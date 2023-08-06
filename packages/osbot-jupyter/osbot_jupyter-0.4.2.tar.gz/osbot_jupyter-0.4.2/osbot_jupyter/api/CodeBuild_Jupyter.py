from osbot_aws.apis.CodeBuild import CodeBuild
from osbot_aws.apis.Logs import Logs

class CodeBuild_Jupyter:
    def __init__(self, build_id, build_info=None):
        self.project_name = 'OSBot-Jupyter'
        self.code_build   = CodeBuild(project_name=self.project_name,role_name=None)
        self.build_id     = build_id
        self._build_info  = build_info

    def build_info(self, reload_data=False):
        if reload_data or self._build_info is None:
            self._build_info = self.code_build.build_info(self.build_id)
        return self._build_info

    def build_status(self):
        return self.build_info(reload_data=True).get('buildStatus')

    def build_phase(self):
        return self.build_info(reload_data=True).get('currentPhase')

    def build_log_messages(self):
        build_info = self.build_info()
        group_name = build_info.get('logs').get('groupName')
        stream_name = build_info.get('logs').get('streamName')
        logs = Logs(group_name=group_name, stream_name=stream_name)
        return logs.messages()

    def build_stop(self):
        self.code_build.codebuild.stop_build(id=self.build_id).get('build')
        return self.build_status()

    def get_server_details_from_logs(self):
        def find_in(array, text):
            return [item for item in array if text in item]

        try:
            messages = self.build_log_messages()
            ngrok_url      = find_in(messages, 'name=command_line addr')[0].split('url=')[1].strip()
            jupyter_token  = find_in(messages, 'token=')[0].split('token=')[1].strip()
            return ngrok_url,jupyter_token
        except:
            return None,None

    def url(self):
        ngrok_url, jupyter_token = self.get_server_details_from_logs()
        if ngrok_url:
            return "{0}?token={1}".format(ngrok_url,jupyter_token)