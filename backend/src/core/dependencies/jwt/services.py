from typing import Callable

from services.jwt import TokenService


def get_token_service_factory() -> Callable[[], TokenService]:
    return lambda: TokenService()
