import json
import requests
from .slack_secrets import web_hook, error_hook
# Set the webhook_url to the one provided by Slack when you create the webhook at https://my.slack.com/services/new/incoming-webhook/
webhook_url = web_hook

def post_to_slack(text, channel):

    channels = {
        'spotter':web_hook,
        'error': error_hook,
    }


    slack_data = {'text': text}
    print("printing channel %s"%(channel))
    print(channels[channel])
    response = requests.post(
        str(channels[channel]),
	data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )