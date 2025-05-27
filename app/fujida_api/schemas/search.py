from pydantic import BaseModel
from typing import Optional, List


class DeviceSpecOut(BaseModel):
    name: str
    value: Optional[str] = None


class DeviceSearchResult(BaseModel):
    id: int
    name: str
    specs: List[DeviceSpecOut]
