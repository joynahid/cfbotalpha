import requests
import os
import asyncio
from quart import Quart, request, render_template, redirect, url_for
from controllers.processor import jobDistributor
from wit import Wit

wit = Wit(os.environ['WIT_CLIENT_TOKEN'])

app = Quart(__name__)

TOKEN = os.environ['TOKEN']
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')


@app.route('/')
async def index():
    return await render_template('index.html')


@app.route('/help')
async def help():
    return await render_template('help.html')


@app.route('/webhook', methods=['GET', 'POST'])
async def webhook():
    if request.method == 'GET' and request.args.get('hub.verify_token') == os.environ['VERIFY_TOKEN']:
        return request.args.get('hub.challenge')

    elif request.method == 'GET':
        return redirect(url_for('index'))

    data = await request.get_json()

    try:
        if 'postback' in data['entry'][0]['messaging'][0]:
            if 'Get Started' in data['entry'][0]['messaging'][0]['postback']['title']:
                text = 'Hi! Hope you\'re doing good! Click the text "How to use this bot?" to get started. Hope you will have fun ;)'
                facebook.send_message(
                    text, data['entry'][0]['messaging'][0]['sender']['id'])
                return 'ok'

        nlp = data['entry'][0]['messaging'][0]['message']['nlp']
        sender = data['entry'][0]['messaging'][0]['sender']['id']
        msg = data['entry'][0]['messaging'][0]['message']['text']

        if 'errors' in nlp:
            nlp = wit.message(msg)
            # print(nlp)

        bot = jobDistributor(nlp, sender)
        asyncio.create_task(bot.reply())

    except Exception as e:
        print('Error at server', e)
        pass

    return 'ok', 200
