from controllers.codeforces_api import userApi


class misc:
    def __init__(self, handle, sender, db):
        self.handle = handle
        self.sender = sender
        self.db = db

    def Help(self):
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
