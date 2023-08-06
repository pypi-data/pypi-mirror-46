from osbot_aws.apis.Lambda import Lambda


class GSBot_Execution:

    def __init__(self):
        self.osbot_lambda = Lambda('osbot.lambdas.osbot')
        self.jira_lambda = Lambda('osbot_jira.lambdas.elastic_jira')

    def invoke(self, command):
        params = command.split(' ')
        if len(params) > 0:
            if params[0] == 'jira':
                return self.invoke_jira(params[1:])
        return self.invoke_osbot(command)

    def invoke_osbot(self, command):
        payload = {'event': {'type': 'message',
                             'text': command,
                             'user': 'jovyan'}}

        result      = self.osbot_lambda.invoke(payload)
        text        = result.get('text')
        attachments = result.get('attachments')
        return text,attachments

    def invoke_jira(self, params):
        payload = {'params': params }
        return "[*]: {0}".format(self.jira_lambda.invoke(payload)),[]