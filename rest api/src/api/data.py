from fastapi import APIRouter, HTTPException, Query
from db.cassandra_models import initialize_cassandra_connection, create_financial_data_model, \
    create_commodity_data_model
from db.pydantic_models import FinancialDataModel, CommodityDataModel
from typing import List

router = APIRouter()


def orm_to_pydantic(orm_instance, model_type='financial'):
    if model_type == 'financial':
        return {
            "asset_id": str(orm_instance.asset_id),
            "source_id": str(orm_instance.source_id),
            "business_date": str(orm_instance.business_date),
            "system_time": str(orm_instance.system_time),
            "symbol": orm_instance.symbol,
            "open": orm_instance.open,
            "high": orm_instance.high,
            "low": orm_instance.low,
            "close": orm_instance.close,
            "volume": orm_instance.volume
        }
    elif model_type == 'commodity':
        return {
            "asset_id": str(orm_instance.asset_id),
            "source_id": str(orm_instance.source_id),
            "business_date": str(orm_instance.business_date),
            "system_time": str(orm_instance.system_time),
            "symbol": orm_instance.symbol,
            "value": orm_instance.value
        }


@router.get("/data/{asset_id}", response_model=List[FinancialDataModel])
def get_asset_data(
        asset_id: str,
        limit: int = Query(20, description="Number of records to return"),
        offset: int = Query(0, description="Number of records to skip from the beginning")
):
    initialize_cassandra_connection()
    sanitized_asset_id = asset_id.split('/')[-1].lower()  # Remove any prefix and convert to lowercase
    financial_data_model = create_financial_data_model(sanitized_asset_id)
    try:
        all_data = list(financial_data_model.objects.limit(limit * (offset + 1)))
        if not all_data:
            raise HTTPException(status_code=404, detail="No data found for the given asset ID")
        paginated_data = all_data[offset * limit: (offset + 1) * limit]
        result = [FinancialDataModel(**orm_to_pydantic(item, 'financial')) for item in paginated_data]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying data: {str(e)}")


@router.get("/commodities/{commodity_id}", response_model=List[CommodityDataModel])
def get_commodity_data(
        commodity_id: str,
        limit: int = Query(20, description="Number of records to return"),
        offset: int = Query(0, description="Number of records to skip from the beginning")
):
    initialize_cassandra_connection()
    sanitized_commodity_id = commodity_id.lower()  # Convert to lowercase
    commodity_data_model = create_commodity_data_model(sanitized_commodity_id)
    try:
        all_data = list(commodity_data_model.objects.limit(limit * (offset + 1)))
        if not all_data:
            raise HTTPException(status_code=404, detail="No data found for the given commodity ID")
        paginated_data = all_data[offset * limit: (offset + 1) * limit]
        result = [CommodityDataModel(**orm_to_pydantic(item, 'commodity')) for item in paginated_data]
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying data: {str(e)}")
