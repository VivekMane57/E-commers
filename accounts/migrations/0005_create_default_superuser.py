from django.db import migrations
import json
import os
from django.conf import settings


def load_initial_products(apps, schema_editor):
    Category = apps.get_model("category", "Category")
    Product = apps.get_model("store", "Product")

    file_path = os.path.join(settings.BASE_DIR, "initial_products.json")

    # Check file exists
    if not os.path.exists(file_path):
        print("⚠️ initial_products.json not found. Skipping import.")
        return

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        model = item["model"]

        if model == "category.category":
            Category.objects.update_or_create(
                id=item["pk"],
                defaults=item["fields"]
            )

        elif model == "store.product":
            Product.objects.update_or_create(
                id=item["pk"],
                defaults=item["fields"]
            )

    print("✅ Categories & Products loaded successfully!")


def reverse_data(apps, schema_editor):
    """Deletes all imported data if migration is rolled back."""
    Category = apps.get_model("category", "Category")
    Product = apps.get_model("store", "Product")
    Product.objects.all().delete()
    Category.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_reviewrating"),
        ("category", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_initial_products, reverse_data),
    ]
