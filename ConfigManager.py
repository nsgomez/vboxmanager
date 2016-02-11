from yaml import load, dump
try:
    from yaml import CLoader as Loader
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Loader
    from yaml import Dumper

config_data = None
def get_data():
    if config_data is None:
        read_data()
        return config_data

def read_data():
    with open('config.yml', 'r') as f:
        config_data = f.read()
        config_data = load(config_data, Loader=Loader)        
