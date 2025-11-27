from django.db import migrations
from django.conf import settings
from pathlib import Path
import json


def load_initial_products(apps, schema_editor):
    Category = apps.get_model("category", "Category")
    Product = apps.get_model("store", "Product")

    # Path to the JSON fixture (you created this earlier)
    fixture_path = Path(settings.BASE_DIR) / "initial_products.json"

    if not fixture_path.exists():
        # If file is missing, do nothing (avoid deployment crash)
        return

    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        model = entry.get("model")
        pk = entry.get("pk")
        fields = entry.get("fields", {})

        # Load categories first
        if model == "category.category":
            Category.objects.update_or_create(
                pk=pk,
                defaults=fields,
            )

    # Second pass: load products (now categories exist)
    for entry in data:
        model = entry.get("model")
        pk = entry.get("pk")
        fields = entry.get("fields", {})

        if model == "store.product":
            category_id = fields.pop("category", None)
            category = None
            if category_id is not None:
                category = Category.objects.filter(pk=category_id).first()
            if not category:
                continue

            Product.objects.update_or_create(
                pk=pk,
                defaults={**fields, "category": category},
            )


def unload_initial_products(apps, schema_editor):
    # Reverse migration (optional cleanup)
    Product = apps.get_model("store", "Product")
    Product.objects.all().delete()
    # We keep categories; remove them too if you really want:
    # Category = apps.get_model("category", "Category")
    # Category.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0003_reviewrating"),  # keep this as in your screenshot
        ("category", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_initial_products, reverse_code=unload_initial_products),
    ]
