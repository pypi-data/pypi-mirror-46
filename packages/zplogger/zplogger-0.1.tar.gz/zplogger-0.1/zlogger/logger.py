import datetime
import sys
import requests
import json

class Logger():
    def __init__(self, user='NoUser', server='10.25.213.32', ip=None, project='', ext=0, debug=False):
        self.logprefix = "%(ip)s	%(project)s	%(file)s	" % ({
            "user": user,
            "ip": ip or requests.get('http://ip.42.pl/raw').text,
            "project": project,
            "file": __file__
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

        status = requests.post(self.server, data=json.dumps([{"headers":{},"body":msg}]))

        self.after_log()

        if self.debug:
            print('[%s][Logger][%s] %s' % (status.status_code, type, msg))


        return msg, status.status_code

    def log(self, line, content):
        return self.msg('log', line, content)


    def warn(self, line, content):
        return self.msg('warn', line, content)


    def error(self, line, content):
        return self.msg('error', line, content)



if __name__ == '__main__':
    logger = Logger(
        user='yulong',
        project="shouma",
        server="10.25.213.32",
        debug=True)
    log_msg = '''
       this is a test msg for test logger in multiplelines.
       
       Stack messag: 
        xxxx
        afdsfdsf
    '''

    logger.warn(sys._getframe().f_lineno, log_msg)