from typing import Optional

from pydantic import BaseModel

class Dashboard(BaseModel):
    result: str