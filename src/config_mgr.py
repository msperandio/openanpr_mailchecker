import json

class ConfigMgr:
    CONFIG_FILENAME = "data/config.json"
    config = {}
    def __init__(self):
        self.load_config()

    def load_config(self):
        try:
            # Opening JSON file
            f = open(self.CONFIG_FILENAME)
            # returns JSON object as
            # a dictionary
            self.config = json.load(f)
            # Closing file
            f.close()
        except FileNotFoundError:
            with open(self.CONFIG_FILENAME, 'w') as fp:
                json.dump({}, fp)
