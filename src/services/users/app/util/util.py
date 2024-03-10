

def get_field(request, field, default=None):
    return request.json.get(field, default)
