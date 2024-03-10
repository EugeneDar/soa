from datetime import datetime


def get_field(request, field, default=None):
    return request.json.get(field, default)


def try_parse_date(value):
    if value is None:
        return None
    try:
        converted = datetime.strptime(value, "%Y-%m-%d").date()
        return converted
    except ValueError:
        return None
