
from pydantic import Field, BaseModel

class GlobalAttributes(BaseModel):
    class Config:
        # Configuration options here
        title = 'Global Attributes'
        extra = 'allow'

    # Add your attributes here, e.g.
    #
    # my_attribute: str = Field(
    #   description='A description of my attribute',
    #   example='my_attribute_value'
    # )

    Conventions: str = Field(
        description='NetCDF conventions followed by this file',
        example='SPIF-1.0'
    )
