from __future__ import unicode_literals

import balanced
from flask import redirect, url_for, request
import json
import requests
from requests.auth import HTTPBasicAuth

from rentmybike import config
from rentmybike.controllers import route, authenticated
from rentmybike.db import Session


@route('/transactions', 'transactions.index')
@authenticated()
def index():
    account_href = request.user.account_href
    if not account_href:
        try:
            account = balanced.Customer.query.filter(
                email=self.request.user.email).one()
        except balanced.exc.NoResultFound:
            return redirect(url_for('accounts.index',
                reason='no-balanced-account'))
        else:
            request.user.account_href = account_href = account.href
            Session.commit()

    # let's create a login token for this user
    token_uri = 'https://dashboard.balancedpayments.com/v1/logins'
    data = {
        'account_href': account_href,
        'redirect_uri': config['DOMAIN_URI'],
    }
    result = requests.post(token_uri, data=json.dumps(data),
        auth=HTTPBasicAuth(balanced.config.api_key_secret, ''),
        headers={'content-type': 'application/json'})
    data = json.loads(result.content)
    return 'transactions/interstitial.mako', {
        'redirect_to': data['token_uri'],
        }
