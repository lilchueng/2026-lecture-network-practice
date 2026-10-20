# Observation for Task3 Longest Prefix Match

## Structure chosen
I selected the **prefix‑length grouped hash table** approach.
We maintain 33 hash dictionaries, one for each possible IPv4 prefix length (0 to 32). When adding a route, we store the network and next hop into the bucket corresponding to its prefix length. For lookup, we check buckets starting from length 32 down to 0, and return the first matched next hop.

## Memory cost
Memory overhead comes from 33 Python dictionaries storing all route entries. Each routing entry is stored exactly once, so total memory scales linearly with the number of prefixes, similar to the baseline linear table, with extra small overhead for the hash table metadata.

## Lookup complexity & measured performance
The lookup time is bounded by **at most 33 hash lookups**, independent of how many routing entries exist in the table. The running time is proportional to the fixed number of possible prefix lengths (33), not the total route count.
In this benchmark with 5,000 prefixes and 20,000 queries, the implementation achieves **329.8× speedup** over the linear baseline, reaching the "good" grade.

## Why hardware prefers bit‑walk (trie), even though hash grouping is faster in Python
Hardware routers use a bit‑by‑bit binary trie for longest prefix match. In ASIC hardware, sequential bit traversal can be fully pipelined and parallelized to deliver wire‑speed constant‑time forwarding.
In Python, however, object overhead and pointer chasing make trie implementations relatively slow. Hash dictionaries in Python are heavily optimized at the C level, so the simpler bucket‑hash method outperforms the textbook trie in this environment. Therefore, the algorithm best suited for Python differs from the one implemented in router hardware.