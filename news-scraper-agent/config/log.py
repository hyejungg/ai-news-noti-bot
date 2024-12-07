import logging
from config.env_config import env
from datetime import datetime
from enum import EnumType
from rich.console import Console
from rich.json import JSON
from rich.logging import RichHandler
from rich.table import Table
from rich.text import Text
from typing import Any
from zoneinfo import ZoneInfo  # Python 3.9 이상에서 사용 가능


class ConsoleDataType(EnumType):
    TABLE = "TABLE"
    JSON = "JSON"
    TEXT = "TEXT"
    DICT = "DICT"


class KSTFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        # KST로 시간 변환
        dt = datetime.fromtimestamp(record.created, tz=ZoneInfo("Asia/Seoul"))
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()


# Formatter 설정
formatter = KSTFormatter(
    fmt="%(asctime)s - %(name)16s - %(levelname)7s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Logger 설정
default_logger = logging.getLogger("NewsScraperAgent")
default_logger.setLevel(logging.DEBUG if env.PROFILE != "real" else logging.INFO)

# RichHandler 추가
console = Console()
rich_handler = RichHandler(rich_tracebacks=True, console=console)
rich_handler.setLevel(logging.DEBUG)
rich_handler.setFormatter(formatter)
default_logger.addHandler(rich_handler)


# logger 객체 추가
def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if env.PROFILE != "real" else logging.INFO)
    logger.addHandler(rich_handler)
    return logger


def to_console_text(data_type: ConsoleDataType, data: Any):
    with console.capture() as capture:
        if data_type == ConsoleDataType.TABLE and isinstance(data, Table):
            console.print(data)
        elif data_type == ConsoleDataType.JSON:
            console.print(JSON.from_data(data))  # json 문자열로 표시 (" 포함)
        elif data_type == ConsoleDataType.DICT:
            console.print(JSON.from_data(data))  # dict를 json 형태로 예쁘게 표시
        elif data_type == ConsoleDataType.TEXT:
            console.print(data)
    return Text.from_ansi(capture.get())


def console_print(data_type: ConsoleDataType, data: Any, logger: logging.Logger = None):
    display_text = to_console_text(data_type, data)
    if logger is None:
        default_logger.info(f"{display_text}")
    else:
        logger.info(f"{display_text}")


if __name__ == "__main__":
    # 로그 테스트 (python -m config.log)
    default_logger.debug("Debug message")
    default_logger.info("Info message")
    default_logger.warning("Warning message")
    default_logger.error("Error message")
    default_logger.critical("Critical message")
