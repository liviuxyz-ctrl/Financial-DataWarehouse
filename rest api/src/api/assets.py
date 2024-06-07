from fastapi import APIRouter, HTTPException
from db.cassandra_models import Asset, initialize_cassandra_connection
from db.pydantic_models import AssetModel
from typing import List

router = APIRouter()


@router.get("/assets", response_model=List[str])
def get_assets(offset: int = 0, limit: int = 20):
    initialize_cassandra_connection()
    assets = Asset.objects.all()[offset:offset + limit]
    return [asset.name for asset in assets]


@router.get("/assets/{asset_id}", response_model=AssetModel)
def get_asset(asset_id: str):
    initialize_cassandra_connection()
    asset = Asset.objects.filter(name=asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return AssetModel.from_orm(asset)
