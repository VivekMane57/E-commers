from django.db import migrations
import json
import os


def load_initial_products(apps, schema_editor):
    Product = apps.get_model("store", "Product")
    Category = apps.get_model("category", "Category")

    file_path = os.path.join(os.path.dirname(__file__), "../../initial_products.json")

    # Read JSON with proper encoding
    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        model = entry["model"]
        fields = entry["fields"]

        if model == "category.category":
            Category.objects.update_or_create(
                id=entry["pk"], defaults=fields
            )

        elif model == "store.product":
            category_id = fields.pop("category")
            category = Category.objects.get(id=category_id)

            Product.objects.update_or_create(
                id=entry["pk"], defaults={**fields, "category": category}
            )


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_reviewrating'),
    ]

    operations = [
        migrations.RunPython(load_initial_products),
    ]
