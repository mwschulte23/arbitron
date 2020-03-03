import os
import logging

logging.basicConfig(
  level=logging.INFO,
  format='%(asctime)s - %(levelname)s - %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)




EMAIL_KEY = os.getenv('EMAIL_KEY')
SPORT_DICT = {'basketball_nba': 'nba', 'americanfootball_ncaaf': 'ncaaf', 'baseball_mlb': 'mlb',
              'basketball_euroleague': 'eurob', 'basketball_ncaab': 'ncaab', 'soccer_usa_mls': 'mls'}
