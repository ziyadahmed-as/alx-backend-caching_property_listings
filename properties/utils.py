# properties/utils.py
from django_redis import get_redis_connection
import logging
from django.core.cache import cache
from .models import Property

def get_all_properties():
    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all())  # Convert queryset to list for caching
        cache.set('all_properties', properties, 3600)  # Cache for 1 hour
    return properties

# Configure logging
logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    try:
        redis_conn = get_redis_connection("default")  # Adjust cache alias if needed
        info = redis_conn.info('stats')
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)

        total_requests = hits + misses
        if total_requests > 0:
            hit_ratio = hits / total_requests
        else:
            hit_ratio = 0

        logger.info(f"Redis Cache Metrics - Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio:.2f}")

        return {
            'hits': hits,
            'misses': misses,
            'hit_ratio': hit_ratio
        }
    except Exception as e:
        logger.error(f"Failed to retrieve Redis cache metrics: {e}")
        return None