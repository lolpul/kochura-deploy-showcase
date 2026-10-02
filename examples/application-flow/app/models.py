from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ApplicationInput(BaseModel):
    model_config = ConfigDict(
        extra="forbid", str_strip_whitespace=True, frozen=True
    )

    task: str = Field(min_length=3, max_length=120)
    units: int = Field(strict=True, ge=1, le=20)


class SavedApplication(BaseModel):
    model_config = ConfigDict(frozen=True)

    number: int
    request: ApplicationInput


class Acceptance(BaseModel):
    model_config = ConfigDict(frozen=True)

    application_number: int
    notification: Literal["delivered", "unavailable"]
