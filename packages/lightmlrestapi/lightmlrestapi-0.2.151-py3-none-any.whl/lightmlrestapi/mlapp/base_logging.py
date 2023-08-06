"""
@file
@brief Machine Learning Post request
"""
from datetime import datetime
import os
import json
from time import perf_counter
import logging
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
import jwt
import ujson


class BaseLogging:
    """
    Simplifies logging. Logging is encrypted
    with module :epkg:`pyjwt` if *secret* is specified.
    """

    def __init__(self, secret, folder='.', level=logging.INFO, encoding='utf-8', when='d'):
        """
        @param      secret      secret for encryption (None to avoid encryption)
        @param      folder      folder where to write the logs (None to disable the logging)
        @param      level       logging level
        @param      when        when rotating the logs,
                                see `TimedRotatingFileHandler
                                <https://docs.python.org/3/library/logging.handlers.html?
                                highlight=streamhandler#logging.handlers.TimedRotatingFileHandler>`_
        @param      encoding    encoding
        """
        if folder is None:
            self.logger = None
        else:
            current_time = datetime.now()
            current_date = current_time.strftime("%Y-%m-%d")
            filename = "{0}-{1}.log".format(
                self.__class__.__name__, current_date)
            file_location = os.path.join(folder, filename)
            form = Formatter('%(asctime)s,%(levelname)s,%(message)s,%(data)s')
            self.handler = TimedRotatingFileHandler(
                file_location, encoding=encoding, delay=True, when=when)
            self.handler.setFormatter(form)
            self.logger = logging.getLogger(self.__class__.__name__)
            self.logger.setLevel(level)
            self.logger.addHandler(self.handler)
            self.secret = secret

    def save_time(self):
        """
        Saves the times to get a duration later.
        """
        self.t1 = perf_counter()

    def duration(self):
        """
        Get the duration since @see me save_time was called.
        """
        return perf_counter() - self.t1

    def info(self, msg, data):
        """
        Logs any king of data into the logs.

        @param  msg         message
        @param  data        data to log
        """
        self._logerrorinfo('info', msg, data)

    def error(self, msg, data):
        """
        Logs any king of data into the logs.

        @param  msg         message
        @param  data        data to log
        """
        self._logerrorinfo('error', msg, data)

    def _logerrorinfo(self, fct, msg, data):
        """
        Logs any king of data into the logs.

        @param  msg         message
        @param  data        data to log
        """
        if self.logger is not None:
            if self.secret is None:
                try:
                    dumped = ujson.dumps(data)
                except Exception:  # pylint: disable=W0703
                    # Cannot serialize into json.
                    dumped = str(data)
                extra = dict(data=dumped)
            else:
                enc_data = jwt.encode(data, self.secret, algorithm='HS256')
                extra = dict(data=enc_data)
            if fct == 'info':
                self.logger.info(msg, extra=extra)
            else:
                self.logger.error(msg, extra=extra)


def enumerate_parsed_logs(folder, secret, encoding='utf-8'):
    """
    Goes through a list of logged files,
    reads and decrypts the content.

    @param      folder      folder which contains the logs
    @param      secret      secret
    @param      encoding    encoding
    @return                 iterator on decrypted data
    """
    for root, _, files in os.walk(folder):
        for name in files:
            full = os.path.join(root, name)
            with open(full, 'r', encoding=encoding) as f:
                for i, line in enumerate(f):
                    spl = line.rstrip('\n\r').split(',')
                    if secret is None:
                        dt = datetime.strptime(spl[0], '%Y-%m-%d %H:%M:%S')
                        data = ','.join(spl[4:])
                        try:
                            data = ujson.loads(data)
                        except ValueError:
                            # json gives better error messages.
                            data = json.loads(data)
                        # data should be a dictionary saved as a string
                        rec = dict(dt=dt, code=spl[1], level=spl[2],
                                   msg=spl[3], data=data)
                        yield rec
                    else:
                        if len(spl) != 5:
                            raise ValueError(
                                "Format issue in\n    File \"{0}\", line {1}".format(full, i + 1))
                        if spl[4].startswith("b'") and spl[4].endswith("'"):
                            data = spl[4][2:-1]
                        else:
                            raise ValueError(
                                "Corrupted logs due to: '{0}'".format(spl[4]))
                        dec = jwt.decode(data, secret, algorithms=['HS256'])
                        dt = datetime.strptime(spl[0], '%Y-%m-%d %H:%M:%S')
                        rec = dict(dt=dt, code=spl[1], level=spl[2],
                                   msg=spl[3], data=dec)
                        yield rec
