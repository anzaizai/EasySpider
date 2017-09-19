class Pipeline:
    def __init__(self):
        pass;

    def piplineData(self,data):
        for  v in data:
            print("<------------------------->")
            print('\n'.join(['%15s : %s' % item for item in v.__dict__.items()]))

