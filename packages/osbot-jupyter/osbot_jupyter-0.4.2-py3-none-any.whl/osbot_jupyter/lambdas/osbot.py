from osbot_aws.apis.Lambda import load_dependencies
from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message
from pbx_gs_python_utils.utils.Misc import Misc
from pbx_gs_python_utils.utils.slack.Slack_Commands_Helper import Slack_Commands_Helper


def run(event, context):
    try:
        load_dependencies(['requests'])
        from osbot_jupyter.osbot.Jupyter_Commands import Jupyter_Commands
        params  = Misc.get_value(event, 'params',[])
        if not params: params = ['']
        data    = event.get('data')
        channel = Misc.get_value(data,'channel')
        team_id = Misc.get_value(data, 'team_id')
        params.append({"data": data } )
        return Slack_Commands_Helper(Jupyter_Commands).invoke(team_id, channel, params)
    except Exception as error:
        message = "[lambda_osbot] Error: {0}".format(error)
        #log_to_elk(message, level='error')
        return message