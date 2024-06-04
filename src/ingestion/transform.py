# src/ingestion/transform.py
def transform_financial_data(symbol, raw_data):
    transformed = []
    for data in raw_data:
        try:
            transformed.append({
                'symbol': symbol,
                'date': data[0],
                'open': data[1],
                'high': data[2],
                'low': data[3],
                'close': data[4],
                'volume': data[5]
            })
        except IndexError:
            print("Data format error with:", data)
    return transformed


def transform_commodity_data(symbol, raw_data):
    transformed = []
    for data in raw_data['data']:
        try:
            value = float(data['value'])
            transformed.append({
                'symbol': symbol,
                'date': data['date'],
                'value': value
            })
        except ValueError as e:
            print(f"Data format error with: {data}, error: {e}")
    return transformed
