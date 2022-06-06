import os


def parse_dev_mode() -> bool:
    dev_mode_str: str = os.getenv("DEV_MODE")

    if dev_mode_str == "True":
        return True
    elif dev_mode_str == "False":
        return False
    else:
        return True


class Config:
    def __init__(self):
        self.SECRET_KEY = os.getenv("SECRET_KEY", "flytospace")
        self.DB_URL = os.getenv("DB_URL", "sqlite+aiosqlite:///test.db")
        self.DEV_MODE = parse_dev_mode()


config = Config()
