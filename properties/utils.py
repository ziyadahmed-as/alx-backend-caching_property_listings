# properties/utils.py

from django.core.cache import cache
from .models import Property

def get_all_properties():
    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all())  # Convert queryset to list for caching
        cache.set('all_properties', properties, 3600)  # Cache for 1 hour
    return properties
