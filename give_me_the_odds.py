import argparse

from utils.utils import get_db_path, load_db_data, load_json_data, OddsComputer
from utils.graph import Graph


def main(millennium_falcon_path: str, empire_path: str) -> None:
    """Main function of the CLI, loads the data, computes the odds and path and print important informations.

    Args:
        millennium_falcon_path (str): The path of the millennium falcon json file.
        empire_path (str): The path of the empire json file.
    """
    millennium_falcon_dict, empire_dict = load_json_data(millennium_falcon_path, empire_path)
    db_path = get_db_path(millennium_falcon_path, millennium_falcon_dict['routes_db'])
    routes_dict = load_db_data(db_path)
    
    universe = Graph()
    universe.process_routes_dict(routes_dict)
    print(f'Universe:\n{universe}\n')

    print(f'Goal: reach {millennium_falcon_dict["arrival"]} from {millennium_falcon_dict["departure"]} under' +
          f' {empire_dict["countdown"]} days, with {millennium_falcon_dict["autonomy"]} days of fuel autonomy.\n')

    computer = OddsComputer(universe, millennium_falcon_dict['departure'], millennium_falcon_dict['arrival'],
                            empire_dict['countdown'], empire_dict['bounty_hunters'], millennium_falcon_dict['autonomy'])

    if computer.odds > 0:
        print(f'Answer: Odds of reaching the destination are {int(computer.odds*100)}% by following the path {" -> ".join(computer.path)}.')
    else:
        print('Answer: The computer did not find a way to reach the destination before the Death Star annihilates it.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('millennium_falcon_path', type=str, help='Path to the millennium-falcon.json file')
    parser.add_argument('empire_path', type=str, help='Path to the empire.json file')
    args = vars(parser.parse_args())

    main(**args)