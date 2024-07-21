from loguru import logger
from utils.sync import sync_clipboard


def main() -> None:
    logger.info("Start syncing clipboard")
    try:
        sync_clipboard()
    except Exception as e:
        logger.exception(e)
        logger.info("Shut down sync clipboard process...")


if __name__ == "__main__":
    main()
