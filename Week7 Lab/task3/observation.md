## Task3
The naive switch evicts the oldest entry by insertion time. This is bad because frequently used hosts may be kicked out when rarely-seen new hosts arrive, which causes unnecessary flooding.
My switch uses the LRU (least recently used) strategy. When a MAC entry is used either as source or destination, it is marked as recently used. When the table is full, the least recently used entry is removed.
This keeps busy hosts in the table longer and reduces flooding. No packets are lost, and wasted flooding traffic is cut by 32% in this test trace.