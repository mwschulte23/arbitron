import os
import argparse
from urllib import parse

from src import logger
from src.arb_finder import ArbFinder

# wrapper script - can run up to 8 API calls per run @ twice hourly


class Runner:
    def __init__(self, arb_finder, sport='basketball_nba', mkt='h2h'):
        self.arb_finder = arb_finder
        self.api_key = os.getenv('API_KEY')
        self.redis_url = parse.urlparse(os.getenv('REDIS_URL'))
        self.sport = sport
        self.mkt = mkt
        self.args = self._cli_args()


    def __str__(self):
        pass


    def _cli_args(self):
        # currently not implemented
        parser = argparse.ArgumentParser(description='parameters for running etl from cli')
        parser.add_argument('--sport_type', '-s',
                            default='basketball_nba',
                            type=str,
                            help=''
                            )
        parser.add_argument('--odds_type', '-o',
                            default='h2h',
                            type=str,
                            help=''
                            )
        return parser.parse_args()


    def runner(self, arb_finder):
        af = arb_finder(self.api_key,
                        self.redis_url,
                        sport=self.sport,
                        mkt=self.mkt
                        )
        af.redis_loader()


# if __name__ == '__main__':
#     run = Runner()
#     run.runner(ArbFinder)