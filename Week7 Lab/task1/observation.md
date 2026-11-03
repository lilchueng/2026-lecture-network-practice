## Task1 Observation
1. Why must a frame never go back out of the port it came in on? Give the concrete thing that breaks if it does.
If a frame is sent back out its incoming port, it creates a forwarding loop. The frame will keep circulating between devices, flooding the LAN with duplicate traffic and eventually causing broadcast storm, which consumes bandwidth and crashes the network.

2. A switch floods when it does not know. A router drops. Why the difference?
Switches work at Layer 2 inside one broadcast domain. Flooding sends the frame to all ports to find the target host within the same local LAN.
Routers work at Layer 3 between separate networks. There is no cross-network broadcast. Without a matching route, the router has no way to forward the packet, so it drops it.

3. Your aging is a timeout. What does the switch lose by using time rather than something more direct, and what would "more direct" even be?
Time-based aging is only a guess. It may delete entries for active hosts that are quiet temporarily, or keep stale entries for hosts that have moved away.
A more direct method is removing MAC entries when the switch detects a port link-down event, or when a host sends a frame from a new port to overwrite the old record.