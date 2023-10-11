from pathlib import Path
from typing import Union

import aiofiles.os


async def path_exists(path: Union[Path, str]) -> bool:
    try:
        await aiofiles.os.stat(str(path))
    except OSError as e:
        return False
    except ValueError:
        return False
    return True