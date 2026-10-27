### Task1
1. Tie-breaking rule for equal-cost paths: pick the neighbor with lexicographically smaller node name. Real OSPF routers may use router ID for tie-break.
2. For source u to destination w, the next hop is x, not w. Direct link u-w cost=5, while u-x-y-w total cost=3, which is shorter.
3. After link u-x fails: destinations x, y, w, z change their next hop; v remains unchanged.