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


# src/ingestion/transform.py
def transform_commodity_data(symbol, raw_data):
    print(f"Raw data for {symbol}: {raw_data}")  # Debugging line

    if 'data' not in raw_data:
        print(f"Unexpected data format for {symbol}: {raw_data}")  # Debugging line
        return []

    transformed = []
    for data in raw_data['data']:
        # Ensure data is a dictionary with expected keys
        if not isinstance(data, dict) or 'date' not in data or 'value' not in data:
            print(f"Unexpected item format in data list for {symbol}: {data}")  # Debugging line
            continue

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
