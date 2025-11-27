from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_default_superuser(apps, schema_editor):
    Account = apps.get_model("accounts", "Account")

    # Avoid duplicate creation
    if Account.objects.filter(email="admin@buytogether.in").exists():
        return

    # Create the user with hashed password
    user = Account(
        first_name="Admin",
        last_name="User",
        email="admin@buytogether.in",
        username="admin",
        password=make_password("Admin@1234"),  # hashing here
    )

    # Assign role flags only if they exist
    for flag in ["is_superuser", "is_staff", "is_admin", "is_superadmin", "is_active"]:
        if hasattr(user, flag):
            setattr(user, flag, True)

    user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_alter_account_last_login_alter_account_referral_code"),
    ]

    operations = [
        migrations.RunPython(create_default_superuser),
    ]
