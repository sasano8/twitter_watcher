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
    print(f"{interval}秒ごとに最新データを取得します")
    watcher = Watcher(*names)
    supervisor = asy.supervise(watcher)
    resutls = supervisor.run()
    print(resutls)


class Watcher:
    def __init__(self, *names: str, interval: int = 10):
        self.interval = interval
        self.api = get_api()
        self.readers = Reader.instatiate_by_names(*names)

    async def __call__(self, token):
        interval = self.interval
        api = self.api
        readers = self.readers

        print("監視対象の存在をチェックします")
        for reader in readers:
            print(f"{reader.home}: {await reader.exists(api)}")

        names = [x.home for x in readers]
        msg = "次のユーザーのツイートを監視します\n" + "\n".join(names)

        broadcast(msg)

        while not token.is_cancelled:
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

        broadcast("ツイートの監視を終了しました")


if __name__ == "__main__":
    typer.run(main)
