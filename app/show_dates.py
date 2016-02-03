from tornado.web import HTTPError

from dateutil import parser as dateparser

from lib import database
from lib import crypto_helper
from lib.request_handler import ApiHandler


class CreateShow(ApiHandler):
    def get(self):
        date_raw = self.get_argument('date')
        try:
            date = dateparser.parse(date)
        except:
            raise HTTPError(status_code=500, reason='INVALID_DATE')
        show = database.get_show(date)
        if show is not None:
            return self.api_response(show)
        else:
            passphrase = crypto_helper.generate_passphrase()
            public_key, private_key = crypto_helper.create_keypair(passphrase)

            shares = crypto_helper.split_passphrase(passphrase)

