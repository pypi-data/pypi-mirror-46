from pbx_gs_python_utils.utils.Lambdas_Helpers import slack_message




def run(event, context):
    repo_name = event.get('repo_name')
    channel   = event.get('channel')
    team_id   = event.get('team_id')
    user      = event.get('user')
    slack_message(":point_right: Hi <@{0}>, starting Jupyter server for you with the repo `{1}`.\n :information_source: This should take between 20 and 60 seconds".format(user, repo_name), [], channel, team_id)
    try:
        from osbot_jupyter.api.CodeBuild_Jupyter_Helper import CodeBuild_Jupyter_Helper

        login_url = CodeBuild_Jupyter_Helper().start_build_for_repo_and_wait_for_jupyter_load(repo_name,user)
        if login_url:
            slack_message(":point_right: Server started ok, please use this link to open it:\n {0}".format(login_url), [], channel, team_id)
        else:
            slack_message(":red_circle: Something went wrong, and the server failed to start. Please check that the repo `{0}` exists.".format(repo_name),[], channel, team_id)

    except Exception as error:
        slack_message(":red_circle: Something went wrong: {0}".format(error),[], channel, team_id)
        return "{0}".format(error)

