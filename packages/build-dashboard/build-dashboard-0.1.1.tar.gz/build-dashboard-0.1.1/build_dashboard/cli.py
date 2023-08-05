from os import environ, path
from argparse import ArgumentParser
import asyncio
import logging
import toml
from build_dashboard.model import BuildbotModel, BuildbotClient
from build_dashboard.screen import draw_screen
from build_dashboard import logger


def main():
    parser = ArgumentParser(prog='build_dashboard', description='A buildbot client')
    parser.add_argument('--unix', help='Unix domain socket to connect through', type=str)
    parser.add_argument('--config', help='Config file to use', type=str)
    parser.add_argument('--protocol', help='Connection protocol (Default: http)', type=str)
    parser.add_argument('--host', help='Buildbot master hostname', type=str)
    parser.add_argument('--log', help='Writes logs to file for debugging', type=str)
    parser.add_argument('--update-interval', help='Update interval', type=str)
    args = parser.parse_args()
    
    config_file = None
    if args.config:
        config_file = args.config
    elif environ.get('HOME') != None:
        config_file = environ.get('HOME') + '/.buildbotrc'

    config = {}

    if (config_file is not None and
            path.exists(config_file)):
        with open(config_file) as f:
            config.update(toml.load(f))

    for key in vars(args):
        value = getattr(args, key)
        if value != None:
            config[key] = value
    
    if 'log' in config:
        handler = logging.FileHandler(config['log'])
        formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    client = BuildbotClient(
            path=config.get('unix', None), 
            protocol=config.get('protocol', 'http'),
            host=config.get('host', 'localhost'))
    
    model = BuildbotModel(client)
    
    loop = asyncio.get_event_loop()
    draw_screen(model, loop, config.get('update-interval', 5))
