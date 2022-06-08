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
        self.SECRET_KEY: str = os.getenv("SECRET_KEY", "flytospace")
        self.DB_URL: str = os.getenv("DB_URL", "sqlite+aiosqlite:///test.db")
        self.REDIS_URL: str = os.getenv("REDIS_URL", None)
        self.DEV_MODE: bool = parse_dev_mode()
        self.TITLE: str = "FlyAPI"
        self.DESCRIPTION: str = """
        FlyAPI is a REST-style service created to faciliate the sharing of custom content for Fly Dangerous
        
        ## Ships
        
        You can define custom Ships in JSON, upload them, and search for them
        
        ## Courses
        
        You can define custom courses in JSON and add metadata about length and difficulty
        
        ## Collections
        
        You can define custom collections and add courses by any user (even deleted ones!) to a collection
        """


config = Config()
