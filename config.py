import os


def parse_bool(env_variable: str) -> bool:
    env_str: str = os.getenv(env_variable)

    if env_str == "True":
        return True
    elif env_str == "False":
        return False
    else:
        return True


class Config:
    def __init__(self):
        self.SECRET_KEY: str = os.getenv("SECRET_KEY", "flytospace")
        self.DB_URL: str = os.getenv("DB_URL", "sqlite+aiosqlite:///test.db")
        self.REDIS_URL: str = os.getenv("REDIS_URL", None)
        self.DEV_MODE: bool = parse_bool("DEV_MODE")
        self.LIMITER_ENABLED: bool = parse_bool("LIMITER_ENABLED")
        self.DEFAULT_LIMIT: str = os.getenv("DEFAULT_LIMIT", "10/minute")
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
