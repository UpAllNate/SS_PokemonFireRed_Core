
from src.ss_logging.spoken_screen_logger import logger

class SafeGlobals():

    safe_globals = {}

    @classmethod
    def register(clsself, cls):
        SafeGlobals.safe_globals[cls.__name__] = cls
        logger.op.info(f"Safe Method added: {cls.__name__}")