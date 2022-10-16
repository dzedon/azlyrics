FILTER_MAP = {
    "equals": lambda query, field, value: query.filter(field == value),
    "not_equals": lambda query, field, value: query.filter(field != value),
    "greater_than": lambda query, field, value: query.filter(field > value),
    "greater_equals_than": lambda query, field, value: query.filter(field >= value),
    "less_than": lambda query, field, value: query.filter(field < value),
    "less_equals_than": lambda query, field, value: query.filter(field <= value),
    "like": lambda query, field, value: query.filter(field.like(f"%{value}%")),
    "ilike": lambda query, field, value: query.filter(field.ilike(f"%{value}%")),
    "not_ilike": lambda query, field, value: query.filter(~field.ilike(f"%{value}%")),
    "in": lambda query, field, value: query.filter(field.in_(value)),
    "not_in": lambda query, field, value: query.filter(~field.in_(value)),
}
