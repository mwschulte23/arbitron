import json
import requests
import pandas as pd
import datetime as dt
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from src import logger

class DataGrab:
    def __init__(self, api_key, sport='basketball_nba', mkt='h2h'):  # mkt=totals
        self.url = 'https://api.the-odds-api.com/v3/odds?sport={}&region=us&mkt={}&apiKey={}'
        self.api_key = api_key
        self.mkt = mkt
        self.sport= sport
        self.json_data = self.request_odds().json()
        self.configs = self._load_configs()


    def __str__(self):
        return 'get, map data from api & store in redis'


    def _load_configs(self):
        with open('configs/configs.json') as f:
            file = json.load(f)

        return file


    def _request_retry(self, retries=3, backoff_factor=0.3,
                       status_forcelist=(401, 404, 500, 502, 504), session=None):
        '''API request retry logic'''
        session = session or requests.Session()
        retry = Retry(total=retries,
                      read=retries,
                      connect=retries,
                      backoff_factor=backoff_factor,
                      status_forcelist=status_forcelist
                      )

        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        return session


    def request_odds(self):
        full_url = self.url.format(self.sport, self.mkt, self.api_key)
        re = self._request_retry().get(full_url)

        if re.status_code != 200:
            raise Exception(f'Non-200 status code returned: {re.status_code}')
        else:
            logger.info(f'API request status code: {re.status_code}')

        return re


    def _dt_format(self, x):
        delt = dt.timedelta(hours=6)
        return (dt.datetime.utcfromtimestamp(x) - delt).strftime('%Y-%m-%d %H:%M:%S')


    def data_construction(self):
        # convert api data into a dataframe
        dfs = []

        for game in self.json_data['data']:
            for site in game['sites']:
                df = pd.DataFrame({'last_updated': self._dt_format(site['last_update']),
                                   'side1': game['teams'][0],
                                   'side1_odds': site['odds']['h2h'][0],
                                   'side2': game['teams'][1],
                                   'side2_odds': site['odds']['h2h'][1],
                                   'start_time': self._dt_format(game['commence_time']),
                                   'site': site['site_nice'],
                                   'sport': game['sport_nice'],
                                   'arb_key': None
                                   },
                                  index=[0])
                dfs.append(df)

        df = pd.concat(dfs)
        out_df = df.loc[df['site'].isin(self.configs['sites'])]

        logger.info('JSON data converted to pandas dataframe')

        return out_df

