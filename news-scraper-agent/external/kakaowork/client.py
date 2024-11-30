import requests

from config.env_config import env
from config.log import logger
from external.kakaowork.message_blocks import KakaoworkMessageRequest

HTTP_METHOD_POST = "POST"
HTTP_CONTENT_TYPE = "application/json"

WEBHOOK_URL_MAP = {
    "real": env.KAWORK_WEBHOOK_REAL_URI,
    "dev": env.KAWORK_WEBHOOK_DEV_URI,
    "local": env.KAWORK_WEBHOOK_LOCAL_URI,
}


class KakaoworkClient:
    def __init__(self, profile: str):
        self.webhook_url = WEBHOOK_URL_MAP.get(profile)

    def send_message(self, request: KakaoworkMessageRequest) -> int:
        try:
            logger.info(
                f"raw request body: {request.model_dump_json(indent=2, exclude_none=True)}"
            )
            response = requests.post(
                self.webhook_url,
                headers={"Content-Type": "application/json"},
                data=request.model_dump_json(exclude_none=True),
            )
            # 응답 코드와 상세 정보 로깅
            logger.info(f"response status_code: {response.status_code}")
            logger.info(f"response body: {response.text}")  # 응답 본문 텍스트
            return response.status_code
        except requests.RequestException as e:
            logger.error(f"Error sending message: {e}")
            return 500  # 에러 상태 코드 반환
