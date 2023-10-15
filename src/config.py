import configparser
from enum import Enum
from typing import Union

import aiofiles
import yaml

from filemanager import path_exists

CONFIG_FILE = "settings.yml"
CONFIG = {}


class ConfigSections(Enum):
    Esound = None
    YTMusic = None


class Config:
    def __init__(self):
        self.config = {}

    async def _load_config(self) -> None:
        async with aiofiles.open(CONFIG_FILE, "r") as f:
            self.config = yaml.load(await f.read(), Loader=yaml.Loader)
            await f.close()

    async def initialize(self):
        if await path_exists(CONFIG_FILE):
            await self._load_config()
            return

        async with aiofiles.open(CONFIG_FILE, "w") as f:
            config = {
                "Esound": {
                    "email": "",
                    "password": ""
                }
            }

            yaml_output = yaml.dump(config)

            await f.write(yaml_output)
            await f.close()

    async def add_key(self, key: str, value: Union[str, int, list, map], section: ConfigSections) -> None:
        async with aiofiles.open(CONFIG_FILE, "r") as f:
            raw_config = await f.read()

            config = yaml.load(raw_config, Loader=yaml.Loader)

            async with aiofiles.open(CONFIG_FILE, "w") as fr:
                config[section.name][key] = value

                CONFIG = config

                await fr.write(yaml.dump(config))
                await fr.close()
                await f.close()
