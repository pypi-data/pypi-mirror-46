ZPlogger
=======

> Zpower日志工具


### Usage

>  
    from zplogger import logger
    logger = Logger(
        user='yulong',
        project="shouma",
        server="xxx.xxx.xxx.xxx", # server ip address
        debug=True)
    log_msg = 'this is a test msg for test logger in multiplelines.'
    logger.warn(sys._getframe().f_lineno, log_msg)
    logger.error(sys._getframe().f_lineno, log_msg)
    logger.log(sys._getframe().f_lineno, log_msg)
