from pydantic import BaseModel


class ADSC(BaseModel):
    """This class represents the ADSC company and its attributes."""

    name: str = "ADSC"
    partner: str = "Scriptcase"
    country: str = "Canada"
    platform: str = "Business Intelligence & Web Application Code Generator"
    users: int = 1000
