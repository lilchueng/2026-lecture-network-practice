# Task3 DNS Cache Observation

## 1. Problems in BaselineCache
The baseline DNS cache has two critical defects.
1. It does **not check TTL expiration** before returning cached records. It returns expired DNS entries directly, which creates stale answers. This violates DNS caching rules.
2. Expired records remain stored in the cache forever. The cache cannot automatically invalidate old data. Even after the TTL time passes, it keeps serving invalid records.

The baseline cache has only 10 upstream calls. However, this low number is achieved by continuously returning expired DNS records. This behavior violates DNS caching rules and produces 811 stale responses. A correct cache must refresh expired entries, which inevitably increases upstream requests.

## 2. Theoretical minimum upstream queries
There is a lower bound for upstream requests for any correct cache.
All 10 unique domain names need at least one initial query.
If a record expires during the 3600s simulation, we must refresh it from upstream. We cannot skip these refreshes, otherwise stale responses will be produced.
The domain `www.microsoft.com` has TTL=20 seconds. It expires many times within one hour, causing repeated upstream lookups. This sets the minimal number of upstream calls.

## 3. The most difficult record
`www.microsoft.com` has TTL of only 20 seconds. It expires very quickly.
Since this domain is queried frequently, our cache must refresh it many times in the one-hour simulation.
The baseline cache ignores expiration and returns stale data. A correct cache must discard expired entries and re-fetch, which increases upstream requests for this domain.