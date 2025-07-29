from src.services.redis_service import RedisService


RedisService.initialize(
        host="localhost",
        port=6379,
        username="default",
        password="redispw",
        db=0
    )

redis_service = RedisService.get_instance()

redis_service.set("mykey", "Hello Devendra", ex=60)
value = redis_service.get("mykey")
print("Fetched Value:", value)
