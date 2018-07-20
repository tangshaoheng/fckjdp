# -*- coding: utf-8 -*-
from __future__ import division
from utils.mail import mail_sender
from main.fun import pagination,capital_flow,buyday
from utils.logger import logger
import datetime
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
log = logger('xxxx')


if __name__ == '__main__':
    while 1:
        if buyday():
            print '1'
        else:
            print '0'
            time.sleep(2)

