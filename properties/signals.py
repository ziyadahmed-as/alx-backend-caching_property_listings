# properties/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property
# Signal handlers to clear cache when a Property instance is saved or deleted
@receiver(post_save, sender=Property)
def clear_cache_on_save(sender, instance, **kwargs):
    cache.delete('all_properties')

# Signal handler to clear cache when a Property instance is deleted
@receiver(post_delete, sender=Property)
def clear_cache_on_delete(sender, instance, **kwargs):
    cache.delete('all_properties')
