import os
from slack import WebClient
from slack.errors import SlackApiError
from flask import Flask, request
app = Flask(__name__)
slack_token = 'YOUR_SLACK_TOKEN'
client = WebClient(token=slack_token)
def send_standup_message(channel, user):
    standup_message = f"Hey <@{user}>, it's time for your stand-up! What did you accomplish yesterday? What are you planning to do today? Any blockers?"
    try:
        response = client.chat_postMessage(
            channel=channel,
            text=standup_message
        )
        print(response)
    except SlackApiError as e:
        print(f"Error sending stand-up message: {e.response['error']}")
@app.route('/standup', methods=['POST'])
def standup():
    data = request.get_json()
    if data['type'] == 'url_verification':
        return data['challenge']
    event = data['event']
    if event['type'] == 'app_mention':
        channel = event['channel']
        user = event['user']
        send_standup_message(channel, user)
    return '', 200
if __name__ == '__main__':
    app.run(port=3000)
