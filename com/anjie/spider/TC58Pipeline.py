from com.anjie.base.pipeline import BasePipeline;


class TC58Pipeline(BasePipeline):
    def __init__(self):
        super(TC58Pipeline, self).__init__();
        self.belongToSpider = 'TC58Spider';

    def piplineData(self, data):
        for v in data:
            print("<------------------------->")
            print('\n'.join(['%15s : %s' % item for item in v.__dict__.items()]))
