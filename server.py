import requests,os
from flask import Flask, request, render_template, redirect, url_for
from controllers.processor import jobDistributor
from controllers.facebook_api import facebook
app = Flask(__name__)

TOKEN = os.environ['TOKEN']
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'GET' and request.args.get('hub.verify_token') == os.environ['VERIFY_TOKEN']:
        return request.args.get('hub.challenge')

    elif request.method == 'GET':
        return redirect(url_for('index'))

    data = request.get_json()

    try:
        nlp = data['entry'][0]['messaging'][0]['message']['nlp']
        sender = data['entry'][0]['messaging'][0]['sender']['id']

        bot = jobDistributor(nlp,sender)

        made_msg = bot.distribute()

        print(made_msg)

        if 'tuple' in str(type(made_msg)):
            for msg in made_msg:
                if msg: facebook.send_message(msg,sender)
        else: facebook.send_message(made_msg, sender)

    except Exception as e:
        print(e)
        facebook.send_message('Sorry! Something went wrong', sender)
        pass

    return 'ok',200

# print(fetch_rating_change('1266','hwyyou'))

if __name__ == "__main__":
    app.run(debug=True, threaded=True, port=80)
