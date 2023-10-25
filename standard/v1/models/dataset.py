
from typing import Optional
import netCDF4 # type: ignore

from pydantic import BaseModel, Field

from vocal.netcdf.mixins import DatasetNetCDFMixin

from ..attributes import GlobalAttributes

from .dimension import Dimension
from .group import InstrumentGroup
from .variable import Variable


class DatasetMeta(BaseModel):
    file_pattern: str = Field(description='Canonical filename pattern for this dataset')
    short_name: Optional[str] = Field(description='Unique hort name for this dataset', default=None)
    description: Optional[str] = Field(description='Description of this dataset', default=None)
    references: Optional[list[tuple[str, str]]] = Field(description='References for this dataset', default=None)


class Dataset(BaseModel, DatasetNetCDFMixin):
    class Config:
        title = 'Dataset Schema'

    meta: DatasetMeta
    attributes: GlobalAttributes
    dimensions: Optional[list[Dimension]] = None
    groups: list[InstrumentGroup]
    variables: list[Variable]
