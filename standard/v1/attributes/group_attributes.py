
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict
from vocal.field import Field

class GenericGroupAttributes(BaseModel):
    model_config = ConfigDict(
        # Configuration options here
        title='Group Attributes',
        extra='allow'
    )

    # Add your attributes here, e.g.
    #
    # my_attribute: str = Field(
    #   description='A description of my attribute',
    #   example='my_attribute_value'
    # )
    spif_group_type: Literal['other']

class CoreGroupAttributes(BaseModel):
    model_config = ConfigDict(
        title='Core Group Attributes',
        extra='allow'
    )

    spif_group_type: Literal['core']


class PlatformGroupAttributes(BaseModel):
    model_config = ConfigDict(
        title='PlatformGroupAttributes',
        extra='allow'
    )

    spif_group_type: Literal['platform']


class InstrumentGroupAttributes(BaseModel):
    model_config = ConfigDict(
        # Configuration options here
        title='Instrument Group Attributes',
        extra='allow'
    )

    # Add your attributes here, e.g.
    #
    # my_attribute: str = Field(
    #   description='A description of my attribute',
    #   example='my_attribute_value'
    # )
    spif_group_type: Literal['instrument']

    instrument_name: str = Field(
        description='Short name of the instrument. May be the same as the group name.',
        example='instrument_name_value'
    )

    instrument_long_name: str = Field(
        description='Full descriptive name of the instrument.',
        example='instrument_long_name_value'
    )

    instrument_serial_number: Optional[str] = Field(
        description='Serial number or instrument identifier.',
        example='instrument_serial_number_value',
        default=None
    )

    instrument_firmware: Optional[str] = Field(
        description='Instrument firmware version.',
        example='instrument_firmware_value',
        default=None
    )

    instrument_software: Optional[str] = Field(
        description='Name and version of the data acquisition software interfacing with the instrument.',
        example='instrument_software_value',
        default=None
    )

    instrument_manufacturer: Optional[str] = Field(
        description='Name of the instrument manufacturer.',
        example='instrument_manufacturer_value',
        default=None
    )

    platform: Optional[str] = Field(
        description='Name of the platform on which the instrument is mounted.',
        example='platform_value',
        default=None
    )

    raw_filenames: Optional[str] = Field(
        description='List of raw filenames used to create this dataset.',
        example='raw_filenames_value',
        default=None
    )

    references: Optional[str] = Field(
        description='Link to webpage. publications, or other references for this instrument.',
        example='references_value',
        default=None
    )
