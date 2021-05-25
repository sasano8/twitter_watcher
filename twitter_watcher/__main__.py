import typer
from typing import List
import asyncio
import asy
import logging

from .reader import get_api, Reader
from .notify import broadcast

app = typer.Typer()

logger = logging.getLogger(__name__)


@app.command()
def main(names: List[str], interval: int = 10):
    watcher = Watcher(*names)
    supervisor = asy.supervise(watcher)
    resutls = supervisor.run()
    print(resutls)


class Watcher:
    def __init__(self, *names: str, interval: int = 10):
        self.interval = interval
        self.api = get_api()
        self.readers = Reader.instatiate_by_names(*names)

    async def __call__(self):
        interval = self.interval
        api = self.api
        readers = self.readers

        while True:
            logger.info("try retrive latest messages.")
            for reader in readers:
                try:
                    data = await reader.get_latest_tweet_and_callback(api, broadcast)
                except Exception as e:
                    logger.critical(e, exc_info=True)
                    try:
                        broadcast(str(e))
                    except:
                        pass
            await asyncio.sleep(interval)


if __name__ == "__main__":
    typer.run(main)
