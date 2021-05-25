from pydantic import BaseSettings, Field


class TwitterConfig(BaseSettings):
    class Config:
        env_file = ".env"

    TWITTER_API_KEY: str
    TWITTER_API_SECRET: str
    # TWITTER_BEARER_TOKEN: str


class LineChannelConfig(BaseSettings):
    class Config:
        env_file = ".env"

    LINE_CHANNEL_ACCESS_TOKEN: str


class AllConfig(BaseSettings):
    twitter: TwitterConfig = Field(default_factory=TwitterConfig)
    line_channel: LineChannelConfig = Field(default_factory=LineChannelConfig)
