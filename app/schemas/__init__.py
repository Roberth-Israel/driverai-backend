from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Any


class ApiModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def _coerce_id(cls, v: Any) -> str:
        return str(v) if isinstance(v, UUID) else v
