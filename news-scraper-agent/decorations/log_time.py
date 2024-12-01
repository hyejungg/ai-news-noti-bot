import time

from config.log import create_logger, default_logger


def log_time_agent_method(func):
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
            f"Time taken: {end_time - start_time:.2f} seconds"
        )
        return result

    return wrapper
