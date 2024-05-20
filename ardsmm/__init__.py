import json
import sys
from typing import Any
from ardsmm._version import __version__, __version_tuple__


class ArmaConfigMod:
    data: dict[Any, Any]
    MOD_SCHEMA = {
        "modId": str,
        "name": str,
        "version": str,
    }

    def __init__(self, mod_dict):
        if isinstance(mod_dict, str):
            if mod_dict.endswith(","):
                mod_dict = mod_dict[:-1]
            self.data = json.loads(mod_dict)
        else:
            self.data = mod_dict
        self.check()

    def check(self):
        for key, expected_type in self.MOD_SCHEMA.items():
            if key not in self.data.keys():
                raise KeyError(f"Mod key '{key}' is missing")
            elif expected_type is not type(self.data[key]):
                raise TypeError(f"Mod '{key}' value should be {expected_type}, but got {type(self.data[key])}")


class ArmaConfig:
    mods: list[Any]
    data: dict[Any, Any]
    file: str
    DEFAULT_INDENT = 4

    def __init__(self, configfile):
        self.file = configfile
        self.data = {}
        self.mods = []
        self.read()

    def read(self):
        with open(self.file, "r") as fp:
            self.data = json.load(fp)

        if not self.data.get("game"):
            self.data["game"] = {}
            if not self.data["game"].get("mods"):
                self.data["game"]["mods"]: []

        for mod in self.data["game"]["mods"]:
            self.mods.append(ArmaConfigMod(mod))

    def to_string(self, indent=DEFAULT_INDENT):
        return json.dumps(self.data, indent=indent)

    def append_mod(self, s):
        mod = ArmaConfigMod(s)

        if mod.data["name"] in [x.data["name"] for x in self.mods]:
            print(f"[Skip  ] {mod.data['name']} exists", file=sys.stderr)
            return
        print(f"[Append] {mod.data['name']}", file=sys.stderr)
        self.mods.append(mod)

    def update(self):
        self.data["game"]["mods"] = sorted(
            [x.data for x in self.mods],
            key=lambda y: y["name"]
        )
