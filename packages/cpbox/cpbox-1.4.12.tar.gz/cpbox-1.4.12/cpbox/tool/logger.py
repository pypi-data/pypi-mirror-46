import logging
import logging.handlers
import syslog
import socket
import os

from cpbox.tool import net
from cpbox.tool import timeutil

class Holder():

    def __init__(self):
        self.basic_handlers = []
        pass

holder = Holder()

try:
    from threading import get_ident
except ImportError:
    from thread import get_ident

class SysLogHandler(logging.handlers.SysLogHandler):

    def emit(self, record):
        super(SysLogHandler, self).emit(record)

class ContextFilter(logging.Filter):

    def __init__(self):
        self.local_ip = net.get_ip_address_udp()

    def filter(self, record):
        record.local_ip = self.local_ip
        record.pid = os.getpid()
        record.tid = get_ident()
        record.time_iso_8601 = timeutil.local_now_ios8061_str()
        return True

def getLogger(name=''):
    logger = logging.getLogger(name)
    return logger

def make_event_logger(app_name, syslog_handler):
    # This is what we want: 2018-11-12T15:34:34+08:00 117.50.2.88 15051.50683 cp mid-call {"fail":0,"service":"id_service.next_id","rt_1":1.1670589447021,"rt":1.1730194091797,"env":"prod"}
    # python strftime can not print timezone as +08:00
    # logstash grok ISO8601_TIMEZONE will let this go: 2018-11-12T15:36:46+0800 172.16.1.150 28114.139798089959232 None test {"env": "dev", "time": "2018-11-12 15:36:46.359019"}
    # ${time_iso_8601} ${client_ip} ${pid}.${rnd/thread_id} {$app_name} ${event_key} ${payload_json_encoded}
    event_log_formatter = logging.Formatter(app_name + '_event_log: %(message)s')
    format_str = app_name + '_event_log[%(pid)d]: %(time_iso_8601)s %(local_ip)s %(pid)d.%(tid)d %(message)s'
    event_log_formatter = logging.Formatter(format_str)

    filter = ContextFilter()
    syslog_handler.setFormatter(event_log_formatter)
    syslog_handler.addFilter(filter)
    event_logger = logging.getLogger('event-log')
    event_logger.propagate = False
    event_logger.setLevel(logging.INFO)
    event_logger.addHandler(syslog_handler)
    return event_logger

def _get_syslog_handler(syslog_ng_server):
    syslog_handler = None
    tcp_port = 601
    if net.is_open(syslog_ng_server, tcp_port):
        syslog_handler = SysLogHandler(address=(syslog_ng_server, tcp_port), facility='local7', socktype=socket.SOCK_STREAM)
    else:
        syslog_handler = SysLogHandler(address=(syslog_ng_server, 514), facility='local6')
    return syslog_handler

def setup_logger_handler(app_name, handler, log_level_str):
    filter = ContextFilter()
    log_level = logging.INFO
    if log_level_str is not None:
        level = log_level_str.lower()
        log_level_conf = {
            'verbose': logging.NOTSET,
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'warn': logging.WARNING,
            'error': logging.ERROR,
            'critical': logging.CRITICAL,
        }
        if level in log_level_conf:
            log_level = log_level_conf[level]

    format_str = app_name + '[%(pid)d]: %(time_iso_8601)s %(local_ip)s %(pid)d.%(tid)d %(levelname)s %(filename)s:%(lineno)d %(message)s'
    formatter = logging.Formatter(format_str)

    handler.setFormatter(formatter)
    handler.setLevel(log_level)
    handler.addFilter(filter)
    return handler

def make_logger(app_name, log_level_str=None, syslog_ng_server=None, console_debug_log=False):
    root_logger = logging.getLogger()

    basic_handlers = []
    if syslog_ng_server is not None:
        syslog_handler = _get_syslog_handler(syslog_ng_server)
        setup_logger_handler(app_name, syslog_handler, log_level_str)
        basic_handlers.append(syslog_handler)
        make_event_logger(app_name, syslog_handler)

    if console_debug_log:
        stream_handler = logging.StreamHandler()
        setup_logger_handler(app_name, stream_handler, log_level_str)
        basic_handlers.append(stream_handler)

    root_logger.handlers = []
    for h in basic_handlers:
        root_logger.setLevel(h.level)
        root_logger.addHandler(h)
    holder.basic_handlers = basic_handlers

def shutdown():
    for handler in holder.basic_handlers:
        handler.close()
