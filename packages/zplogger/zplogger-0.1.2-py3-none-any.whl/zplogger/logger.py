import datetime
import sys
import requests
import json

import inspect

class LineMeta(type):
    def __repr__(self):


        stack = inspect.stack()
        print(stack)
        callerframerecord = stack[stack.__len__()-1]  # 0 represents this line
        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)

        return str(info.lineno)


class FileMeta(type):
    def __repr__(self):

        stack = inspect.stack()
        callerframerecord = stack[stack.__len__()-1]  # 0 represents this line
        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)

        return str(info.filename)

class FuncMeta(type):
    def __repr__(self):

        stack = inspect.stack()
        callerframerecord = stack[stack.__len__()-1]  # 0 represents this line
        frame = callerframerecord[0]
        info = inspect.getframeinfo(frame)

        return str(info.function)

class __ZLINE__(metaclass=LineMeta):
    pass

class __ZFILE__(metaclass=FileMeta):
    pass

class __ZFUNC__(metaclass=FuncMeta):
    pass

class Logger():
    def __init__(self, user='NoUser', file='NoFile', server='10.25.213.32', ip=None, project='', ext=0, debug=False):
        self.logprefix = "%(user)s	%(ip)s	%(project)s	%(file)s	" % ({
            "user": user,
            "ip": ip or requests.get('http://ip.42.pl/raw').text,
            "project": project,
            "file": file
        })
        self.server = "http://%s:50000" % server
        self.ext = ext
        self.debug = debug

    def before_log(self):
        pass

    def after_log(self):
        pass

    def msg(self, type, line, msg):
        self.before_log()

        msg = '%s	' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") \
              + self.logprefix + "%s	%s	%s	%s" % (line, type, self.ext, msg)

        status = ''

        if self.debug:
            print('[Logger][%s] %s' % (type, msg))
        else:
            status = requests.post(self.server, data=json.dumps([{"headers": {}, "body": msg}]))

        self.after_log()

        return msg, status.status_code if status else 'DEBUG'

    def info(self, line, content):
        return self.msg('info', line, content)


    def warn(self, line, content):
        return self.msg('warn', line, content)


    def error(self, line, content):
        return self.msg('error', line, content)
