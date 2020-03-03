import os
import json
import redis
import pandas as pd
from urllib import parse

from src import logger
from src.data_grab import DataGrab


class ArbFinder(DataGrab):
    def __init__(self, configs, sport='basketball_nba', mkt='h2h'):
        super().__init__(os.getenv('API_KEY'), configs, sport, mkt)
        self.redis_url = parse.urlparse(os.getenv('REDIS_URL'))
        self.configs = configs


    def __str__(self):
        return 'find best available odds across bookies'


    def _best_odds_grouper(self, data):
        '''
        Used in pandas groupby (split-apply-combine)
        '''
        side1 = dict(zip(data['side1_odds'], data['site']))
        side2 = dict(zip(data['side2_odds'], data['site']))

        side1_max = max(side1.keys())
        side2_max = max(side2.keys())

        side1_prob = 1 / side1_max
        side2_prob = 1 / side2_max

        return pd.DataFrame({'side1_site': side1[side1_max],
                             'side2_site': side2[side2_max],
                             'side1_odds': side1_max,
                             'side2_odds': side2_max,
                             'side1_prob': side1_prob,
                             'side2_prob': side2_prob,
                             'comb_prob': side1_prob + side2_prob,
                             'site1_last_updated': data.loc[data['site'] == side1[side1_max]]['last_updated'].iloc[0],
                             'site2_last_updated': data.loc[data['site'] == side2[side2_max]]['last_updated'].iloc[0],
                             'active': 1,
                             },
                            index=[0])


    def best_odds(self):
        df = self.data_construction()

        out_df = df.groupby(['start_time', 'side1', 'side2']).apply(self._best_odds_grouper).reset_index()

        try:
            out_df.drop('level_3', axis=1, inplace=True)
        except KeyError as e:
            logger.info(e, exc_info=True)

        out_df.loc[:, 'arb_key'] = 'arb_' + out_df['side1'].apply(lambda x: x.split(' ')[-1]) + '_' +\
                                            out_df['side2'].apply(lambda x: x.split(' ')[-1])
        logger.info(f'Found best odds for {out_df.shape[0]} games')

        out_df.loc[out_df['comb_prob'] < self.configs['threshold']]

        return out_df


    def redis_loader(self):

        with redis.Redis(host=self.redis_url.hostname,
                         port=self.redis_url.port,
                         password=self.redis_url.password) as r:
            try:
                for _, vals in self.best_odds().iterrows():
                    r.set(vals['arb_key'], vals.drop('arb_key').to_json(), ex=14400) #4 hrs

                return 'Success'
            except Exception as e:
                logger.error(e, exc_info=True)
                return f'Failed: {e}'
