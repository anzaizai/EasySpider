


class BaseScheduler:
    def __init__(self):
        super(BaseScheduler, self).__init__();

    def __iter__(self):
        return self

    def __next__(self):
        pass;

    def nextRequest(self):
        pass

    def addRequest(self, rq):
        pass

    def addRequests(self, rqs):
        pass;

    def addLoserRequest(self, rq):
        pass;
