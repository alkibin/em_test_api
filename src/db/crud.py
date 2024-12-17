from sqlalchemy import select


def _get_all(table, limit, offset):
    query = select(table)
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    return query
