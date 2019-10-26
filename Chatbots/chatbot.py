from flask import Flask, request
import requests
import json
import textblob

app = Flask(__name__)


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


@app.route("/", methods=['POST'])
def listen():
    payload = request.data.decode('utf-8')
    message = json.loads(payload)
    response = get_bot_response(message['message'])
    return json.dumps({'response':response})


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
