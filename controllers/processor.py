import re
import os
import random
from controllers.rating_change_controller import ratingChangeControl
from controllers.misc_controller import misc
import firebase_admin
from firebase_admin import credentials, firestore

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
        try: self.intent = wit['intents'][0]['name']
        except: self.intent = None
        
        self.wit = wit
        self.contest_id = None
        self.handle = None
        self.sender = str(sender)
        self.error = jobErrorHandler()

        print('Bot Initialized')

    def setValue(self, key, confidence):
        # print('Setting', key)
        if key in self.wit['entities']:
            data = self.wit['entities'][key][0]

            if data['confidence'] > confidence:
                return data['value']

        return self.error.notSure()

    def distribute(self):
        cf_handle_data = self.setValue('cf_handle:cf_handle', 0.8)

        if 'error' not in cf_handle_data:
            self.handle = cf_handle_data
        
        contest_id = self.setValue('contest_id:contest_id', 0.8)

        if 'error' not in contest_id:
            self.contest_id = contest_id

        print(self.intent)

        if self.intent == 'rating_change':
            bot = ratingChangeControl(self.handle, self.contest_id, self.sender, db)
            return bot.fetch_rating_change_message()

        if self.intent == 'remember':
            bot = misc(self.handle, self.sender, db)
            return bot.Remember()

        if self.intent == 'help':
            bot = misc(self.handle, self.sender, db)
            return bot.Help()

        return self.error.notSure()['error']


class jobErrorHandler:
    def notSure(self):
        text = 'I\'m not sure what you\'ve sent 🙁. Can you write explicitly?', 'It will help me understand'
        return {'error' : text}