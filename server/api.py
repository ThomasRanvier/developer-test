from fastapi import FastAPI
from pydantic import BaseModel

from utils.utils import get_db_path, load_db_data, load_from_json, OddsComputer
from utils.graph import Graph
import os


app = FastAPI()


class RequestData(BaseModel):
    countdown: int
    bounty_hunters: list


class ResponseData(BaseModel):
    odds: float
    path: list[str]|None


@app.get('/')
def root():
    return 'Giskard development test'


@app.post('/compute_odds', response_model=ResponseData)
async def compute_odds(request: RequestData) -> None:
    """Compute the odds of reaching the destination before anihilation.

    Args:
        request (RequestData): The empire.json data used to compute the odds.
    """
    # Loading millenium and db data here to allow modifying files while the web servive is running
    millennium_falcon_dict = load_from_json('/data/millennium-falcon.json')
    routes_dict = load_db_data('/data/universe.db')
    empire_dict = request.dict()

    universe = Graph()
    universe.process_routes_dict(routes_dict)
    computer = OddsComputer(universe, millennium_falcon_dict['departure'], millennium_falcon_dict['arrival'],
                            empire_dict['countdown'], empire_dict['bounty_hunters'], millennium_falcon_dict['autonomy'])

    return {'odds': computer.odds, 'path': computer.path}


if __name__ == '__main__':
    app.run(debug=True)