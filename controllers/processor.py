import re
import os
import random
import asyncio
import time
from controllers.rating_change_controller import ratingChangeControl
from controllers.misc_controller import misc
import firebase_admin
from firebase_admin import credentials, firestore
from controllers.facebook_api import facebook

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": os.environ['FIREBASE_PROJECT_ID'],
    "private_key_id": os.environ['FIREBASE_PRIVATE_KEY_ID'],
    "private_key": os.environ['FIREBASE_PROJECT_KEY'].replace('\\n', '\n'),
    "client_email": os.environ['FIREBASE_CLIENT_EMAIL'],
    "client_id": os.environ['FIREBASE_CLIENT_ID'],
    "auth_uri": os.environ['FIREBASE_AUTH_URI'],
    "token_uri": os.environ['FIREBASE_TOKEN_URI'],
    "auth_provider_x509_cert_url": os.environ['FIREBASE_AUTH_CERT_URL'],
    "client_x509_cert_url": os.environ['FIREBASE_CLIENT_CERT_URL']
})

firebase_admin.initialize_app(cred)
db = firestore.client()

class jobDistributor:
    def __init__(self, wit, sender=None):
        
        self.intent = None

        try:
            if wit['intents'][0]['confidence']>=0.8:
                self.intent = wit['intents'][0]['name']
        
        self.wit = wit
        self.contest_id = None
        self.handle = None
        self.sender = str(sender)
        self.error = jobErrorHandler()

    def setValue(self, key, confidence):
        # print('Setting', key, self.wit)
        if 'entities' in self.wit and key in self.wit['entities']:
            data = self.wit['entities'][key][0]

            if data['confidence'] > confidence:
                return data['value']

        return self.error.notSure()

    async def reply(self):
        past = time.time()
        made_msg = await asyncio.create_task(self.distribute())
        if 'tuple' in str(type(made_msg)):
            for msg in made_msg:
                if msg:
                    facebook.send_message(msg, self.sender)

        elif 'list' in str(type(made_msg)):
            facebook.send_list_item(made_msg, self.sender)
        else:
            facebook.send_message(made_msg, self.sender)

        future = time.time()
        print('Executed in', future-past, 'seconds')

    async def distribute(self):
        try:
            if not self.intent:
                bot = misc(self.handle, self.sender, db)
                return bot.ability()

            cf_handle_data = self.setValue('cf_handle:cf_handle', 0.8)

            if 'error' not in cf_handle_data:
                self.handle = cf_handle_data
            
            contest_id = self.setValue('contest_id:contest_id', 0.8)

            if 'error' not in contest_id:
                self.contest_id = contest_id

            print('INTENTION', self.intent, self.handle, self.contest_id)

            if self.intent == 'rating_change':
                bot = ratingChangeControl(self.handle, self.contest_id, self.sender, db)
                return await asyncio.create_task(bot.fetch_rating_change_message())

            if self.intent == 'remember':
                if not self.handle: return 'Looks like you didn\'t provide your codeforces handle', 'Send me, Remember yourcfhandle'
                bot = misc(self.handle, self.sender, db)
                return bot.remember()

            if self.intent == 'help':
                bot = misc(self.handle, self.sender, db)
                return bot.help()

            if self.intent == 'whoami':
                bot = misc(self.handle, self.sender, db)
                return bot.whoAmI()

            if self.intent == 'upcoming_contests':
                bot = misc(self.handle, self.sender, db)
                return bot.upcomingContest()

        except Exception as e:
            print('Bot error', e)

class jobErrorHandler:
    def notSure(self):
        text = 'I\'m not sure what you\'ve sent 🙁. Can you write explicitly?', 'It will help me understand'
        return {'error' : text}