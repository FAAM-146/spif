from typing import Optional
from pydantic import Field, BaseModel

class VariableAttributes(BaseModel):
    class Config:
        # Configuration options here
        title = 'Variable Attributes'
        extra = 'allow'

    # Add your attributes here, e.g.
    #
    # my_attribute: str = Field(
    #   description='A description of my attribute',
    #   example='my_attribute_value'
    # )
    standard_name: Optional[str] = Field(
        description='Standard name for this variable',
        example='standard_name_value'
    )

    # blah: str = Field(
    #     description='blah',
    #     example='blah_value'
    # )
