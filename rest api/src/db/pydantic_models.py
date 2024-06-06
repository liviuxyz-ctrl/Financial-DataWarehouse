from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
import uuid

class AssetModel(BaseModel):
    asset_id: uuid.UUID
    name: str
    type: str

    class Config:
        orm_mode = True

class DataSourceModel(BaseModel):
    source_id: uuid.UUID
    source_name: str

    class Config:
        orm_mode = True

class FinancialDataModel(BaseModel):
    asset_id: uuid.UUID
    source_id: uuid.UUID
    business_date: date
    system_time: datetime
    symbol: str
    open: Optional[float]
    high: Optional[float]
    low: Optional[float]
    close: Optional[float]
    volume: Optional[int]

    class Config:
        orm_mode = True

class CommodityDataModel(BaseModel):
    asset_id: uuid.UUID
    source_id: uuid.UUID
    business_date: date
    system_time: datetime
    symbol: str
    value: float

    class Config:
        orm_mode = True
