from http import HTTPStatus
from typing import Any

from fastapi import HTTPException


class BadRequest(HTTPException):
    def __init__(
        self, detail: Any | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTPStatus.BAD_REQUEST, detail, headers)


class NotFound(HTTPException):
    def __init__(
        self, detail: Any | None = None, headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(HTTPStatus.NOT_FOUND, detail, headers)
