def clone(model):
    new_kwargs = dict(
        [(fld.name, getattr(model, fld.name)) for fld in model._meta.fields if fld.name != model._meta.pk])

    return model.__class__(**new_kwargs)


def get_field(clazz, name):
    for field in clazz._meta.fields:
        if field.name == name:
            return field

    return None
