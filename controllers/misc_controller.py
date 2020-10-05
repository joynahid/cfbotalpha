from controllers.codeforces_api import userApi


class misc:
    def __init__(self, handle, sender, db):
        self.handle = handle
        self.sender = sender
        self.db = db

    def Help(self):
        help_text = ('Send me ContestID and your cf handle to know Rating Changes bot predicted and official. For example: rate tourist 1400',
        'Remember your handle to enable handleless query. Send me: Remember tourist.',
        'if you write \'rate tourist\', it will show what tourist did in the last contest',
        'So now you know, \'Rate <cfhandle>\' will reply you with last contest rating change')

        help_text = help_text.strip()
        msg = help_text
        return msg, 'Now, remember yourself first to make life easier :D'

    def Remember(self):  # Remember Handle

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
