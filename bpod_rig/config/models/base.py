"""Base classes for configuration classes"""

import datetime
from typing import Annotated, Union, Optional, Any

import pydantic.types
from pydantic import BaseModel, Field, PastDate, validator, field_validator


class SettingsBase(BaseModel):
    creation_date: Annotated[
        Union[datetime.date, PastDate],
        Field(
            title="Settings Creation Date",
            description="Date that this settings model was instantiated",
        ),
    ] = datetime.date.today()

    save_datetime: Annotated[
        Optional[
            Union[datetime.datetime, PastDate]
        ],  # Optional, but can be either type
        Field(
            None,
            title="Settings Save Date and Time",
            description="Date and time that this settings model was saved or updated.",
        ),
    ] = None

    username: Annotated[
        str,
        Field(
            min_length=1,
            max_length=128,
            title="Username of settings creator",
            description="Username of the creator of this settings model.",
        ),
    ] = "BpodUser"

    # noinspection PyNestedDecorators
    @field_validator("creation_date", mode="after")
    @classmethod
    def validate_nonfuture(cls, value: datetime.date) -> datetime.date:
        if value > datetime.date.today():
            raise ValueError(f'Provided creation_date {value} cannot be in the future!')
        return value

    # noinspection PyNestedDecorators
    @field_validator("save_datetime", mode="after")
    @classmethod
    def validate_nonfuture_datetime(cls, value: datetime.datetime) -> datetime.datetime:
        if value > datetime.datetime.now():
            raise ValueError(f'Provided save_datetime {value} cannot be in the future!')
        return value




class ModuleBase(SettingsBase):
    name: Annotated[
        str,
        Field(
            title="Module Name",
            description="Name of module associated with this configuration",
        ),
    ]
    USB_port: Annotated[
        str, Field(title="USB Port", description="Last used USB port for this module")
    ]
