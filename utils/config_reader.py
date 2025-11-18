import configparser

class Config:
    def _initialize(self):
        self.config = configparser.ConfigParser()
        self.config.read('configs/config.ini')

    def get_config(self, section, option):
        return self.config.get(section, option)