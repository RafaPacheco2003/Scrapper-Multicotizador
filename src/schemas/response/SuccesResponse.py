from typing import Any, Optional
from dataclasses import dataclass, field


@dataclass
class SuccessResponse:
    message: str
    data: Optional[Any] = None
    success: bool = field(default=True, init=False)