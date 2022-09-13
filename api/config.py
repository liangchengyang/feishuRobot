from os import getenv

from pydantic import BaseSettings


class Settings(BaseSettings):
    ENV = "test"
    PROJECT_NAME: str = "feishuRobot"
    ROBOT_WEBHOOK: str = "https://open.feishu.cn/open-apis/bot/v2/hook/74cfb77f-6958-4d19-aba4-f59de0783fc0"


class OnlineSettings(Settings):
    ENV = "prod"


settings = Settings() if getenv("ENV", "test") == "test" else OnlineSettings()
