from . import factory
from . import filter as ft

def dictfy(
        obj, query, flat_obj=None,
        nested_flat_obj=None, nested_iter_obj=None):
    return factory._dict(
        obj,
        query,
        flat_obj,
        nested_flat_obj,
        nested_iter_obj,
    )


def filter(
        obj, query, flat_obj=None,
        nested_flat_obj=None, nested_iter_obj=None):
    return ft.filtered_dict(
        obj,
        query,
        flat_obj,
        nested_flat_obj,
        nested_iter_obj,
    )

def useobj(function, query=None):
    return factory.UseObj(function, query)


def objfield(field_name, call=False, args=tuple(), kwargs={}):
    if call:
        return useobj(
            lambda obj: getattr(obj, field_name)(*args, **kwargs),
            query=None
        )
    else:
        return useobj(lambda obj: getattr(obj, field_name), query=None)


def dictfield(field_name, call=False, args=tuple(), kwargs={}):
    if call:
        return useobj(
            lambda obj: obj[field_name](*args, **kwargs),
            query=None
        )
    else:
        return useobj(lambda obj: obj[field_name], query=None)


def newfield(value):
    return factory.NewField(value)
