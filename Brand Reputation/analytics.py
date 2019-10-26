from flask import Flask, request
import requests
import json
import random
import textblob

app = Flask(__name__)


def get_bot_response(message):
    blob = textblob.TextBlob(message)

    nouns = []
    for word, tag in blob.tags:
        if tag == 'NN' and len(nouns)<=8:
            nouns.append(word)



    text_parts = []
    for word, pos in blob.tags:
        text_parts.append([word, pos])

    avg_polarity = 0
    avg_subjectivity = 0

    for sentence in blob.sentences:
        avg_polarity += sentence.sentiment.polarity
        avg_subjectivity += sentence.sentiment.subjectivity

    return {
        'tags': text_parts,
        'polarity': avg_polarity/len(blob.sentences),
        'subjectivity': avg_subjectivity/len(blob.sentences),
        'summary': nouns
    }


@app.route("/", methods=['POST'])
def listen():
    payload = request.data.decode('utf-8')
    message = json.loads(payload)
    response = get_bot_response(message['message'])
    return json.dumps(response)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
