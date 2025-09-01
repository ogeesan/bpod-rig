"""Base classes for configuration classes"""

import datetime
from typing import Annotated, Union, Optional
from pydantic import BaseModel, Field, PastDate


class SettingsBase(BaseModel):
    creation_date: Annotated[
        Union[datetime.date, PastDate],
        Field(
            datetime.date.today(),
            title="Settings Creation Date",
            description="Date that this settings model was instantiated",
        ),
    ]

    save_date: Annotated[
        Optional[Union[datetime | PastDate]],  # Optional, but can be either type
        Field(
            title="Settings Save Date and Time",
            description="Date and time that this settings model was saved or updated.",
        ),
    ]

    author: Annotated[
        str,
        Field(
            ...,
            min_length=1,
            max_length=128,
            title="Username of settings creator",
            description="Username of the creator of this settings model.",
            alias="username",
        ),
    ]


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
