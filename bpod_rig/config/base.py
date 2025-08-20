"""Base classes for configuration classes"""
from pydantic import BaseModel, PastDate

class SettingsBase(BaseModel):
    creation_date: PastDate
    save_date: PastDate
    author: str  # Username of settings creator

class ModuleBase(BaseModel, SettingsBase):
    name: str
    USB_port: str
