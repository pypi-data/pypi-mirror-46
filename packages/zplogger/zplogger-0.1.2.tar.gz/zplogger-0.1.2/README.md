ZPlogger
=======
    Zpower日志工具


### Usage

>  
    from zplogger.logger import Logger 
    
    logger = Logger(
        file=__file__,
        user='yulong',
        project="shouma",
        server="127.0.0.1",
        debug=True)
    
    log_msg = '''
          this is a test msg for test logger in multiplelines.
    
          Stack messag: 
           xxxx
           more stack info..
       '''
    # warning message
    logger.warn(sys._getframe().f_lineno, log_msg)
    
    # info message
    logger.info(sys._getframe().f_lineno, log_msg)
    
    # error message
    logger.error(sys._getframe().f_lineno, log_msg)
