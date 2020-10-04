import re, os, random
from controllers.rating_change_controller import makeRatingChangeMessage
import firebase_admin
from firebase_admin import credentials, firestore
from controllers.codeforces_api import userApi

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

HELP = r'help'
HEY = r'hey|hi|hello|oi|hola'

print(re.findall(HEY, 'hello world'))

RATE_CONTESTID_USERNAME = r"rate \d{1,6} [a-z-._0-9]{1,}"
RATE_CONTESTID = r'rate \d{1,5}'
RATE = r'rate'

REMEMBER_HANDLE = r'remember [a-z-_0-9]{1,}'


class jobDistributor:
    def __init__(self, message, sender=None):
        self.raw_message = message.lower()
        self.sender = str(sender)
        self.errorHandler = rawMessageErrorHandle()

    def find_and_execute_command(self):
        res = re.findall(HELP, self.raw_message)
        if len(res) == 1:
            help_text = """CFBOT αlpha

rate <contestid> <handle>
Shows rating change of <handle> in contest <contestid>

remember <handle>
Remembers your handle to enable querying without typing your handle everytime.

rate <contestid>
Shows rating change of a <contestid>. It needs to remember <handle> first

<rate>
Shows the rating change of the last/ running contest. Extremely useful when you want to know the predicted rating change real quick. Depends on remember <handle> command.
            """

            help_text = help_text.strip()

            msg = help_text
            return msg, 'Now send me \'Remember <yourcfhandle>\' ;)'

        res = re.findall(REMEMBER_HANDLE, self.raw_message)
        if len(res) == 1:
            handle = res[0][9:].strip().split()[0]

            verify_res = userApi.info(handle)

            if verify_res['status'] == 'FAILED':
                return '{} not found'.format(handle)

            db.collection('profiles').document(self.sender).set({
                'username': handle
            })

            msg = f'{handle} remembered. :D'

            return (msg, 'Great! Now send me \'Rate\' to know what you did in the last rated contest ;)')

        res = re.findall(RATE_CONTESTID_USERNAME, self.raw_message)
        if len(res) == 1:
            cmd_id, cmd_username = res[0][5:].strip().split()
            rating = makeRatingChangeMessage(cmd_username, cmd_id)
            msg = rating.fetch_rating_change_message()
            return msg

        res = re.findall(RATE_CONTESTID, self.raw_message)
        if len(res) == 1:
            try:
                cmd_id = res[0][5:].strip().split()[0]
                cmd_username = db.collection('profiles').document(
                    self.sender).get().to_dict()['username']
                rating = makeRatingChangeMessage(cmd_username, cmd_id)
                msg = rating.fetch_rating_change_message()
                return msg
            except:
                return self.errorHandler.username_not_found()

        res = re.findall(RATE, self.raw_message)
        if len(res) == 1:
            try:
                cmd_username = db.collection('profiles').document(
                    self.sender).get().to_dict()['username']
                rating = makeRatingChangeMessage(cmd_username)
                msg = rating.fetch_rating_change_message()
                return msg
            except:
                return self.errorHandler.username_not_found()

        res = re.findall(HEY, self.raw_message)
        if res:
            msg = ['Hey! What\'s up?','Hello! How are you doing? :D', 'Hi! Hope you\'re doing good']
            help_text = 'Send \'help\' to know what you can do with me'
            return msg[random.randint(0,2)], help_text

        return self.errorHandler.wrong_format()


class rawMessageErrorHandle:
    def wrong_format(self):
        return ("I'm still a noob to recognize your message :(", "Send \'help\' to see queries you can perform")

    def username_not_found(self):
        return 'Handle not found :/. Send "remember handle" to query handleless commands'
