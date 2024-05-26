import requests


def clickhouse_request(query):
    url = 'http://clickhouse:8123'
    params = {'query': query}
    response = requests.get(url, params=params)
    response.raise_for_status()

    return [
        row.split('\t')
        for row in response.text.strip().split('\n')
    ]
