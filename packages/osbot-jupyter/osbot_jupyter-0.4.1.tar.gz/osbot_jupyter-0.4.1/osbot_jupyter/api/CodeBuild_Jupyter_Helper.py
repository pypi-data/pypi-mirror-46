from time import sleep

from osbot_aws.apis.CodeBuild import CodeBuild
from osbot_aws.apis.Secrets import Secrets
from pbx_gs_python_utils.utils.Json import Json
from pbx_gs_python_utils.utils.Misc import Misc

from osbot_jupyter.api.CodeBuild_Jupyter import CodeBuild_Jupyter


class CodeBuild_Jupyter_Helper:

    def __init__(self):
        self.project_name  = 'OSBot-Jupyter'
        self.code_build    = CodeBuild(project_name=self.project_name,role_name=None)
        self.max_builds    = 10
        self.build_timeout = 240
        self.server_sizes  = {'small': 'BUILD_GENERAL1_SMALL', 'medium': 'BUILD_GENERAL1_MEDIUM','large': 'BUILD_GENERAL1_LARGE'}

    def get_active_build_id(self):
        builds = self.get_active_builds(stop_when_match=True)
        return Misc.array_pop(list(set(builds)))

    def get_active_builds(self, stop_when_match=False):
        build_ids   = list(self.code_build.project_builds_ids(self.project_name))[0:self.max_builds]
        build_infos = self.code_build.codebuild.batch_get_builds(ids=build_ids).get('builds')
        builds = {}
        for build_info in build_infos:
            build_id = build_info.get('id')
            if build_info.get('currentPhase') != 'COMPLETED':
                builds[build_id] = CodeBuild_Jupyter(build_id=build_id, build_info=build_info)
                if stop_when_match:
                    return builds
        return builds

    def get_active_server_details(self):
        build_id = self.get_active_build_id()
        if build_id is None:
            self.start_build_and_wait_for_jupyter_load()
            build_id = self.get_active_build_id()
        code_build = CodeBuild_Jupyter(build_id)
        return code_build.get_server_details_from_logs()

    def start_build(self):
        build_arn =self.code_build.build_start()
        build_id = build_arn.split('build/').pop()
        return CodeBuild_Jupyter(build_id=build_id)

    def start_build_and_wait_for_jupyter_load(self, max_seconds=60):
        build = self.start_build()
        return self.wait_for_jupyter_load(build,max_seconds)

    def start_build_for_repo(self,repo_name,user='gsbot', server_size='small'):
        aws_secret = "git__{0}".format(repo_name)

        data = Secrets(aws_secret).value_from_json_string()
        repo_url = data['repo_url']

        kvargs = {
            'projectName'                 : self.project_name,
            'timeoutInMinutesOverride'    : self.build_timeout ,
            'sourceLocationOverride'      : repo_url,
            'computeTypeOverride'         : self.server_sizes[server_size],
            'environmentVariablesOverride': [{'name': 'repo_name', 'value': repo_name, 'type': 'PLAINTEXT'},
                                             {'name': 'user'     , 'value': user     , 'type': 'PLAINTEXT'}]
        }
        build_id = self.code_build.codebuild.start_build(**kvargs).get('build').get('arn')
        return {'status': 'ok', 'data': build_id}

    def start_build_for_repo_and_wait_for_jupyter_load(self, repo_name, user='gsbot'):
        build_id = self.start_build_for_repo(repo_name,user).get('data')
        build    = CodeBuild_Jupyter(build_id=build_id)
        return self.wait_for_jupyter_load(build)


    def stop_all_active(self):
        available_builds = self.get_active_builds()
        stopped = []
        for build_id in available_builds.keys():
            self.code_build.codebuild.stop_build(id=build_id).get('build')
            stopped.append(build_id)
        return stopped

    def save_active_server_details(self, file):
        build_id     = self.get_active_build_id()
        server,token = CodeBuild_Jupyter(build_id).get_server_details_from_logs()
        config = { 'build_id': build_id,
                   'server'  : server  ,
                   'token'   : token   }
        Json.save_json(file, config)
        return config

    def wait_for_jupyter_load(self, build,max_seconds=90):
        seconds_sleep = 5
        for i in range(0,max_seconds,seconds_sleep):
            sleep(seconds_sleep)
            (ngrok_url,jupyter_token) = build.get_server_details_from_logs()
            if ngrok_url is not None:
                return "{0}?token={1}".format(ngrok_url, jupyter_token)

    def util_rename_secret(self, old, new):
        old = "git__{0}".format(old)
        new = "git__{0}".format(new)
        data = Secrets(old).value()
        if data:
            Secrets(new).create(data)
        if Secrets(new).value() == Secrets(old).value():
            Secrets(old).delete()
            return True