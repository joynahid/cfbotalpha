import requests, os

TOKEN = os.environ['TOKEN']

class facebookApi:
    def send(self, request_body):
        print(request_body)
        resp = requests.post('https://graph.facebook.com/v5.0/me/messages?access_token='+TOKEN, json=request_body, headers = {'Content-type': 'application/json'})
        print(resp.text)

    def send_message(self, msg=None,recipient_id=None):
        try:
            if msg:
                request_body = {
                    'recipient': {
                        'id': recipient_id
                    },
                    'message': {
                        "text": msg
                    }
                }

                self.send(request_body)
        except:
            pass

    def send_list_item(self, List, recipient_id):
        try:
            if List:
                request_body = {
                    'recipient': {
                        'id' : recipient_id
                    },
                    'message' : {
                        'attachment': {
                            'type':'template',
                            'payload': { 
                                "template_type": "generic",
                                "elements": List
                            }
                        }
                    }
                }

                self.send(request_body)
        except:
            pass

facebook = facebookApi()