import configparser

class Config:

    def __init__(self):
        self.config = configparser.ConfigParser().read('config.ini')['default']

    def get_log_file(self):
        return self.config['debug_log']

    def get_key(self):
        return self.config['key']

    def get_endpoint(self):
        return self.config['endpoint']
