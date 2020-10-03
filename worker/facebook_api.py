import requests, os

TOKEN = os.environ['TOKEN']

class facebookApi:
    def send_message(self, msg=None,recipient_id=None):
        try:
            if msg:
                request_body = {
                    'recipient': {
                        'id': recipient_id
                    },
                    'message': {"text": msg}
                }
                
                requests.post('https://graph.facebook.com/v5.0/me/messages?access_token='+TOKEN, json=request_body)
        except:
            pass

facebook = facebookApi()