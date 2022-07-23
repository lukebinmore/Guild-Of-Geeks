from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from . import models

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

def validate_category(form, title):
    if not title.isdigit():
        if not models.Category.objects.filter(title=title).exists():
            category = models.Category.objects.create(title=title)
            form.set_category(category)
    else:
        if not models.Category.objects.filter(id=title).exists():
            del form.errors['category'][0]
            form.add_error('category', 'Category can not be numbers only!')
    return form

def validate_tags(form, tags):
    new_tags = []
    for tag in tags:
        if not tag.isdigit():
            if not models.Tag.objects.filter(title=tag).exists():
                new_tags.append(models.Tag.objects.create(title=tag))
        else:
            if not models.Tag.objects.filter(id=tag).exists():
                del form.errors['tags'][0]
                form.add_error('tags', 'Tags may not be just numbers!')
            else:
                new_tags.append(tag)
    form.set_tags(new_tags)
    return form