from controllers.api_requests import userApi, clistApi
from datetime import datetime as dt
import re


class misc:
    def __init__(self, handle, sender, db):
        self.handle = handle
        self.sender = sender
        self.db = db

    def help(self):
        help_text = ('Send me ContestID and your cf handle to know Rating Changes both predicted and official. For example: rate tourist 1400',
        'Remember your handle to enable handleless query. Send me: Remember tourist.',
        'if you write \'rate tourist\', it will show what tourist did in the last contest',
        'So now you know, \'Rate <cfhandle>\' will reply you with last contest rating change','Now, remember yourself first to make life easier :P')

        return help_text

    def remember(self):  # Remember Handle

        print(self.handle, self.sender)

        verify_res = userApi.info(self.handle)

        if verify_res['status'] == 'FAILED':
            return '{} not found'.format(self.handle)

        self.db.collection('profiles').document(self.sender).set({
            'username': self.handle
        })

        msg = (
            '{} remembered'.format(self.handle),
            'Great! Now send me \'Rate\' to know what {} did in the last rated contest :D'.format(
                self.handle)
        )

        return msg

    def whoAmI(self):
        try: return 'I guess you\'re {} 👀'.format(self.db.collection('profiles').document(self.sender).get().to_dict()['username'])
        except: return ('I don\'t know you yet :/', 'But you can identify yourself ;)', 'Just send me, Remember CFHANDLE')

    def upcomingContest(self):
        try:
            FILTER_CONTEST_SITE = ['codeforces', 'toph', 'topcoder', 'codechef']
            MAX_DURATION = 5*60*60 # Seconds

            processed_list = []

            data = clistApi.contests()

            for each in data['objects']:
                contest_data = {}

                time_now = dt.now()
                contest_start_time = dt.fromisoformat(each['start'])
                time_delta = (contest_start_time - time_now).total_seconds()

                if time_delta < 0: break

                for i in FILTER_CONTEST_SITE:
                    if i in each['href']:
                        each['href'] = each['href'].replace("http://","https://")

                        if each['duration'] <= MAX_DURATION:
                            contest_data = {
                                'time_delta': time_delta,
                                'start': each['start'],
                                'name':each['event'],
                                'href':each['href'],
                            }

                    if contest_data:
                        processed_list.append(contest_data)
                        break
                
                # print(contest_data)

            processed_list = sorted(processed_list, key= lambda i: i['time_delta'])
            processed_list = processed_list[0:4]

            readable_message = []

            for each in processed_list:
                readable_message.append({
                    'title': each['name'],
                    'subtitle': 'Starts ' + each['start'],
                    'default_action': {
                        'type' : 'web_url',
                        'url' : each['href'],
                        'webview_height_ratio' : 'tall',
                        'messenger_extensions' : True if 'codeforces' in each['href'] else False
                    }
                })

            return readable_message

        except Exception as e:
            print("upcoming contest error", e)

        return 'Found'


