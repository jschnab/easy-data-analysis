import yaml

from os import path as ospath
from pathlib import Path
from shutil import copyfile


transform_input = {
    "use_cols": lambda x: list(map(int, x.split())),
    "figure_size": lambda x: list(map(int, x.split())),
    "xcolumn": lambda x: x,
    "ycolumn": lambda x: x,
    "xlabel": lambda x: x,
    "ylabel": lambda x: x,
    "xlimit": lambda x: list(map(int, x.split())),
    "ylimit": lambda x: list(map(int, x.split())),
    "skip_header": lambda x: int(x),
    "legend_location": lambda x: x,
    "title": lambda x: x,
    "model": lambda x: True if x.lower() == 'true' else False,
}


class ConfigurationManager:
    def __init__(self):
        here = ospath.abspath(ospath.dirname(__file__))
        home = str(Path.home())
        self.config_user = ospath.join(home, ".edaconf")
        self.config_default = ospath.join(here, "config_default.yaml")
        if not ospath.exists(self.config_user):
            copyfile(self.config_default, self.config_user)

    def print_info(self):
        print()
        print(f"Configuration instructions")
        print("--------------------------")
        print("The current value is displayed between ( parentheses ).")
        print("The absence of value is indicated by 'None'.")
        print("Validate your choice by pressing <Enter>.")
        print()
        print("Possible actions:")
        print("* Keep the current value: leave the input field empty")
        print("* Modify the current value: type your input")
        print("* Enter a list of values: use a space to separate them")
        print("* Enter a void value: type 'none' (without quotes)")
        print()

    def record(self, subcommand):
        self.print_info()
        with open(self.config_user) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        inputs = {}
        for key, value in config["plot"][subcommand].items():
            while True:
                user_input = input(f"{key} ( {value} ): ")
                if not user_input:
                    inputs[key] = value
                    break
                elif user_input.lower() == "none":
                    inputs[key] = None
                    break
                try:
                    trans = transform_input[key](user_input)
                except ValueError:
                    print("Invalid value")
                    pass
                if key in ["use_cols", "figure_size", "xlimit", "ylimit"]:
                    if len(trans) != 2:
                        print("Invalid value")
                        continue
                inputs[key] = trans
                break
        config["plot"][subcommand] = inputs
        with open(self.config_user, "w") as f:
            yaml.dump(config, f, default_flow_style=False)

    def spectrum(self, subcommand):
        self.record(subcommand)

    def kinetics(self, subcommand):
        self.record(subcommand)

    def default(self, *args):
        with open(self.config_default) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        with open(self.config_user, "w") as f:
            yaml.dump(config, f, default_flow_style=False)
        print("Rolled back to default configuration")
