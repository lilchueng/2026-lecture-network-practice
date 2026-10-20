# Observation for Task1 Subnets & Longest-Prefix Match

## 1. Return values for /31 and /32
- **/32**: This is a host route matching exactly one IP. There is no separate network address or broadcast address. I return the same IP for first usable, last usable, and broadcast.
- **/31**: Following RFC 3021 for point-to-point links. Both addresses in this subnet are usable for hosts; there is no dedicated broadcast address. I return the two addresses of the subnet as first and last usable, and use the second address as broadcast.

## 2. Matched prefixes for 10.20.30.70
The four matching CIDR entries:
1. 0.0.0.0/0 (default route)
2. 10.0.0.0/8 (campus)
3. 10.20.0.0/16 (eng-building)
4. 10.20.30.0/24 (lab-floor)
5. 10.20.30.64/26 (lab-rack-2)
> The longest match winner: **10.20.30.64/26 → lab-rack-2**, because longest-prefix match selects the entry with maximum prefix length.

## 3. Policy for entries with identical prefix length but different next hops
If two routes have the same prefix length but different network addresses: both routes are kept and evaluated normally during lookup.
If two routes have **the same network and same prefix length** (duplicate prefix): the later entry overwrites the old one, so only the newest next hop remains in the forwarding table.