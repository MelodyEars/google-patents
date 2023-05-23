import asyncio
import subprocess
from pathlib import Path

import aiohttp
from aiohttp import ClientSession
from fake_useragent import UserAgent
from loguru import logger


FILE_COUNT = 1
COUNT_ACCOUNT = 1

ROOT_DIR = Path(__file__).parent


def file_exists(path_to_file: str | Path) -> bool:
    """Check file exists by path"""
    path = Path(path_to_file)

    if path.is_file():
        return True
    else:
        return False


def dir_exists(path_to_dir: str | Path) -> bool:
    """Check directory exists by path"""
    path = Path(path_to_dir)

    if path.is_dir():
        return True
    else:
        return False



def auto_create(path: Path, _type: str, hidden=False):
    """
    @_type=file
    @_type=dir
    """

    if _type == "file":

        if not file_exists(path):
            open(path, "a+", encoding="utf8", errors="ignore").close()

            if hidden:
                subprocess.call("attrib +h " + str(path))

    elif _type == "dir":
        if not dir_exists(path):
            path.mkdir(parents=True, exist_ok=True)
            '''Параметр parents=True дозволяє створювати всі проміжні папки, якщо вони не існують.
             Параметр exist_ok=True дозволяє не викидати помилку, якщо шлях вже існує 
             (наприклад, якщо його створила інша операція паралельно).'''

            if hidden:
                subprocess.call("attrib +h " + str(path))

    else:
        raise Exception(f"Invalid flag _type='{_type}'")

    return path


def write_line(filename, list_line):
    """Writes line in file. Rewrite all info in the file."""
    with open(filename, "w+", encoding="utf8", errors="ignore") as file:
        if isinstance(list_line, list):
            list_line = (line for line in list_line if line.strip())

            file.seek(0)
            file.truncate()
            file.write("\n".join(str(line) for line in list_line))

        elif isinstance(list_line, str):
            file.seek(0)
            file.truncate()
            file.write(list_line + "\n")

def get_str_file(path_to_file) -> str:
    if file_exists(path_to_file):
        with open(path_to_file, "r", encoding="utf8",) as file:
            content = file.read()

        return content
    else:
        raise Exception(f'Not found {path_to_file}')


def del_all_responses():
    folder_with_resps = ROOT_DIR / "responses"
    folder_with_resps.unlink()


async def fetch(session, url, proxy_link, auth, retries=3):
    global FILE_COUNT

    for retry in range(retries):
        try:
            async with session.get(url, headers={'User-Agent': UserAgent().random}) as response:
                filepath: Path = auto_create(ROOT_DIR / "responses", _type="dir") / f"output{FILE_COUNT}.html"
                html_to_file = await response.text()

                write_line(filepath, html_to_file)
                html = get_str_file(filepath)

                FILE_COUNT += 1

                if not ('page not found' in html and html is None):
                    return html

                logger.error(f"page not found: {url}")
                await asyncio.sleep(2)

        except Exception as e:
            if retry == retries - 1:  # If this was the last attempt
                raise e  # Then raise the exception to the caller
            else:
                logger.error(f"Attempt {retry+1} failed, retrying after delay...")
                await asyncio.sleep(2**(retry+1))  # Exponential backoff delay

    return await fetch(session, url)


async def get_patents(proxy_link, auth):
    url = f"https://vladey.net/en/artist/doping-pong"
    async with ClientSession() as session:
        html = await fetch(session, url, proxy_link, auth)
        print(html)

def sync_get_patents(proxy_link, auth):
    try:
        asyncio.run(get_patents(proxy_link, auth))

    finally:
        del_all_responses()


if __name__ == '__main__':
    # host = 'zproxy.lum-superproxy.io'
    # port = 22225
    # user = 'brd-customer-hl_2ea60b2d-zone-zone12'
    # password = '5ly8cts13myu'
    #
    # proxy_link = f"http://{host}:{port}"
    # auth = aiohttp.BasicAuth(user, password)
    proxy_link = None
    auth = None

    sync_get_patents(proxy_link, auth)

