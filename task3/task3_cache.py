# task3_cache.py
# task3_cache.py
class BaselineCache:
    def __init__(self, upstream):
        self.upstream = upstream
        self.cache = dict()

    def lookup(self, name, now):
        if name in self.cache:
            ans, exp = self.cache[name]
            # Original bug: no TTL expiration check
            return ans
        else:
            ans, ttl = self.upstream(name)
            exp = now + ttl
            self.cache[name] = (ans, exp)
            return ans


class YourCache:
    def __init__(self, upstream):
        self.upstream = upstream
        # cache: domain -> (answer, expire_time)
        self.cache = {}

    def lookup(self, name, now):
        if name in self.cache:
            answer, expire_time = self.cache[name]
            # Return cached value if it is still valid
            if now < expire_time:
                return answer
        
        # Reach here if:
        # 1. domain is not in cache OR 2. cached record is expired
        answer, ttl = self.upstream(name)
        new_expire = now + ttl
        self.cache[name] = (answer, new_expire)
        return answer