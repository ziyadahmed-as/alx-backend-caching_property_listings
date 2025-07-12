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
    """
    Connect to Redis, retrieve keyspace_hits and keyspace_misses,
    calculate and return hit_ratio, and log the metrics.
    """
    try:
        redis_conn = get_redis_connection("default")  # Adjust cache alias if needed
        info = redis_conn.info('stats')
        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)

        total_requests = hits + misses
        # Calculates and returns hit_ratio
        hit_ratio = hits / total_requests if total_requests > 0 else 0

        logger.info(
            f"Redis Cache Metrics - Hits: {hits}, "
            f"Misses: {misses}, Hit Ratio: {hit_ratio:.2f}"
        )

        return {
            'hits': hits,
            'misses': misses,
            'hit_ratio': hit_ratio
        }
    except Exception as e:
        logger.error(f"Failed to retrieve Redis cache metrics: {e}")
        return None
