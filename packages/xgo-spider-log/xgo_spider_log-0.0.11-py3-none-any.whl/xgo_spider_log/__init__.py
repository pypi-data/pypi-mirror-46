import logging
import logging.handlers
import socket
import os
import json

delimiter = '|'

name = 'xgo_spider_log'


def create_logger(log_level=logging.DEBUG):
    """
    create monitor logger
    :param log_level logging log level
    :return: logging object
    """

    debug = (os.getenv('PROD') != '1')

    hostname = socket.gethostname()
    project_name = os.getenv('PROJECT_NAME')

    # create logger
    logger = logging.getLogger(project_name)
    logger.setLevel(log_level)

    class ContextFilter(logging.Filter):
        """
        This is a filter which injects contextual information into the log.
        """
        def filter(self, record):
            record.project_name = project_name
            record.delimiter = delimiter
            record.program = project_name
            return True
    logger.addFilter(ContextFilter())
    formatter = logging.Formatter('%(program)s %(project_name)s%(delimiter)s%(name)s%(delimiter)s%(asctime)s%(delimiter)s%(levelname)s%(delimiter)s%(message)s', "%Y-%m-%d %H:%M:%S")


    if debug:
        # create stream logger handler
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    else:
        # create syslog logger handler
        sh = logging.handlers.SysLogHandler(address='/var/log/spider.sock')
        sh.setLevel(log_level)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

    return logger


monitor_logger = create_logger(logging.DEBUG)


def log_syslog(msg):
    monitor_logger.info(json.dumps(msg, ensure_ascii=False))

def spider_start():
    '''
    @description: 爬虫开始事件，爬虫启动时调用
    @return: 
    '''
    msg = {
        'type': 'event',
        'content': '抓取开始'
    }
    log_syslog(msg)

def spider_stop():
    '''
    @description: 爬虫停止事件，爬虫结束时调用
    @return: 
    '''
    msg = {
        'type': 'event',
        'content': '抓取结束'
    }
    log_syslog(msg)

def spider_aborting():
    '''
    @description: 爬虫异常退出事件，异常退出时调用
    @return: 
    '''
    msg = {
        'type': 'event',
        'content': '异常结束'
    }
    log_syslog(msg)

def spider_node_start():
    '''
    @description: 爬虫节点启动（分布式爬虫专用）
    @param {type} 
    @return: 
    '''
    msg = {
        'type': 'event',
        'content': '节点抓取开始'
    }
    log_syslog(msg)

def spider_node_stop():
    '''
    @description: 爬虫节点停止（分布式爬虫专用）
    @param {type} 
    @return: 
    '''
    msg = {
        'type': 'event',
        'content': '节点抓取结束'
    }
    log_syslog(msg)

def spider_node_aborting():
    '''
    @description: 爬虫节点异常退出（分布式爬虫专用）
    @param {type} 
    @return: 
    '''
    msg = {
        'type': 'event',
        'content': '节点异常结束'
    }
    log_syslog(msg)

def crawl_content(type, count=1, extra={}):
    '''
    @description: 记录抓取内容及数量
    @param {string} type 内容类型 
    @param {int} count 内容数量
    @param {dict} extra 附加信息
    @return: 
    '''
    msg = {
        'type': 'count',
        'content_type': type,
        'count': count
    }
    msg.update(extra)
    log_syslog(msg)

def crawl_failed(type, count=1, extra={}):
    '''
    @description: 记录抓取失败的内容及数量
    @param {string} type 内容类型 
    @param {int} count 内容数量
    @param {dict} extra 附加信息
    @return: 
    '''
    msg = {
        'type': 'failed_count',
        'content_type': type,
        'count': count
    }
    msg.update(extra)
    log_syslog(msg)

def queue_remaining(type, count):
    '''
    @description: 记录剩余需抓取的内容及数量
    @param {string} type 内容类型 
    @param {int} count 内容数量
    @return: 
    '''
    msg = {
        'type': 'count',
        'content_type': f'{type}-剩余',
        'count': count
    }
    log_syslog(msg)

def general_log(log_dict):
    '''
    @description: 通用日志，可自定义数据结构
    @param {dict} log_dict 自定义内容 
    @return: 
    '''
    msg = {
        'type': 'general'
    }
    msg.update(log_dict)

    log_syslog(msg)

def general_log_info(info):
    '''
    @description: 快捷方法，记录通用内容
    @param {type} 
    @return: 
    '''
    general_log({'info': info})
    

if __name__ == "__main__":
    spider_start()
    crawl_content('ahh', 1)
    queue_remaining('ahh', 1)