from osbot_aws.apis.Lambda import Lambda

class Jp_Jira:
    def issue(self,issue_id):
        print('getting screenshot of issue {0} from jira'.format(issue_id))

        from IPython.display import display_html

        jira_web = Lambda('osbot_browser.lambdas.jira_web')
        payload = {'issue_id': issue_id}
        png_data = jira_web.invoke(payload)
        html = '<img style="border:1px solid black" align="left" src="data:image/png;base64,{}"/>'.format(png_data)
        display_html(html, raw=True)