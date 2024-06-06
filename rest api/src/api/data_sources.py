from fastapi import APIRouter, HTTPException
from src.db.cassandra_models import DataSource
from src.db.pydantic_models import DataSourceModel
from src.db.database import initialize_cassandra_connection
from typing import List

router = APIRouter()

@router.get("/data_sources", response_model=List[DataSourceModel])
def get_data_sources():
    initialize_cassandra_connection()
    data_sources = DataSource.objects.all()
    return [DataSourceModel.from_orm(ds) for ds in data_sources]

@router.get("/data_sources/{source_id}", response_model=DataSourceModel)
def get_data_source(source_id: str):
    initialize_cassandra_connection()
    data_source = DataSource.objects.filter(source_id=source_id).first()
    if not data_source:
        raise HTTPException(status_code=404, detail="Data source not found")
    return DataSourceModel.from_orm(data_source)
