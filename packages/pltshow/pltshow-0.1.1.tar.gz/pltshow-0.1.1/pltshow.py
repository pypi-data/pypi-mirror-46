# -*- coding: utf-8 -*-
import requests
import pandas

URL="http://api.pltshow.com"

class Client:
    def __init__(self, token = None):
        self.authHeader = {'Authorization' : 'Bearer ' + token}

    def plot(self, df, chart = 'default'):
        requests.post('%s/api/csv/%s' % (URL, chart), headers=self.authHeader, data=bytes(json.to_csv(), encoding = "utf8"))
