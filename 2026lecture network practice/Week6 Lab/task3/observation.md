### Task3 Observation
My implementation keeps a cached shortest-path tree (distance and predecessor table) computed by an internal Dijkstra.
The optimization rule: only skip full SPF recomputation when a link’s cost increases and that link is not on the current shortest-path tree.
All other events, including link down, new link addition and link cost reduction, trigger a full SPF run to guarantee correct forwarding table.

This reduces SPF runs from 1001 to 874 (13% saved) in the benchmark.
In Python, the wall time becomes longer because of our internal Dijkstra overhead.
For real routers, full SPF is CPU-heavy, so reducing SPF runs lowers CPU load when links flap frequently. Memory for storing predecessor and distance maps is cheap on network devices.