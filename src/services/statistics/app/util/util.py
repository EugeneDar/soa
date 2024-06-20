import requests


def parse_http_response(response):
    if len(response.strip()) == 0:
        return []
    return [
        row.split('\t')
        for row in response.strip().split('\n')
    ]


def clickhouse_request(query):
    url = 'http://clickhouse:8123'
    params = {'query': query}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return parse_http_response(response.text)
