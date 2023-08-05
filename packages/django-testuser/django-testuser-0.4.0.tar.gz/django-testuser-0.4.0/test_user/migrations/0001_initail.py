from django.apps.registry import Apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db import migrations
from env_settings import env


def add_default_admin_for_testing_on_non_prod_env(apps: Apps, _):
    if env.is_prod():
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
    setattr(user, user.EMAIL_FIELD, email_and_pass)
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
