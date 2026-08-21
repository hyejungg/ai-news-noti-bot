import json
import logging
from config.env_config import env
from datetime import datetime, timezone, timedelta
from enum import Enum
from rich.console import Console
from rich.json import JSON
from rich.logging import RichHandler
from rich.table import Table
from rich.text import Text
from typing import Any

KST = timezone(timedelta(hours=9))


class ConsoleDataType(Enum):
    TABLE = "TABLE"
    JSON = "JSON"
    TEXT = "TEXT"
    DICT = "DICT"


class JsonLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log = {
            "timestamp": datetime.fromtimestamp(record.created, tz=KST).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log["exception"] = self.formatException(record.exc_info)
        return json.dumps(log, ensure_ascii=False)


class NewsScraperAgentLogger(logging.Logger):
    def __init__(self, name: str = "NewsScraperAgent"):
        super().__init__(name)

        self.console = Console()
        self._initialize_logger()

    def _initialize_logger(self):
        # Logger 레벨 설정
        self.setLevel(logging.DEBUG if env.PROFILE != "prod" else logging.INFO)

        if env.PROFILE in ("dev", "prod"):
            # dev/prod 환경에서는 CloudWatch 조회를 위해 JSON 형태로 로그 출력
            json_handler = logging.StreamHandler()
            json_handler.setLevel(logging.DEBUG)
            json_handler.setFormatter(JsonLogFormatter())
            self.addHandler(json_handler)
            return

        # Formatter 설정
        formatter = logging.Formatter(fmt="%(name)16s - %(message)s")

        # RichHandler 추가
        rich_handler = RichHandler(
            rich_tracebacks=True,
            console=self.console,
            log_time_format=lambda dt: Text(
                datetime.fromtimestamp(dt.timestamp(), tz=KST).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            ),
        )
        rich_handler.setLevel(logging.DEBUG)
        rich_handler.setFormatter(formatter)
        self.addHandler(rich_handler)

    def console_print(self, data_type: ConsoleDataType, data: Any):
        display_text = self._to_console_text(data_type, data)
        self.info(f"{display_text}")

    def _to_console_text(self, data_type: ConsoleDataType, data: Any):
        with self.console.capture() as capture:
            if data_type == ConsoleDataType.TABLE and isinstance(data, Table):
                self.console.print(data)
            elif data_type == ConsoleDataType.JSON:
                self.console.print(JSON.from_data(data))  # JSON 문자열로 표시 (" 포함)
            elif data_type == ConsoleDataType.DICT:
                self.console.print(
                    JSON.from_data(data)
                )  # dict를 JSON 형태로 예쁘게 표시
            elif data_type == ConsoleDataType.TEXT:
                self.console.print(data)
        return Text.from_ansi(capture.get())


if __name__ == "__main__":
    # 로그 테스트 (python -m config.log)
    logger = NewsScraperAgentLogger("NewsScraperAgent")

    # 로그 메시지 테스트
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")

    # console_print 사용 예시
    sample_data = {"key": "value", "another_key": "another_value"}
    logger.console_print(ConsoleDataType.DICT, sample_data)
