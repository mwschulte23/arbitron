import json
from fastapi import FastAPI
from pydantic import BaseModel

from src.arb_finder import ArbFinder


class RunParams(BaseModel):
    sport: str = 'basketball_nba'
    mkt: str = 'h2h'


app = FastAPI()


@app.post('/run')
async def post_run(sport: str = 'basketball', mkt: str = 'h2h'):
    with open('configs.json') as f:
        configs = json.load(f)

    af = ArbFinder(configs, sport=sport, mkt=mkt)
    result = af.redis_loader()

    return {'result': result, 'sport': sport, 'mkt': mkt}


@app.get('/run')
async def get_run(sport: str = 'basketball', mkt: str = 'h2h'):
    return {'sport': sport, 'mkt': mkt}