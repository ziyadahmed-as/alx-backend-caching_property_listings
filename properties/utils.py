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

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    try:
        # Get the Redis connection used by Django cache
        connection = get_redis_connection("default")
        
        # Retrieve Redis INFO stats
        info = connection.info()
        
        keyspace_hits = info.get("keyspace_hits", 0)
        keyspace_misses = info.get("keyspace_misses", 0)
        
        total = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total) if total > 0 else 0
        
        metrics = {
            "keyspace_hits": keyspace_hits,
            "keyspace_misses": keyspace_misses,
            "hit_ratio": hit_ratio,
        }
        
        # Log the metrics (you can also write to a file or use other logging methods)
        logger.info(f"Redis Cache Metrics: Hits={keyspace_hits}, Misses={keyspace_misses}, Hit Ratio={hit_ratio:.2%}")
        
        return metrics
    
    except Exception as e:
        logger.error(f"Failed to get Redis cache metrics: {e}")
        return None
