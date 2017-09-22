import logging


class Elog:

    # 创建一个logger
    logger = logging.getLogger('')
    # 设置logger的等级，大于等于这个等级的信息会被输出，其他会被忽略
    logger.setLevel(logging.DEBUG)
    # 以下创建的是输出到文件的handler，并把等级设为DEBUG
    fh = logging.FileHandler('spider.log')
    fh.setLevel(logging.DEBUG)

    # 以下创建的是输出到控制台的handler，并把等级设为DEBUG
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)

    # 下面指定了handler的信息输出格式，其中asctime,name,levelname，message都是logging的关键字
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)

    # 把Handler加入到logger中，可理解为给处理者在logger中安排了职位
    logger.addHandler(fh)
    logger.addHandler(sh)

    @staticmethod
    def debug(msg):
        logging.debug(msg);

    @staticmethod
    def info(msg):
        logging.info(msg);

    @staticmethod
    def warning(msg):
        logging.warning(msg);

    @staticmethod
    def error(msg):
        logging.error(msg);

if __name__ == '__main__':
    Elog.debug('ssss')
