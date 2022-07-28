from . import forms


def filters(request):
    return {"filters": forms.FilterForm()}
