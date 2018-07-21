# -*- coding: utf-8 -*-
from __future__ import division
from main_app.core.utils.mail import mail_sender
from main_app.core.func.func import pagination,capital_flow,buyday
from main_app.core.utils.logger import logger
import datetime
import time
log = logger('log_instance')


if __name__ == '__main__':
    while 1:
        if buyday():
            print('1')
        else:
            print('0')
            time.sleep(2)

