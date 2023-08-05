from onepanel.sdk.jobs import Jobs


class Client():
    def __init__(self, account_uid=None, project_uid=None):
        self.jobs = Jobs(account_uid, project_uid)

