if env.bool("REDIS"):
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env("REDIS_URL"),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                # "PARSER_CLASS": "redis.connection.HiredisParser",
                "IGNORE_EXCEPTIONS": True,
                "CONNECTION_POOL_KWARGS": {
                    "max_connections": 100,
                    "retry_on_timeout": True,
                },
            },
            "KEY": "backend_cache",
        }
    }

    # Standardize Cache TTL (Time To Live) to 15 minutes
    CACHE_TTL = 60 * 15
