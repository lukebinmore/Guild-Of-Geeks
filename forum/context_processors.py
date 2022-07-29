from . import forms


def filters(request):
    """
    Return a dictionary with a key of 'filters'
    and a value of the FilterForm class.

    :param request: The current request object
    :return: A dictionary with a key of "filters"
    and a value of the FilterForm object.
    """
    return {"filters": forms.FilterForm()}
