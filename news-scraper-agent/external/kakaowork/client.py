import requests

from config.env_config import env
from config.log import ConsoleDataType, NewsScraperAgentLogger
from decorations.log_time import log_time_method
from external.kakaowork.message_blocks import KakaoworkMessageRequest

HTTP_METHOD_POST = "POST"
HTTP_CONTENT_TYPE = "application/json"

WEBHOOK_URL_MAP = {
    "prod": env.KAWORK_WEBHOOK_PROD_URI,
    "dev": env.KAWORK_WEBHOOK_DEV_URI,
    "local": env.KAWORK_WEBHOOK_LOCAL_URI,
}


class KakaoworkClient:
    def __init__(self, profile: str):
        self.webhook_url = WEBHOOK_URL_MAP.get(profile)
        self.logger = NewsScraperAgentLogger(self.__class__.__name__)

    @log_time_method
    def send_message(self, request: KakaoworkMessageRequest) -> int:
        try:
            self.logger.info("request body 👇")
            self.logger.console_print(
                ConsoleDataType.DICT, request.model_dump(exclude_none=True)
            )

            response = requests.post(
                self.webhook_url,
                headers={"Content-Type": "application/json"},
                data=request.model_dump_json(exclude_none=True),
            )
            # 응답 코드와 상세 정보 로깅
            self.logger.info(f"response status_code: {response.status_code}")
            self.logger.info("response body 👇")  # 응답 본문 텍스트
            self.logger.console_print(ConsoleDataType.DICT, response.json())
            return response.status_code
        except requests.RequestException as e:
            self.logger.error(f"Error sending message: {e}")
            return 500  # 에러 상태 코드 반환
