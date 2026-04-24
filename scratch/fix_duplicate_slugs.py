from core.models import Category
from django.utils.text import slugify

# Find categories with duplicate slugs
slugs = Category.objects.values_list('slug', flat=True)
duplicate_slugs = set([x for x in slugs if list(slugs).count(x) > 1])

print(f"Duplicate slugs found: {duplicate_slugs}")

for slug in duplicate_slugs:
    categories = Category.objects.filter(slug=slug)
    print(f"Found {categories.count()} categories for slug: {slug}")
    for i, cat in enumerate(categories):
        if i > 0:
            new_slug = f"{slug}-{i}"
            print(f"Updating category '{cat.title}' slug from '{slug}' to '{new_slug}'")
            cat.slug = new_slug
            cat.save()

print("Cleanup complete.")
