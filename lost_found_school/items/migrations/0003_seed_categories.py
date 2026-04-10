from django.db import migrations


def seed_categories(apps, schema_editor):
    Category = apps.get_model('items', 'Category')
    categories = [
        'Electronics',
        'School Supplies',
        'Clothing',
        'Bags & Pouches',
        'Accessories',
        'ID / Cards / Wallet',
        'Water Bottle / Tumbler',
        'Keys',
        'Books',
        'Sports Equipment',
        'Umbrella',
        'Others',
    ]
    for name in categories:
        Category.objects.get_or_create(name=name)


def remove_categories(apps, schema_editor):
    Category = apps.get_model('items', 'Category')
    Category.objects.filter(name__in=[
        'Electronics',
        'School Supplies',
        'Clothing',
        'Bags & Pouches',
        'Accessories',
        'ID / Cards / Wallet',
        'Water Bottle / Tumbler',
        'Keys',
        'Books',
        'Sports Equipment',
        'Umbrella',
        'Others',
    ]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_alter_item_category_alter_item_date_lost_found_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_categories, remove_categories),
    ]
