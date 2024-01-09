import sys

from utils.logger import handle_exception, set_logger

logger = set_logger("./", "log.log")
sys.excepthook = handle_exception
if __name__ == "__main__":
    pass
