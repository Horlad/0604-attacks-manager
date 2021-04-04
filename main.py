from loguru import logger
from attack import Attack
import concurrent.futures
import json
import argparse
import pathlib, os


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Automated attack manager for RNBO IR event')

    parser.add_argument('-c', '--configfile', nargs='?',
                        type = pathlib.Path,
                        default = os.path.join(os.path.dirname(__file__), 'attacks_config.json'),
                        help = "path to attacks config file. If it is not mentioned, it will take attacks_config.json from %(prog)s location directory")
    parser.add_argument('-l', '--log', nargs='?',
                        type = pathlib.Path,
                        default = os.path.dirname(__file__),
                        help = "path to log folder. If it is not mentioned, it create attacks_{time}.log files in %(prog)s location directory")
    #parser.add_argument('-t', '--teams', nargs = '*',
    #                    type = str,
    #                    help = "list of team names. ")
    parser.add_argument('-r', '--rotation',  
                        type = str,
                        default = "10 MB",
                        help = "defines how often to rotate log file")

    params = parser.parse_args()

    with open(params.configfile) as attack_settings:
        settings = json.load(attack_settings)
    
    logger.add(os.path.join(params.log, 'attacks_{time}.log'),
        colorize=True, enqueue=True, serialize=False,
        format="{time} {level} {message}",
        rotation=params.rotation)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for attack_setting in settings:
            executor.submit(Attack(**(attack_setting)).run_sheduled())