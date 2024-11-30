import logging
from datetime import datetime


from zoneinfo import ZoneInfo  # Python 3.9 이상에서 사용 가능

from config.env_config import env


class KSTColorFormatter(logging.Formatter):
    # ANSI 코드 색상 정의
    COLORS = {
        "DEBUG": "\033[90m",  # 회색
        "INFO": "",  # 변경 없음
        "WARNING": "\033[93m",  # 노란색
        "ERROR": "\033[91m",  # 빨간색
        "CRITICAL": "\033[41m",  # 빨간 배경 (심각한 오류)
    }
    RESET = "\033[0m"  # 색상 초기화

    def formatTime(self, record, datefmt=None):
        # KST로 시간 변환
        dt = datetime.fromtimestamp(record.created, tz=ZoneInfo("Asia/Seoul"))
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()

    def format(self, record):
        # 레벨에 따른 색상 추가
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.msg = f"{log_color}{record.msg}{self.RESET}"  # 메시지에 색상 적용
        return super().format(record)


formatter = KSTColorFormatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Logger 설정
default_logger = logging.getLogger("NewsScraperAgent")

if env.PROFILE == "real":
    default_logger.setLevel(logging.INFO)
else:
    default_logger.setLevel(logging.DEBUG)


# Console Handler 추가
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)  # DEBUG 이상만 받는 핸들러

handler.setFormatter(formatter)


def create_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO if env.PROFILE == "real" else logging.DEBUG)
    logger.addHandler(handler)
    return logger


if __name__ == "__main__":
    # 로그 테스트 (python -m config.log)
    default_logger.debug("Debug message")
    default_logger.info("Info message")
    default_logger.warning("Warning message")
    default_logger.error("Error message")
    default_logger.critical("Critical message")
