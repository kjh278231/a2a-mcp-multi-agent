import os
import dotenv

dotenv.load_dotenv()


def get_env_variable(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        raise ValueError(
            f"{key} 환경 변수가 설정되지 않았습니다. .env 파일을 확인해주세요."
        )
    return value


OPENAI_API_KEY: str = get_env_variable("OPENAI_API_KEY")
GOOGLE_API_KEY: str = get_env_variable("GOOGLE_API_KEY")

NAVER_API_CLIENT_ID = get_env_variable("NAVER_API_CLIENT_ID")
NAVER_API_SECRET_KEY = get_env_variable("NAVER_API_SECRET_KEY")
FIRE_CRAWL_KEY = get_env_variable("FIRE_CRAWL_KEY")
