from django.contrib.auth.hashers import make_password
from django.db import migrations


def seed_accounts(apps, schema_editor):
    # Historical models from apps.get_model() don't carry AbstractBaseUser
    # methods (set_password), so hash passwords directly with make_password.
    User = apps.get_model("accounts", "User")

    if not User.objects.filter(phone="A12s12df$").exists():
        User.objects.create(
            phone="A12s12df$",
            password=make_password("A12s12df$"),
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

    if not User.objects.filter(phone="admin").exists():
        User.objects.create(
            phone="admin",
            password=make_password("admin@789"),
            is_staff=True,
            is_superuser=False,
            is_active=True,
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0045_alter_withdrawalrequest_status"),
    ]

    operations = [
        migrations.RunPython(seed_accounts, noop),
    ]
