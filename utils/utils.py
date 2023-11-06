import sqlite3
import json
import os
import copy

from .graph import Graph


def load_db_data(db_path: str) -> dict[tuple[str, str], int]:
    """Extract all routes costs from the SQLite database and return the routes as a dictionnary.

    Args:
        db_path (str): The path to the database file.

    Returns:
        dict[tuple[str, str], int]: A dictionnary containing the routes that can be directly fed to a Graph object.
    """
    db_co = sqlite3.connect(db_path)
    cursor = db_co.cursor()

    try:
        cursor.execute('SELECT * FROM ROUTES')
        routes_dict = {}
        for row in cursor.fetchall():
            planet_1, planet_2, cost = row
            routes_dict[(planet_1, planet_2)] = cost

    except sqlite3.Error as e:
        print(f'Error executing SQL query: {e}')

    finally:
        cursor.close()
        db_co.close()

    return routes_dict


def get_db_path(millennium_falcon_path: str, db_relative_path: str) -> str:
    """Returns the path of the database file in regards to the path of the millennium falcon path.

    Args:
        millennium_falcon_path (str): The path of the millennium falcon file.
        db_relative_path (str): The relative path of the db file from the location of the millennium falcon file.

    Returns:
        str: The path of the database file.
    """
    return os.path.join(os.path.dirname(millennium_falcon_path), db_relative_path)


def load_from_json(path: str) -> dict:
    """Extracts the dictionnary from a json file.

    Args:
        path (str): The path of the json file.

    Returns:
        dict: The extracted dictionnary.
    """
    with open(path, 'r') as file:
        data_dict = json.loads(file.read())
    return data_dict


def load_json_data(millennium_falcon_path: str, empire_path: str) -> tuple[dict, dict]:
    """Loads the data from both the millennium falcon and empire json files.

    Args:
        millennium_falcon_path (str): The path of the millennium falcon json file.
        empire_path (str): The path of the empire json file.

    Returns:
        tuple[dict, dict]: The extracted dictionnaries.
    """
    millennium_falcon_dict = load_from_json(millennium_falcon_path)
    empire_dict = load_from_json(empire_path)
    return (millennium_falcon_dict, empire_dict)


class OddsComputer():
    """The computer used to compute the odds of reaching the goal planet.
    """
    def __init__(self, universe: Graph, start_planet: str, goal_planet: str, countdown: int, bounty_hunters: list[dict], init_autonomy: int) -> None:
        """Instantiates the computer and calculate and saves the odds and path.

        Args:
            universe (Graph): The graph object that represents the universe.
            start_planet (str): The name of the starting location.
            goal_planet (str): The name of the destination.
            countdown (int): The amount of days before anihilation of the destination.
            bounty_hunters (list[dict]): The list of location and schedule of the bounty hunters.
            init_autonomy (int): The autonomy of the falcon in days.
        """
        self._universe = universe
        self._goal_planet = goal_planet
        self._countdown = countdown
        self._bounty_hunters = bounty_hunters
        self._init_autonomy = init_autonomy
        self._odds = 0
        self._path = None

        # Compute the odds
        self._compute(start_planet, 0, self._init_autonomy, 0, [])


    @property
    def odds(self) -> float:
        """Getter for the vertices of the graph, decorated as a property for easy access.

        Returns:
            float: The computed odds of reaching the destination.
        """
        return self._odds


    @property
    def path(self) -> list[str]|None:
        """Getter for the vertices of the graph, decorated as a property for easy access.

        Returns:
            list[str]|None: The list of all planets on the path if it is possible to reach the destination, None otherwise.
        """
        return self._path


    def _compute(self, current_planet: str, current_day: int, current_autonomy: int, encountered_enemies: int, current_path: list[str]) -> None:
        """The recursive calculation function of the odds computer, which explores all possibilities and gives the best obtained odds and corresponding path.

        Args:
            current_planet (str): The current planet.
            current_day (int): The current day.
            current_autonomy (int): The remaining autonomy in days.
            encountered_enemies (int): How many enemies have been encountered on this search branch.
            current_path (list[str]): The path of this search branch.
        """
        if current_day > self._countdown or current_autonomy < 0:
            return
        
        if {'planet': current_planet, 'day': current_day} in self._bounty_hunters:
            encountered_enemies += 1

        current_path.append(current_planet)

        if current_planet == self._goal_planet:
            captured_odds = 0
            if encountered_enemies > 0:
                captured_odds += .1
                for k in range(2, encountered_enemies + 1):
                    captured_odds += (9.**(k-1)) / (10.**k)
            current_odds = 1 - captured_odds
            if current_odds > self._odds:
                self._odds = current_odds
                self._path = current_path
            return
        
        # Stay on current planet, either to avoid enemies or refuel
        self._compute(current_planet, current_day + 1, self._init_autonomy, encountered_enemies, copy.deepcopy(current_path))
        
        # Go to neighboring planet
        for (neighbor, travel_time) in self._universe.get_neighbors(current_planet):
            self._compute(neighbor, current_day + travel_time, current_autonomy - travel_time, encountered_enemies, copy.deepcopy(current_path))
        