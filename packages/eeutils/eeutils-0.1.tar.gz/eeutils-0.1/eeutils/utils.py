# -*- coding: utf-8 -*-
import psycopg2
import logging

logger = logging.getLogger(__name__)


class with_cr(object):
    ok_params = ['dbname', 'database', 'user', 'password', 'host', 'port']

    def __init__(self, fnct):
        self.fnct = fnct

    @property
    def __name__(self):
        return self.fnct.__name__

    def __call__(self, *args, **kwargs):
        psyco_args = {k: v for k, v in kwargs.items() if k in self.ok_params}
        try:
            self.conn = psycopg2.connect(**psyco_args)
        except psycopg2.OperationalError as e:
            return self.fnct(*args, **kwargs)
        cursor = self.conn.cursor()
        kwargs['cr'] = cursor
        res = self.fnct(*args, **kwargs)
        cursor.close()
        self.conn.close()
        return res
