import time

from config.log import create_logger, default_logger


def log_time_agent_method(func):
    # agent 안에 있는 method에서 사용 (site도 함께 로깅)
    def wrapper(self, *args, **kwargs):
        has_site = hasattr(self, "site")
        logger = (
            self.logger if hasattr(self, "logger") and self.logger else default_logger
        )

        logger.info(
            f"Started {self.__class__.__name__} "
            f"{f'with site: {self.site.name}. ' if has_site else ''}"
        )

        start_time = time.time()
        result = func(self, *args, **kwargs)
        end_time = time.time()

        logger.info(
            f"Finished {self.__class__.__name__} "
            f"{f'with site: {self.site.name}. ' if has_site else ''}"
            f"({end_time - start_time:.2f}s)"
        )
        return result

    return wrapper


def log_time_method(func):
    # 일반적인 클래스 메서드에서 사용
    def wrapper(self, *args, **kwargs):
        logger = (
            self.logger if hasattr(self, "logger") and self.logger else default_logger
        )
        logger.info(f"Started {self.__class__.__name__}.{func.__name__}")

        start_time = time.time()
        result = func(self, *args, **kwargs)
        end_time = time.time()

        logger.info(
            f"Finished {self.__class__.__name__}.{func.__name__} ({end_time - start_time:.2f}s)"
        )
        return result

    return wrapper
