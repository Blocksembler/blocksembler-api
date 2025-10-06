from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TanRead(BaseModel):
    code: str
    valid_from: Optional[datetime]
    valid_to: Optional[datetime]
