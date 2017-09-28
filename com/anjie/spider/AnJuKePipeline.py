from com.anjie.base.pipeline import BasePipeline;


class AnJuKePipeline(BasePipeline):
    def __init__(self):
        super(AnJuKePipeline, self).__init__();
        self.belongToSpider = 'AnJuKe'

    def piplineData(self, data):
        for v in data:
            print("<------------------------->")
            print('\n'.join(['%15s : %s' % item for item in v.__dict__.items()]))
