from pathlib import Path
from typing import Union

import aiofiles.os


async def path_exists(path: Union[Path, str]) -> bool:
    try:
        await aiofiles.os.stat(path)
    except OSError as e:
        return False
    except ValueError:
        return False
    return True


async def read_file(dir: Union[Path, str]) -> str:
    try:
        async with aiofiles.open(dir, "r") as f:
            return await f.read()
    except:
        raise Exception(f"Are you sure file '{dir}' exists?")
