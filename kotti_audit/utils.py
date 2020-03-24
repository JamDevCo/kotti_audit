from kotti.resources import Content
from sqlalchemy import and_, func


def date_query(query, column_name, value, cls=Content):
    column = cls.__dict__.get(column_name)
    return query.filter(
        and_(
            func.date(column) >= func.date(value),
            func.date(column) <= func.date(value)
        )
    )