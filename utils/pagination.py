def pagination(limit: int = 5, offset: int = 1, data = []):
    start = (offset - 1) * limit
    end = start + limit
    return data[start:end]