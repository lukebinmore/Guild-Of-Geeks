from django.contrib import admin
from . import models
from django_summernote.admin import SummernoteModelAdmin

all_models = [
    models.Post,
    models.Profile,
    models.Category,
    models.Tag,
    models.Comment
]


class SummernoteAdmin(SummernoteModelAdmin):
    summernote_fields = ('content')

admin.site.register(all_models, SummernoteAdmin)