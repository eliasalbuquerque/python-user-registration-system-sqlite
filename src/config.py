import json

class Config:
    def __init__(self, config_path="src/config.json"):
        self.config_path = config_path
        with open(self.config_path, "r") as f:
            self.config = json.load(f)

    def save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)

    @property
    def db_path(self):
        return self.config["db_path"]

    @property
    def show_startup_message(self):
        return self.config["show_startup_message"]

    @show_startup_message.setter
    def show_startup_message(self, value):
        self.config["show_startup_message"] = value
        self.save_config()
