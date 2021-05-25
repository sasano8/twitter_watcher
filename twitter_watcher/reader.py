from . import config
import tweepy
from pydantic import BaseModel
import datetime

from . import config
from .parser import TweetText
from typing import List, Union
import logging

logger = logging.getLogger(__name__)


def get_api() -> tweepy.API:
    conf = config.TwitterConfig()
    auth = tweepy.OAuthHandler(conf.TWITTER_API_KEY, conf.TWITTER_API_SECRET)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        raise Exception("Error! Failed to get request token.")

    api = tweepy.API(auth)
    return api


class Reader(BaseModel):
    name: str
    latest_at: datetime.datetime = None

    @staticmethod
    def instatiate_by_names(*names: str) -> List["Reader"]:
        watchers = [Reader(name=name) for name in names]
        return watchers

    async def get_latest_tweet(self, api: tweepy.API) -> Union[TweetText, None]:
        # self.latest_at = self.latest_at or datetime.datetime.utcnow()
        self.latest_at = self.latest_at or datetime.datetime(datetime.MINYEAR, 1, 1)

        results = api.user_timeline(id=self.name)[:1]
        status = next(iter(results), None)

        if status:
            data = TweetText.parse(status)

        else:
            data = None

        if data and (self.latest_at < data.created_at):
            self.latest_at = data.created_at
            logger.critical(f"{self.latest_at} > {data.created_at}")
            return data
        else:
            return None

    async def get_latest_tweet_and_callback(self, api: tweepy.API, callback):
        data = await self.get_latest_tweet(api)
        if data:
            callback(data.summalize())

    async def get_latest_tweet_and_callback_async(self, api: tweepy.API, callback):
        data = await self.get_latest_tweet(api)
        if data:
            await callback(data.summalize())
