from controllers.network.api_urls import user_api, clist_api
from datetime import datetime as dt
import re, random

ability_text = (
    'You can send me <ContestID> and your <CFHandle> to know rating changes both predicted and official. For example: rate tanusera 1400',
    'The bot can remember you. If you gimme only contestID I\'ll automatically detect you ;) . Send me Remember <YourHandle>',
    'You will be happy to know if you just write \'rate tourist\', it will show what tourist did in the last rated contest',
    'Okay. You can write "rate <cfhandle> <contestid>" to know rating change of <cfhandle>',
    'Do I know you? Send me \'whoami\' :P',
    'Sometimes I don\'t understand your message. So I reply with some of my abilities. Hehe'
)

class misc:
    def __init__(self, handle, sender, db):
        self.handle = handle
        self.sender = sender
        self.db = db

    def ability(self):
        return ability_text[random.randint(0,len(ability_text)-1)]

    def remember(self):  # Remember Handle

        print(self.handle, self.sender)

        try: verify_res = user_api.info(self.handle)
        except: return 'May be Codeforces is down :( . Please try again later'

        if verify_res['status'] == 'FAILED':
            return 'Oopsyy! {} not found in Codeforces'.format(self.handle)

        self.db.collection('profiles').document(self.sender).set({
            'username': self.handle
        })

        msg = (
            '{} remembered'.format(self.handle),
            'Great! Now just send me \'Rate\' to know what {} did in the last rated contest :D'.format(
                self.handle)
        )

        return msg

    def whoAmI(self):
        try: return 'I guess you\'re {} 👀'.format(self.db.collection('profiles').document(self.sender).get().to_dict()['username'])
        except: return ('I don\'t know you yet :/', 'But you can identify yourself ;)', 'Just send me, Remember <YOURCFHANDLE>')

    def upcomingContest(self):
        try:
            FILTER_CONTEST_SITE = ['codeforces', 'toph', 'topcoder', 'codechef', 'atcoder','leetcode','hackerrank']
            MAX_DURATION = 5*60*60 # Seconds

            processed_list = []

            data = clist_api.contests()

            for each in data['objects']:
                contest_data = {}

                time_now = dt.now()
                contest_start_time = dt.fromisoformat(each['start'])
                time_delta = (contest_start_time - time_now).total_seconds()

                delta_days = int(time_delta)//(24*60*60)
                rem_delta = int(time_delta)%(24*60*60)
                delta_hrs = rem_delta//(60*60)
                rem_delta = rem_delta%(60*60)
                delta_mins = rem_delta//60

                time_msg = ''

                if delta_days:
                    time_msg+=str(delta_days) + ' days '
                if delta_hrs:
                    time_msg+=str(delta_hrs) + ' hours '
                if delta_mins:
                    time_msg+=str(delta_mins) + ' minutes'

                each['start'] = time_msg

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
                    'subtitle': 'Starts in ' + each['start'],
                    'buttons': [
                        {
                            'type' : 'web_url',
                            'title': 'Go to Contest',
                            'url' : each['href']
                        }
                    ]
                })

            return readable_message

        except Exception as e:
            print("upcoming contest error", e)

        return 'Found'