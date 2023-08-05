from django.apps.registry import Apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import migrations
from settings_utils.env import DjangoEnv


def add_default_admin_for_testing_on_non_prod_env(apps: Apps, _):
    is_prod_env = settings.DJANGO_ENV == DjangoEnv.PROD
    if is_prod_env:
        return

    User = get_user_model()
    email_and_pass = settings.TEST_USER_USERNAME_AND_PASS
    if User.objects.filter(email=email_and_pass).exists():
        return
    # `create_superuser` and `set_password` aren't going to work in migrations
    user = User(
        is_staff=True,
        is_superuser=True,
    )
    setattr(user, user.USERNAME_FIELD, email_and_pass)
    user.password = make_password(email_and_pass)
    user.save()


user_model_app_label, _ = settings.AUTH_USER_MODEL.split('.')


class Migration(migrations.Migration):

    dependencies = [
        (user_model_app_label, '__latest__'),
    ]
    
    operations = [
        migrations.RunPython(add_default_admin_for_testing_on_non_prod_env),
    ]
