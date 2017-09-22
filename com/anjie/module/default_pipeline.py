from com.anjie.base.pipeline import BasePipeline;


class DefaultPipeline(BasePipeline):
    def __init__(self):
        super(DefaultPipeline, self).__init__();
        pass;

    def piplineData(self, data):
        for v in data:
            print("<------------------------->")
            print('\n'.join(['%15s : %s' % item for item in v.__dict__.items()]))
