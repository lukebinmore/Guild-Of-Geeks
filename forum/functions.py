from django.shortcuts import get_object_or_404, render
from django.urls import reverse

def previous_page(request):
    return render(
        request,
        'redirect.html',
        {
            'redirect_url': request.META['HTTP_HX_CURRENT_URL']
        }
    )

def redirect_page(request, page, **kwargs):
    return render(
        request,
        'redirect.html',
        {
            'redirect_url': reverse(page, kwargs=kwargs)
        }
    )

def form_field_errors(*args):
    for form in args:
        for field in form:
            if field.errors:
                return f'{field.name.title()} : {field.errors[0]}'

def get_object(model, **kwargs):
    queryset = model.objects.all()
    return get_object_or_404(queryset, **kwargs)
