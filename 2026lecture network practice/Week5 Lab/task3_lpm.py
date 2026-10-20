#!/usr/bin/env python3
"""Week 5 · Task 3 — Make longest-prefix match fast.

Textbook §4.3.3.

`LinearTable` is correct and it is what you probably wrote in Task 1: keep the
prefixes in a list, check every one, remember the longest that matched. On six
entries that is fine. A real router holds close to a million, and it has to
answer while the packet is still in the buffer.

Beat it:

    python3 bench.py
    python3 bench.py --yours

Correctness first: `bench.py` checks every one of your answers against the
linear table. A fast router that forwards to the wrong next hop is not a
router, it is an outage.
"""


class LinearTable:
    """Correct, and slow in the obvious way."""

    def __init__(self):
        self.entries = []                     # (prefix_len, network, next_hop)

    def add(self, network, prefix_len, next_hop):
        self.entries.append((prefix_len, network, next_hop))

    def lookup(self, address):
        best = None
        for plen, net, hop in self.entries:
            mask = (0xFFFFFFFF << (32 - plen)) & 0xFFFFFFFF
            if address & mask == net and (best is None or plen > best[0]):
                best = (plen, hop)
        return best[1] if best else None


class YourTable:
    def __init__(self):
        # 索引：prefix_len → {network_int: next_hop}
        self.buckets = [dict() for _ in range(33)]

    def add(self, network, prefix_len, next_hop):
        self.buckets[prefix_len][network] = next_hop

    def lookup(self, address):
        # 从最长前缀32，往下查到0，命中就返回
        for plen in range(32, -1, -1):
            mask = (0xFFFFFFFF << (32 - plen)) & 0xFFFFFFFF
            net = address & mask
            if net in self.buckets[plen]:
                return self.buckets[plen][net]
        return None