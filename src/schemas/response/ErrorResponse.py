from typing import Any, Optional
from dataclasses import dataclass, field


@dataclass
class ErrorResponse:
    message: str
    error_code: Optional[str] = None
    details: Optional[Any] = None
    success: bool = field(default=False, init=False)