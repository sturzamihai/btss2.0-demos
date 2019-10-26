from flask import Flask, request
import requests
import json
import textblob

app = Flask(__name__)

TOKEN = 'EAAK09rzmZA4IBACg8hZCccv3lM5ZATUgDM0jiZAo4WTWoOdbBGN3iDIV9BH0lIw2cILKWzaNCh0KdEj5KZCZA95ZCyE5RLqwc9gfKVaLQHHTU0pbAgeqzUPVmft8TRarYnpZASImxSF7g1FVyMq3nzAMFo8s9Vne0SOrma38rjKntgZDZD'
VERIFY_TOKEN = 'demobtss20'


def convert_polarity(polarity):
    if polarity < 0.1 and polarity > -0.1:
        return 'Thank you for your feedback.'
    elif polarity >= 0.1:
        return 'Thank you for your feedback. We\'re really glad you liked our experience with us!'
    elif polarity <= 0.1:
        return 'Thank you for your feedback. We\'re sorry if you are unsatisfied.'


def get_bot_response(message):
    blob = textblob.TextBlob(message)
    avg_polarity = 0
    for sentence in blob.sentences:
        avg_polarity += sentence.sentiment.polarity

    return convert_polarity(avg_polarity/len(blob.sentences))


def respond(sender, message):
    response = get_bot_response(message)
    send_message(sender, response)


def send_message(sender_id, message):
    payload = {
        'message': {
            'text': message
        },
        'recipient': {
            'id': sender_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': TOKEN
    }

    response = requests.post(
        'https://graph.facebook.com/v2.6/me/messages',
        params=auth,
        json=payload
    )

    return response.json()


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
    else:
        return "incorrect"


def is_user_message(message):
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))


@app.route("/webhook")
def listen():
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        payload = request.json
        event = payload['entry'][0]['messaging']
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                respond(sender_id, text)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
