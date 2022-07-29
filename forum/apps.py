from django.apps import AppConfig


# The default_auto_field attribute is set
# to the BigAutoField class, which is a subclass of AutoField.
class ForumConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "forum"
